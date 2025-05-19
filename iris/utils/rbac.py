from flask import abort, current_app, request
from flask_login import current_user
from functools import wraps


def role_required(role_name):
    """Decorator to require a specific role for a view"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            
            if not current_user.has_role(role_name):
                current_app.logger.warning(f"User {current_user.id} attempted to access {request.path} without required role: {role_name}")
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def permission_required(resource, action):
    """Decorator to require a specific permission for a view"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            
            if not current_user.has_permission(resource, action):
                current_app.logger.warning(f"User {current_user.id} attempted to access {request.path} without required permission: {resource}.{action}")
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role for a view"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        
        if not current_user.is_admin():
            current_app.logger.warning(f"User {current_user.id} attempted to access admin-only route {request.path}")
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


# Helper function to check permissions in templates
def can_user(user, resource, action):
    """Check if a user has permission to perform an action on a resource"""
    if user.is_admin():
        return True
    return user.has_permission(resource, action)
