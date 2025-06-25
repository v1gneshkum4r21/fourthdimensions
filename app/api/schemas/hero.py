from flask_restx import fields
from app.api import api, ns_hero
from app.api.schemas.base import base_text_model, base_text_response, base_video_response, file_upload_parser

# Hero Text schemas
hero_text = api.inherit('HeroText', base_text_model, {})
hero_text_response = api.inherit('HeroTextResponse', base_text_response, {})

# Hero Video schemas
hero_video = api.inherit('HeroVideo', base_video_response, {})

# Hero Video upload parser
hero_video_parser = file_upload_parser.copy() 