from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Role, UserProfile

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.role.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'error': 'Insufficient permissions'}, status=403)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User profile not found'}, status=403)
        return _wrapped_view
    return decorator

# Convenience decorators for specific roles
super_admin_required = role_required(Role.SUPER_ADMIN)
manager_required = role_required(Role.SUPER_ADMIN, Role.MANAGER)
lawyer_required = role_required(Role.SUPER_ADMIN, Role.MANAGER, Role.LAWYER)
npl_required = role_required(Role.SUPER_ADMIN, Role.MANAGER, Role.LAWYER, Role.NPL)
user_required = role_required(Role.SUPER_ADMIN, Role.MANAGER, Role.LAWYER, Role.NPL, Role.USER)