from functools import wraps
from flask import request, g
from flask_restx import abort
from app.models.user import User
from werkzeug.security import check_password_hash

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            
        if not token:
            abort(401, 'Authentication token is missing')
            
        # Simple token validation (in a real app, use JWT or other secure method)
        if token != 'admin-token':
            abort(401, 'Invalid authentication token')
            
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # First check token
        token_required(lambda: None)()
        
        # Here you could add additional checks for admin role
        # For simplicity, we're just checking if the token is the admin token
        
        return f(*args, **kwargs)
    
    return decorated 