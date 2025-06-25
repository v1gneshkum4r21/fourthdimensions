from app.api.schemas.base import (
    base_text_model, base_text_response,
    base_image_model, base_image_response,
    base_video_model, base_video_response,
    file_upload_parser
)
from app.api.schemas.hero import hero_text, hero_text_response, hero_video, hero_video_parser
from app.api.schemas.interior import (
    interior_category_text, interior_category_text_response,
    interior_gallery_image, interior_video,
    interior_image_parser, interior_video_parser
)
from app.api.schemas.construction import (
    construction_category_text, construction_category_text_response,
    construction_intro_image, construction_gallery_image, construction_video,
    construction_intro_image_parser, construction_gallery_image_parser, construction_video_parser
)
from app.api.schemas.testimonial import (
    testimonial_text, testimonial_text_response,
    testimonial_rating, testimonial_rating_response,
    testimonial_video, testimonial_video_parser
) 