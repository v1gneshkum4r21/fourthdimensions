from app import db
from app.models.base import BaseTextModel, BaseVideoModel

class TestimonialText(BaseTextModel):
    __tablename__ = 'testimonial_text'
    
    author = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author
        data['company'] = self.company
        return data

class TestimonialRating(db.Model):
    __tablename__ = 'testimonial_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    testimonial_id = db.Column(db.Integer, db.ForeignKey('testimonial_text.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'testimonial_id': self.testimonial_id,
            'rating': self.rating,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TestimonialVideo(BaseVideoModel):
    __tablename__ = 'testimonial_videos'
    
    author = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['author'] = self.author
        data['company'] = self.company
        return data 