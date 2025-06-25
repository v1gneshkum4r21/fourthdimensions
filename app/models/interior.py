from app import db
from app.models.base import BaseTextModel, BaseImageModel, BaseVideoModel

class InteriorCategoryText(BaseTextModel):
    __tablename__ = 'interior_category_text'
    
    category = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data

class InteriorGalleryImage(BaseImageModel):
    __tablename__ = 'interior_gallery_images'
    
    category = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data

class InteriorVideo(BaseVideoModel):
    __tablename__ = 'interior_videos'
    
    category = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['category'] = self.category
        return data 