from app import db
from app.models.base import BaseTextModel, BaseImageModel

class TeamText(BaseTextModel):
    __tablename__ = 'team_text'
    
    position = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        data = super().to_dict()
        data['position'] = self.position
        return data

class TeamImage(BaseImageModel):
    __tablename__ = 'team_images'
    
    member_id = db.Column(db.Integer, db.ForeignKey('team_text.id'), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['member_id'] = self.member_id
        return data 