from flask import request, jsonify
from flask_restx import Resource, fields
from app.api import ns_admin, api
from app.models.user import User
from werkzeug.security import check_password_hash
from app import db

login_model = ns_admin.model('Login', {
    'username': fields.String(required=True, description='Admin username'),
    'password': fields.String(required=True, description='Admin password')
})

@ns_admin.route('/login')
class AdminLogin(Resource):
    @ns_admin.doc('admin_login')
    @ns_admin.expect(login_model)
    def post(self):
        """Login to get admin access token"""
        data = request.json
        
        user = User.query.filter_by(username=data.get('username')).first()
        
        if not user or not check_password_hash(user.password, data.get('password')):
            return {'message': 'Invalid credentials'}, 401
        
        # In a real app, use JWT or other secure token method
        # For simplicity, we're returning a simple token
        return {
            'token': 'admin-token',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }

@ns_admin.route('/dashboard')
class AdminDashboard(Resource):
    @ns_admin.doc('admin_dashboard')
    def get(self):
        """Get admin dashboard stats"""
        # This would typically return stats about the content
        # For simplicity, we're just returning a placeholder
        return {
            'stats': {
                'total_images': 0,
                'total_videos': 0,
                'total_texts': 0
            }
        } 