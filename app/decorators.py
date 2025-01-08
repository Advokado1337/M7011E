from functools import wraps
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


def token_and_superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Token required'}, status=401)
        
        token_key = auth_header.split('Token ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # Check if the user is a superuser
        if not user.is_superuser:
            return JsonResponse({'error': 'Superuser access required'}, status=403)
        
        # Allow the original view to execute
        return view_func(self, request, *args, **kwargs)
    
    return _wrapped_view

def token_and_isstaff_required(view_func):
    """
    A decorator to check if the user has a valid token and is staff.
    """
    @wraps(view_func)
    def _wrapped_view(self,request, *args, **kwargs):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        try:
            # Validate the token and get the associated user
            token = Token.objects.get(key=token_key)
            user = token.user  # Get the user linked to the token
            request.user = user  # Attach the user to the request object
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        # Check if the user is a superuser
        if not user.is_staff:
            return JsonResponse({'error': 'Staff access required'}, status=403)

        # Proceed to the view
        return view_func(self,request, *args, **kwargs)
    return _wrapped_view

def token_and_user_required(view_func):
    """
    A decorator to check if the user has a valid token.
    """
    @wraps(view_func)
    def _wrapped_view(self,request, args, **kwargs):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Token required'}, status=401)

        token_key = auth_header.split('Token ')[1]
        try:
            # Validate the token and get the associated user
            token = Token.objects.get(key=token_key)
            user = token.user  # Get the user linked to the token
            request.user = user  # Attach the user to the request object
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        # Proceed to the view
        return view_func(self,request,args, **kwargs)
    return _wrapped_view