from flask_restx import fields
from app.api import api, ns_construction
from app.api.schemas.base import base_text_model, base_text_response, base_image_response, base_video_response, file_upload_parser

# Construction Category Text schemas
construction_category_text = api.inherit('ConstructionCategoryText', base_text_model, {
    'category': fields.String(required=True, description='The construction category')
})
construction_category_text_response = api.inherit('ConstructionCategoryTextResponse', base_text_response, {
    'category': fields.String(description='The construction category')
})

# Construction Intro Image schemas
construction_intro_image = api.inherit('ConstructionIntroImage', base_image_response, {})

# Construction Gallery Image schemas
construction_gallery_image = api.inherit('ConstructionGalleryImage', base_image_response, {
    'category': fields.String(required=True, description='The construction category')
})

# Construction Video schemas
construction_video = api.inherit('ConstructionVideo', base_video_response, {
    'category': fields.String(description='The construction category')
})

# Construction Intro Image upload parser
construction_intro_image_parser = file_upload_parser.copy()

# Construction Gallery Image upload parser
construction_gallery_image_parser = file_upload_parser.copy()
construction_gallery_image_parser.add_argument('category', type=str, required=True, help='Category for the image', location='form')

# Construction Video upload parser
construction_video_parser = file_upload_parser.copy()
construction_video_parser.add_argument('category', type=str, help='Category for the video', location='form') 