from app import db
from app.models.base import BaseTextModel, BaseVideoModel

class HeroText(BaseTextModel):
    __tablename__ = 'hero_text'
    
    # Additional fields specific to hero text can be added here

class HeroVideo(BaseVideoModel):
    __tablename__ = 'hero_videos'
    
    # Additional fields specific to hero videos can be added here 