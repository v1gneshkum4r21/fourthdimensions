from app import db
from app.models.base import BaseModel, BaseImageModel

class AboutBadge(BaseModel):
    __tablename__ = 'about_badges'
    
    title = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AboutImage(BaseImageModel):
    __tablename__ = 'about_images' 