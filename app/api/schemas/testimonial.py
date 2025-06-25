from flask_restx import fields
from app.api import api, ns_testimonials
from app.api.schemas.base import base_text_model, base_text_response, base_video_response, file_upload_parser

# Testimonial Text schemas
testimonial_text = api.inherit('TestimonialText', base_text_model, {
    'author': fields.String(required=True, description='The author of the testimonial'),
    'company': fields.String(description='The company of the author')
})
testimonial_text_response = api.inherit('TestimonialTextResponse', base_text_response, {
    'author': fields.String(description='The author of the testimonial'),
    'company': fields.String(description='The company of the author')
})

# Testimonial Rating schemas
testimonial_rating = api.model('TestimonialRating', {
    'id': fields.Integer(readonly=True, description='The unique identifier'),
    'testimonial_id': fields.Integer(required=True, description='The testimonial ID'),
    'rating': fields.Float(required=True, description='The rating value (0-5)'),
    'category': fields.String(required=True, description='The rating category')
})
testimonial_rating_response = api.inherit('TestimonialRatingResponse', testimonial_rating, {
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

# Testimonial Video schemas
testimonial_video = api.inherit('TestimonialVideo', base_video_response, {
    'author': fields.String(required=True, description='The author of the testimonial'),
    'company': fields.String(description='The company of the author')
})

# Testimonial Video upload parser
testimonial_video_parser = file_upload_parser.copy()
testimonial_video_parser.add_argument('author', type=str, required=True, help='Author of the testimonial', location='form')
testimonial_video_parser.add_argument('company', type=str, help='Company of the author', location='form') 