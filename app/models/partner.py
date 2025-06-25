from app import db
from app.models.base import BaseImageModel

class PartnerImage(BaseImageModel):
    __tablename__ = 'partner_images'
    
    website_url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        data = super().to_dict()
        data['website_url'] = self.website_url
        return data 