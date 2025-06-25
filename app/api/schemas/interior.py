from flask_restx import fields
from app.api import api, ns_interior
from app.api.schemas.base import base_text_model, base_text_response, base_image_response, base_video_response, file_upload_parser

# Interior Category Text schemas
interior_category_text = api.inherit('InteriorCategoryText', base_text_model, {
    'category': fields.String(required=True, description='The interior category')
})
interior_category_text_response = api.inherit('InteriorCategoryTextResponse', base_text_response, {
    'category': fields.String(description='The interior category')
})

# Interior Gallery Image schemas
interior_gallery_image = api.inherit('InteriorGalleryImage', base_image_response, {
    'category': fields.String(required=True, description='The interior category')
})

# Interior Video schemas
interior_video = api.inherit('InteriorVideo', base_video_response, {
    'category': fields.String(description='The interior category')
})

# Interior Image upload parser
interior_image_parser = file_upload_parser.copy()
interior_image_parser.add_argument('category', type=str, required=True, help='Category for the image', location='form')

# Interior Video upload parser
interior_video_parser = file_upload_parser.copy()
interior_video_parser.add_argument('category', type=str, help='Category for the video', location='form') 