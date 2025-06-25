from app.api.resources.auth import token_required, admin_required
from app.api.resources.hero import HeroTextList, HeroTextItem, HeroVideoList, HeroVideoItem
from app.api.resources.interior import (
    InteriorCategoryTextList, InteriorCategoryTextItem,
    InteriorGalleryImageList, InteriorGalleryImageItem,
    InteriorVideoList, InteriorVideoItem
)
from app.api.resources.admin import AdminLogin, AdminDashboard 