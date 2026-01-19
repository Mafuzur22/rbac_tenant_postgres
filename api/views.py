from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from django.contrib.auth import get_user_model, authenticate, login
from .sereializer import UserSerializer, ApprovedUserSerializer
from main.decorators import manager_required
from .request_serializer import AccountRequestSerializer
from main.models import AccountRequest, Role, UserProfile
from main.decorators import super_admin_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

User = get_user_model()

@api_view(['GET'])
def api_root(request):
    return Response({"message": "Welcome to the multi-tenant API root!"})

@api_view(['GET'])
def sample_view(request):
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)   
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@manager_required
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'GET'])
def update_user(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Login successful', 'user_id': user.id})
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def logout_user(request):
    
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['POST'])
def request_account(request):
    serializer = AccountRequestSerializer(data=request.data)
    if serializer.is_valid():
        account_request = serializer.save()
        account_request.password = make_password(request.data.get('password'))
        account_request.save()
        return Response({'message': 'Account request submitted for approval'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@super_admin_required
def pending_requests(request):
    requests = AccountRequest.objects.filter(status=AccountRequest.PENDING)
    serializer = AccountRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@super_admin_required
def approve_request(request, request_id):
    try:
        account_request = AccountRequest.objects.get(id=request_id, status=AccountRequest.PENDING)
        
        # Use serializer to create user
        user_data = {
            'username': account_request.username,
            'email': account_request.email,
            'password': account_request.password,
            'role': account_request.requested_role
        }
        
        serializer = ApprovedUserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Update request status
            account_request.status = AccountRequest.APPROVED
            account_request.approved_by = request.user
            account_request.save()
            
            return Response({'message': 'Account approved and created', 'user_id': user.id})
        return Response(serializer.errors, status=400)
        
    except AccountRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)

@api_view(['POST'])
@super_admin_required
def reject_request(request, request_id):
    try:
        account_request = AccountRequest.objects.get(id=request_id, status=AccountRequest.PENDING)
        account_request.status = AccountRequest.REJECTED
        account_request.approved_by = request.user
        account_request.save()
        return Response({'message': 'Account request rejected'})
    except AccountRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)