from app import db
from app.models.base import BaseTextModel, BaseImageModel, BaseVideoModel

class ConstructionCategoryText(BaseTextModel):
    __tablename__ = 'construction_category_text'
    
    category = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data

class ConstructionIntroImage(BaseImageModel):
    __tablename__ = 'construction_intro_images'

class ConstructionGalleryImage(BaseImageModel):
    __tablename__ = 'construction_gallery_images'
    
    category = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data

class ConstructionVideo(BaseVideoModel):
    __tablename__ = 'construction_videos'
    
    category = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data 