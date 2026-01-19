from rest_framework.serializers import ModelSerializer, SerializerMethodField
from main.models import UserProfile, Role
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
class UserSerializer(ModelSerializer):
    role = SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role.get_name_display()
        except UserProfile.DoesNotExist:
            return None

    def create(self, validated_data):
        password = validated_data.pop('password')
        validate_password(password)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class ApprovedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = User(**validated_data)
        user.save()
        
        if role:
            UserProfile.objects.create(user=user, role=role)
        
        return user