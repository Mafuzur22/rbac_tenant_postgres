from django.urls import path
from .views import *

urlpatterns = [
    path('', api_root, name='api-root'),
    path('users/', sample_view, name='sample-view'),
    path('users/<int:user_id>/update/', update_user, name='update-user'),
    path('users/create/', create_user, name='create-user'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('request-account/', request_account, name='request-account'),
    path('pending-requests/', pending_requests, name='pending-requests'),
    path('approve-request/<int:request_id>/', approve_request, name='approve-request'),
    path('reject-request/<int:request_id>/', reject_request, name='reject-request'),
    
    ]