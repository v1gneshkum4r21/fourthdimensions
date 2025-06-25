from app import db
from datetime import datetime
from flask import url_for

def normalize_path(path):
    """Normalize path to use forward slashes even on Windows"""
    if path:
        return path.replace('\\', '/')
    return path

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BaseTextModel(BaseModel):
    __abstract__ = True
    
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class BaseImageModel(BaseModel):
    __abstract__ = True
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        image_url = None
        if self.image_path:
            normalized_path = normalize_path(self.image_path)
            image_url = url_for('static', filename=normalized_path, _external=True)
            
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_path': self.image_path,
            'image_url': image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class BaseVideoModel(BaseModel):
    __abstract__ = True
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_path = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        video_url = None
        if self.video_path:
            normalized_path = normalize_path(self.video_path)
            video_url = url_for('static', filename=normalized_path, _external=True)
            
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_path': self.video_path,
            'video_url': video_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 