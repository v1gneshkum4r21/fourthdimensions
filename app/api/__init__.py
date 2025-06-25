from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    version='1.0',
    title='Fourth Dimensions API',
    description='API for Fourth Dimensions website content management',
    doc='/docs',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    security='apikey'
)

# Create namespaces for different sections
ns_hero = api.namespace('hero', description='Hero section operations')
ns_interior = api.namespace('interior', description='Interior section operations')
ns_construction = api.namespace('construction', description='Construction section operations')
ns_about = api.namespace('about', description='About us section operations')
ns_team = api.namespace('team', description='Team section operations')
ns_testimonials = api.namespace('testimonials', description='Testimonials section operations')
ns_partners = api.namespace('partners', description='Partners section operations')
ns_why_us = api.namespace('why-us', description='Why Us section operations')
ns_admin = api.namespace('admin', description='Admin panel operations')

# Import all resources
from app.api.resources import * 