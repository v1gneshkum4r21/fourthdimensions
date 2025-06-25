from flask_restx import fields
from app.api import api

# Base schemas
base_text_model = api.model('BaseText', {
    'id': fields.Integer(readonly=True, description='The unique identifier'),
    'title': fields.String(required=True, description='The title'),
    'content': fields.String(required=True, description='The content text')
})

base_text_response = api.inherit('BaseTextResponse', base_text_model, {
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

base_image_model = api.model('BaseImage', {
    'id': fields.Integer(readonly=True, description='The unique identifier'),
    'title': fields.String(required=True, description='The image title'),
    'description': fields.String(description='The image description')
})

base_image_response = api.inherit('BaseImageResponse', base_image_model, {
    'image_path': fields.String(readonly=True, description='Path to the image file'),
    'image_url': fields.String(readonly=True, description='Full URL to the image file'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

base_video_model = api.model('BaseVideo', {
    'id': fields.Integer(readonly=True, description='The unique identifier'),
    'title': fields.String(required=True, description='The video title'),
    'description': fields.String(description='The video description')
})

base_video_response = api.inherit('BaseVideoResponse', base_video_model, {
    'video_path': fields.String(readonly=True, description='Path to the video file'),
    'video_url': fields.String(readonly=True, description='Full URL to the video file'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

# Parser for file uploads
file_upload_parser = api.parser()
file_upload_parser.add_argument('title', type=str, required=True, help='Title for the file', location='form')
file_upload_parser.add_argument('description', type=str, help='Description for the file', location='form')
file_upload_parser.add_argument('file', type='file', required=True, help='The file to upload', location='files') 