from flask import redirect, url_for, request, Markup, flash, jsonify
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, ImageUploadField, Select2Field
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from wtforms import ValidationError, StringField, Form, validators
import traceback
import logging
import sys
from app import db
from app.models import *
from app.utils.file_helpers import allowed_image_file, allowed_video_file, save_image, save_video, delete_file
from app.utils.category_helpers import get_all_categories_for_model, create_category, delete_category, get_section_for_model

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)

# Custom base view with authentication
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login', next=request.url))

# Base class for unified section views
class UnifiedSectionView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login', next=request.url))
    
    def __init__(self, name, category, models_dict, session, **kwargs):
        """
        Initialize the unified section view
        
        Args:
            name: Name of the section
            category: Category for the admin menu
            models_dict: Dictionary of model classes for this section
                         e.g. {'text': TextModel, 'image': ImageModel, 'video': VideoModel}
            session: SQLAlchemy session
        """
        super().__init__(name=name, category=category, **kwargs)
        self.models_dict = models_dict
        self.session = session
    
    def get_view_name(self, model_class):
        """Get the view name for a model class"""
        # Convert the class name to lowercase without adding 'view' suffix
        view_name = model_class.__name__.lower()
        
        # Return the view name
        return view_name
        
    @expose('/')
    def index(self):
        """Show the section dashboard with all content types"""
        # Get counts for each content type
        counts = {}
        items = {}
        view_names = {}
        
        for content_type, model_class in self.models_dict.items():
            # Get count
            counts[content_type] = self.session.query(db.func.count(model_class.id)).scalar()
            
            # Get recent items (up to 5)
            recent = self.session.query(model_class).order_by(model_class.created_at.desc()).limit(5).all()
            items[content_type] = recent
            
            # Get view name
            view_names[content_type] = self.get_view_name(model_class)
        
        return self.render('admin/section_index.html', 
                          section_name=self.name,
                          counts=counts,
                          items=items,
                          models=self.models_dict,
                          view_names=view_names)
    
    @expose('/create/<content_type>', methods=['GET', 'POST'])
    def create(self, content_type):
        """Create a new content item"""
        if content_type not in self.models_dict:
            flash(f'Invalid content type: {content_type}', 'error')
            return redirect(url_for('.index'))
        
        model_class = self.models_dict[content_type]
        view_name = self.get_view_name(model_class)
        
        # Redirect to the appropriate create view
        return redirect(url_for(f'{view_name}.create_view'))
    
    @expose('/edit/<content_type>/<int:id>', methods=['GET', 'POST'])
    def edit(self, content_type, id):
        """Edit an existing content item"""
        if content_type not in self.models_dict:
            flash(f'Invalid content type: {content_type}', 'error')
            return redirect(url_for('.index'))
        
        model_class = self.models_dict[content_type]
        view_name = self.get_view_name(model_class)
        
        # Redirect to the appropriate edit view
        return redirect(url_for(f'{view_name}.edit_view', id=id))
    
    @expose('/delete/<content_type>/<int:id>', methods=['GET', 'POST'])
    def delete(self, content_type, id):
        """Delete a content item"""
        if content_type not in self.models_dict:
            flash(f'Invalid content type: {content_type}', 'error')
            return redirect(url_for('.index'))
        
        model_class = self.models_dict[content_type]
        view_name = self.get_view_name(model_class)
        
        if request.method == 'POST':
            # Handle the deletion directly
            item = self.session.query(model_class).get(id)
            if item:
                try:
                    # Handle file deletion if it's an image or video
                    if hasattr(item, 'image_path') and item.image_path:
                        delete_file(item.image_path)
                    if hasattr(item, 'video_path') and item.video_path:
                        delete_file(item.video_path)
                    
                    # Delete the database record
                    self.session.delete(item)
                    self.session.commit()
                    flash(f'{content_type.capitalize()} item was successfully deleted.', 'success')
                except Exception as ex:
                    self.session.rollback()
                    flash(f'Failed to delete {content_type} item. Error: {str(ex)}', 'error')
            else:
                flash(f'{content_type.capitalize()} item with ID {id} not found.', 'error')
            
            return redirect(url_for('.index'))
        else:
            # Redirect to the appropriate delete view for GET requests
            return redirect(url_for(f'{view_name}.delete_view', id=id))

# Base class for models with categories
class CategoryModelView(SecureModelView):
    form_excluded_columns = ['created_at', 'updated_at']
    
    def create_form(self):
        form = super().create_form()
        if hasattr(form, 'category'):
            model_class = self.model
            categories = get_all_categories_for_model(model_class)
            form.category.choices = categories
        elif hasattr(form, 'service_type'):
            form.service_type.choices = get_all_categories_for_model(self.model)
            # Do not set a default category
        return form
    
    def edit_form(self, obj):
        form = super().edit_form(obj)
        if hasattr(form, 'category'):
            model_class = self.model
            categories = get_all_categories_for_model(model_class)
            form.category.choices = categories
        elif hasattr(form, 'service_type'):
            form.service_type.choices = get_all_categories_for_model(self.model)
        return form
    
    def scaffold_form(self):
        form_class = super().scaffold_form()
        
        # Check if the model has category or service_type field
        model_columns = [column.key for column in self.model.__table__.columns]
        
        if 'category' in model_columns:
            form_class.category = Select2Field('Category', choices=[])
        if 'service_type' in model_columns:
            form_class.service_type = Select2Field('Service Type', choices=[])
            
        return form_class
        
    def validate_form(self, form):
        """Override validate_form to check if a category is selected"""
        if hasattr(form, 'category') and not form.category.data:
            flash('Please create a category first before adding content.', 'error')
            return False
        elif hasattr(form, 'service_type') and not form.service_type.data:
            flash('Please create a service type first before adding content.', 'error')
            return False
        return super().validate_form(form)

# Base class for image uploads
class ImageUploadView(SecureModelView):
    form_excluded_columns = ['created_at', 'updated_at']
    
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''
        return Markup(f'<img src="{url_for("static", filename=model.image_path)}" width="100">')
    
    column_formatters = {
        'image_path': _list_thumbnail
    }
    
    def create_model(self, form):
        """Override create_model to add better error handling"""
        try:
            # Process the form data
            model = self.model()
            form.populate_obj(model)
            
            # Handle file upload
            file_obj = request.files.get('image')
            if file_obj and file_obj.filename:
                result = save_image(file_obj)
                if result:
                    model.image_path = result['file_path']
                else:
                    flash('Failed to save image. Make sure it is a valid image file.', 'error')
                    return False
            else:
                flash('Image file is required for new records.', 'error')
                return False
            
            # Save the model
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'Failed to create record. Error: {str(ex)}', 'error')
            print(f"Error creating image record: {str(ex)}")
            traceback.print_exc()
            return False
    
    def update_model(self, form, model):
        """Override update_model to add better error handling"""
        try:
            form.populate_obj(model)
            
            # Handle file upload
            file_obj = request.files.get('image')
            if file_obj and file_obj.filename:
                result = save_image(file_obj)
                if result:
                    # Delete old file if it exists
                    if model.image_path:
                        delete_file(model.image_path)
                    model.image_path = result['file_path']
                else:
                    flash('Failed to save image. Make sure it is a valid image file.', 'error')
                    return False
            
            self._on_model_change(form, model, False)
            self.session.commit()
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'Failed to update record. Error: {str(ex)}', 'error')
            print(f"Error updating image record: {str(ex)}")
            traceback.print_exc()
            return False
    
    def delete_model(self, model):
        """Override delete_model to delete the associated file"""
        try:
            # Delete the file first
            if model.image_path:
                logger.info(f"Deleting file: {model.image_path}")
                delete_file(model.image_path)
            
            # Then delete the database record
            self.session.delete(model)
            self.session.commit()
            flash('Record and associated file were successfully deleted.', 'success')
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'Failed to delete record. Error: {str(ex)}', 'error')
            logger.exception(f"Error deleting image record: {str(ex)}")
            return False
    
    # Override these properties instead of using methods
    create_template = 'admin/image_create.html'
    edit_template = 'admin/image_edit.html'

# Base class for image uploads with categories
class CategoryImageUploadView(ImageUploadView, CategoryModelView):
    # Override create_template and edit_template to use our custom templates
    create_template = 'admin/image_create.html'
    edit_template = 'admin/image_edit.html'
    
    def create_form(self):
        """Override to ensure categories are loaded"""
        form = super().create_form()
        if hasattr(form, 'category'):
            model_class = self.model
            categories = get_all_categories_for_model(model_class)
            form.category.choices = categories
        return form
    
    def edit_form(self, obj):
        """Override to ensure categories are loaded"""
        form = super().edit_form(obj)
        if hasattr(form, 'category'):
            model_class = self.model
            categories = get_all_categories_for_model(model_class)
            form.category.choices = categories
        return form

# Base class for video uploads
class VideoUploadView(SecureModelView):
    form_excluded_columns = ['created_at', 'updated_at']
    
    def _list_video_link(view, context, model, name):
        if not model.video_path:
            return ''
        return Markup(f'<a href="{url_for("static", filename=model.video_path)}" target="_blank" class="btn btn-xs btn-info">View Video</a>')
    
    column_formatters = {
        'video_path': _list_video_link
    }
    
    def create_model(self, form):
        """Override create_model to add better error handling"""
        try:
            # Log the form data
            logger.debug("Form data: %s", form.data)
            
            # Process the form data
            model = self.model()
            form.populate_obj(model)
            
            # Log the model data
            logger.debug("Model after populate_obj: %s", vars(model))
            
            # Log request files
            logger.debug("Request files: %s", request.files)
            
            # Handle file upload
            file_obj = request.files.get('video')
            if file_obj and file_obj.filename:
                logger.debug("File object found: %s", file_obj.filename)
                
                # Check if file is allowed
                if not allowed_video_file(file_obj.filename):
                    logger.error("File type not allowed: %s", file_obj.filename)
                    flash(f'File type not allowed: {file_obj.filename}. Allowed types: mp4, webm, ogg, mov', 'error')
                    return False
                
                result = save_video(file_obj)
                logger.debug("Save video result: %s", result)
                
                if result:
                    model.video_path = result['file_path']
                    logger.debug("Set model.video_path to: %s", result['file_path'])
                else:
                    logger.error("Failed to save video")
                    flash('Failed to save video. Make sure it is a valid video file.', 'error')
                    return False
            else:
                logger.error("No video file provided")
                flash('Video file is required for new records.', 'error')
                return False
            
            # Save the model
            logger.debug("Adding model to session")
            self.session.add(model)
            
            logger.debug("Calling _on_model_change")
            self._on_model_change(form, model, True)
            
            logger.debug("Committing session")
            self.session.commit()
            
            logger.info("Successfully created record")
            flash('Record was successfully created.', 'success')
            return True
        except Exception as ex:
            logger.exception("Error creating video record")
            self.session.rollback()
            flash(f'Failed to create record. Error: {str(ex)}', 'error')
            return False
    
    def update_model(self, form, model):
        """Override update_model to add better error handling"""
        try:
            # Log the form data
            logger.debug("Form data: %s", form.data)
            
            form.populate_obj(model)
            
            # Log the model data
            logger.debug("Model after populate_obj: %s", vars(model))
            
            # Log request files
            logger.debug("Request files: %s", request.files)
            
            # Handle file upload
            file_obj = request.files.get('video')
            if file_obj and file_obj.filename:
                logger.debug("File object found: %s", file_obj.filename)
                
                # Check if file is allowed
                if not allowed_video_file(file_obj.filename):
                    logger.error("File type not allowed: %s", file_obj.filename)
                    flash(f'File type not allowed: {file_obj.filename}. Allowed types: mp4, webm, ogg, mov', 'error')
                    return False
                
                result = save_video(file_obj)
                logger.debug("Save video result: %s", result)
                
                if result:
                    # Delete old file if it exists
                    if model.video_path:
                        logger.debug("Deleting old file: %s", model.video_path)
                        delete_file(model.video_path)
                    
                    model.video_path = result['file_path']
                    logger.debug("Set model.video_path to: %s", result['file_path'])
                else:
                    logger.error("Failed to save video")
                    flash('Failed to save video. Make sure it is a valid video file.', 'error')
                    return False
            
            logger.debug("Calling _on_model_change")
            self._on_model_change(form, model, False)
            
            logger.debug("Committing session")
            self.session.commit()
            
            logger.info("Successfully updated record")
            flash('Record was successfully updated.', 'success')
            return True
        except Exception as ex:
            logger.exception("Error updating video record")
            self.session.rollback()
            flash(f'Failed to update record. Error: {str(ex)}', 'error')
            return False
    
    def delete_model(self, model):
        """Override delete_model to delete the associated file"""
        try:
            # Delete the file first
            if model.video_path:
                logger.info(f"Deleting file: {model.video_path}")
                delete_file(model.video_path)
            
            # Then delete the database record
            self.session.delete(model)
            self.session.commit()
            flash('Record and associated file were successfully deleted.', 'success')
            return True
        except Exception as ex:
            self.session.rollback()
            flash(f'Failed to delete record. Error: {str(ex)}', 'error')
            logger.exception(f"Error deleting video record: {str(ex)}")
            return False
    
    # Override these properties instead of using methods
    create_template = 'admin/video_create.html'
    edit_template = 'admin/video_edit.html'

# Base class for video uploads with categories
class CategoryVideoUploadView(VideoUploadView, CategoryModelView):
    pass

# Custom index view with login/logout
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login'))
        
        # Get counts for dashboard
        image_count = db.session.query(db.func.count(AboutImage.id)).scalar()
        image_count += db.session.query(db.func.count(ConstructionGalleryImage.id)).scalar()
        image_count += db.session.query(db.func.count(ConstructionIntroImage.id)).scalar()
        image_count += db.session.query(db.func.count(InteriorGalleryImage.id)).scalar()
        image_count += db.session.query(db.func.count(PartnerImage.id)).scalar()
        image_count += db.session.query(db.func.count(TeamImage.id)).scalar()
        image_count += db.session.query(db.func.count(WhyUsImage.id)).scalar()
        
        video_count = db.session.query(db.func.count(ConstructionVideo.id)).scalar()
        video_count += db.session.query(db.func.count(HeroVideo.id)).scalar()
        video_count += db.session.query(db.func.count(InteriorVideo.id)).scalar()
        video_count += db.session.query(db.func.count(TestimonialVideo.id)).scalar()
        
        text_count = db.session.query(db.func.count(AboutBadge.id)).scalar()
        text_count += db.session.query(db.func.count(ConstructionCategoryText.id)).scalar()
        text_count += db.session.query(db.func.count(HeroText.id)).scalar()
        text_count += db.session.query(db.func.count(InteriorCategoryText.id)).scalar()
        text_count += db.session.query(db.func.count(TeamText.id)).scalar()
        text_count += db.session.query(db.func.count(TestimonialRating.id)).scalar()
        text_count += db.session.query(db.func.count(TestimonialText.id)).scalar()
        
        user_count = db.session.query(db.func.count(User.id)).scalar()
        
        # Get recent items
        recent_items = []
        
        # Get recent images
        recent_images = (
            db.session.query(
                AboutImage.id, 
                AboutImage.title, 
                AboutImage.created_at
            ).order_by(AboutImage.created_at.desc()).limit(3).all()
        )
        for item in recent_images:
            recent_items.append({
                'id': item.id,
                'title': item.title,
                'created_at': item.created_at,
                'type': 'image'
            })
        
        # Get recent videos
        recent_videos = (
            db.session.query(
                HeroVideo.id, 
                HeroVideo.title, 
                HeroVideo.created_at
            ).order_by(HeroVideo.created_at.desc()).limit(3).all()
        )
        for item in recent_videos:
            recent_items.append({
                'id': item.id,
                'title': item.title,
                'created_at': item.created_at,
                'type': 'video'
            })
        
        # Get recent text
        recent_text = (
            db.session.query(
                HeroText.id, 
                HeroText.title, 
                HeroText.created_at
            ).order_by(HeroText.created_at.desc()).limit(3).all()
        )
        for item in recent_text:
            recent_items.append({
                'id': item.id,
                'title': item.title,
                'created_at': item.created_at,
                'type': 'text'
            })
        
        # Sort by created_at
        recent_items.sort(key=lambda x: x['created_at'], reverse=True)
        recent_items = recent_items[:5]  # Limit to 5 most recent
        
        return self.render('admin/index.html', 
                          image_count=image_count,
                          video_count=video_count,
                          text_count=text_count,
                          user_count=user_count,
                          recent_items=recent_items)
    
    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                
                # Update last login time
                from datetime import datetime
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                flash('Login successful!', 'success')
                return redirect(url_for('.index'))
            else:
                flash('Invalid username or password!', 'error')
        
        return self.render('admin/login.html')
    
    @expose('/logout')
    def logout(self):
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('.login'))

# Model views for each model
class HeroTextView(SecureModelView):
    column_searchable_list = ['title', 'content']
    column_filters = ['title']
    form_excluded_columns = ['created_at', 'updated_at']

class HeroVideoView(VideoUploadView):
    column_searchable_list = ['title', 'description']
    column_filters = ['title']
    column_list = ['id', 'title', 'description', 'video_path', 'created_at', 'updated_at']
    
class InteriorCategoryTextView(CategoryModelView):
    column_searchable_list = ['title', 'content', 'category']
    column_filters = ['title', 'category']
    form_excluded_columns = ['created_at', 'updated_at']
    
    # Use custom templates for better category handling
    create_template = 'admin/category_text_create.html'
    edit_template = 'admin/category_text_edit.html'

class InteriorGalleryImageView(CategoryImageUploadView):
    column_searchable_list = ['title', 'description', 'category']
    column_filters = ['title', 'category']
    column_list = ['id', 'title', 'description', 'category', 'image_path', 'created_at', 'updated_at']

class InteriorVideoView(CategoryVideoUploadView):
    column_searchable_list = ['title', 'description', 'category']
    column_filters = ['title', 'category']
    column_list = ['id', 'title', 'description', 'category', 'video_path', 'created_at', 'updated_at']

class ConstructionCategoryTextView(CategoryModelView):
    column_searchable_list = ['title', 'content', 'category']
    column_filters = ['title', 'category']
    form_excluded_columns = ['created_at', 'updated_at']
    
    # Use custom templates for better category handling
    create_template = 'admin/category_text_create.html'
    edit_template = 'admin/category_text_edit.html'

class ConstructionIntroImageView(ImageUploadView):
    column_searchable_list = ['title', 'description']
    column_filters = ['title']
    column_list = ['id', 'title', 'description', 'image_path', 'created_at', 'updated_at']

class ConstructionGalleryImageView(CategoryImageUploadView):
    column_searchable_list = ['title', 'description', 'category']
    column_filters = ['title', 'category']
    column_list = ['id', 'title', 'description', 'category', 'image_path', 'created_at', 'updated_at']

class ConstructionVideoView(CategoryVideoUploadView):
    column_searchable_list = ['title', 'description', 'category']
    column_filters = ['title', 'category']
    column_list = ['id', 'title', 'description', 'category', 'video_path', 'created_at', 'updated_at']

class AboutBadgeView(SecureModelView):
    column_searchable_list = ['title', 'value', 'description']
    column_filters = ['title']
    form_excluded_columns = ['created_at', 'updated_at']

class AboutImageView(ImageUploadView):
    column_searchable_list = ['title', 'description']
    column_filters = ['title']
    column_list = ['id', 'title', 'description', 'image_path', 'created_at', 'updated_at']

class TeamTextView(SecureModelView):
    column_searchable_list = ['title', 'content', 'position']
    column_filters = ['title', 'position']
    form_excluded_columns = ['created_at', 'updated_at']

class TeamImageView(ImageUploadView):
    column_searchable_list = ['title', 'description']
    column_filters = ['title', 'member_id']
    column_list = ['id', 'title', 'description', 'member_id', 'image_path', 'created_at', 'updated_at']

class TestimonialTextView(SecureModelView):
    column_searchable_list = ['title', 'content', 'author', 'company']
    column_filters = ['title', 'author', 'company']
    form_excluded_columns = ['created_at', 'updated_at']

class TestimonialRatingView(SecureModelView):
    column_searchable_list = ['category']
    column_filters = ['testimonial_id', 'rating', 'category']
    form_excluded_columns = ['created_at', 'updated_at']

class TestimonialVideoView(VideoUploadView):
    column_searchable_list = ['title', 'description', 'author', 'company']
    column_filters = ['title', 'author', 'company']
    column_list = ['id', 'title', 'description', 'author', 'company', 'video_path', 'created_at', 'updated_at']

class PartnerImageView(ImageUploadView):
    column_searchable_list = ['title', 'description', 'website_url']
    column_filters = ['title']
    column_list = ['id', 'title', 'description', 'website_url', 'image_path', 'created_at', 'updated_at']

class WhyUsImageView(ImageUploadView):
    column_searchable_list = ['title', 'description']
    column_filters = ['title']
    column_list = ['id', 'title', 'description', 'image_path', 'created_at', 'updated_at']

class UserView(SecureModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['username', 'email']
    form_excluded_columns = ['password', 'created_at']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            from werkzeug.security import generate_password_hash
            model.password = generate_password_hash('admin')  # Default password for new users

# Unified section views
class HeroSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'text': HeroText,
            'video': HeroVideo
        }
        super().__init__(name='Hero', category='Content', models_dict=models, session=session)

class InteriorSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'text': InteriorCategoryText,
            'image': InteriorGalleryImage,
            'video': InteriorVideo
        }
        super().__init__(name='Interior', category='Content', models_dict=models, session=session)

class ConstructionSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'text': ConstructionCategoryText,
            'intro_image': ConstructionIntroImage,
            'gallery_image': ConstructionGalleryImage,
            'video': ConstructionVideo
        }
        super().__init__(name='Construction', category='Content', models_dict=models, session=session)

class AboutSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'badge': AboutBadge,
            'image': AboutImage
        }
        super().__init__(name='About', category='Content', models_dict=models, session=session)

class TeamSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'text': TeamText,
            'image': TeamImage
        }
        super().__init__(name='Team', category='Content', models_dict=models, session=session)

class TestimonialSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'text': TestimonialText,
            'rating': TestimonialRating,
            'video': TestimonialVideo
        }
        super().__init__(name='Testimonials', category='Content', models_dict=models, session=session)

class PartnerSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'image': PartnerImage
        }
        super().__init__(name='Partners', category='Content', models_dict=models, session=session)

class WhyUsSectionView(UnifiedSectionView):
    def __init__(self, session):
        models = {
            'image': WhyUsImage
        }
        super().__init__(name='Why Us', category='Content', models_dict=models, session=session)

# Category manager view
class CategoryManagerView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login', next=request.url))
    
    @expose('/')
    def index(self):
        """Show the category manager dashboard"""
        # Get all model classes with categories
        category_models = {
            'interior': {
                'text': InteriorCategoryText,
                'image': InteriorGalleryImage,
                'video': InteriorVideo
            },
            'construction': {
                'text': ConstructionCategoryText,
                'image': ConstructionGalleryImage,
                'video': ConstructionVideo
            }
        }
        
        # Get categories for each section
        categories = {}
        for section, models in category_models.items():
            # Use the first model to get categories
            model_class = list(models.values())[0]
            categories[section] = get_all_categories_for_model(model_class)
        
        return self.render('admin/category_manager.html', 
                          categories=categories,
                          category_models=category_models)
    
    @expose('/create/<section>/<content_type>', methods=['POST'])
    def create_category(self, section, content_type):
        """Create a new category"""
        if not current_user.is_authenticated:
            return jsonify(success=False, message="Authentication required"), 401
        
        category_name = request.form.get('category_name')
        if not category_name:
            return jsonify(success=False, message="Category name is required"), 400
        
        # Get the model class
        model_class = None
        if section == 'interior':
            if content_type == 'text':
                model_class = InteriorCategoryText
            elif content_type == 'image':
                model_class = InteriorGalleryImage
            elif content_type == 'video':
                model_class = InteriorVideo
        elif section == 'construction':
            if content_type == 'text':
                model_class = ConstructionCategoryText
            elif content_type == 'image':
                model_class = ConstructionGalleryImage
            elif content_type == 'video':
                model_class = ConstructionVideo
        
        if not model_class:
            return jsonify(success=False, message=f"Invalid section or content type: {section}/{content_type}"), 400
        
        # Create the category
        success, message = create_category(model_class, category_name)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=success, message=message)
        else:
            if success:
                flash(message, 'success')
            else:
                flash(message, 'error')
            return redirect(url_for('.index'))
    
    @expose('/delete/<section>/<content_type>/<category>', methods=['POST'])
    def delete_category(self, section, content_type, category):
        """Delete a category"""
        if not current_user.is_authenticated:
            return jsonify(success=False, message="Authentication required"), 401
        
        # Get the model class
        model_class = None
        if section == 'interior':
            if content_type == 'text':
                model_class = InteriorCategoryText
            elif content_type == 'image':
                model_class = InteriorGalleryImage
            elif content_type == 'video':
                model_class = InteriorVideo
        elif section == 'construction':
            if content_type == 'text':
                model_class = ConstructionCategoryText
            elif content_type == 'image':
                model_class = ConstructionGalleryImage
            elif content_type == 'video':
                model_class = ConstructionVideo
        
        if not model_class:
            return jsonify(success=False, message=f"Invalid section or content type: {section}/{content_type}"), 400
        
        # Delete the category
        success, message = delete_category(model_class, category)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=success, message=message)
        else:
            if success:
                flash(message, 'success')
            else:
                flash(message, 'error')
            return redirect(url_for('.index'))

def register_admin_views(admin_instance, db_instance):
    """Register all admin views"""
    # Register unified section views
    admin_instance.add_view(HeroSectionView(db_instance.session))
    admin_instance.add_view(InteriorSectionView(db_instance.session))
    admin_instance.add_view(ConstructionSectionView(db_instance.session))
    admin_instance.add_view(AboutSectionView(db_instance.session))
    admin_instance.add_view(TeamSectionView(db_instance.session))
    admin_instance.add_view(TestimonialSectionView(db_instance.session))
    admin_instance.add_view(PartnerSectionView(db_instance.session))
    admin_instance.add_view(WhyUsSectionView(db_instance.session))
    
    # Register category manager
    admin_instance.add_view(CategoryManagerView(name='Categories', category='Admin'))
    
    # Register individual model views under their respective section categories
    admin_instance.add_view(HeroTextView(HeroText, db_instance.session, category='Hero'))
    admin_instance.add_view(HeroVideoView(HeroVideo, db_instance.session, category='Hero'))
    
    admin_instance.add_view(InteriorCategoryTextView(InteriorCategoryText, db_instance.session, category='Interior'))
    admin_instance.add_view(InteriorGalleryImageView(InteriorGalleryImage, db_instance.session, category='Interior'))
    admin_instance.add_view(InteriorVideoView(InteriorVideo, db_instance.session, category='Interior'))
    
    admin_instance.add_view(ConstructionCategoryTextView(ConstructionCategoryText, db_instance.session, category='Construction'))
    admin_instance.add_view(ConstructionIntroImageView(ConstructionIntroImage, db_instance.session, category='Construction'))
    admin_instance.add_view(ConstructionGalleryImageView(ConstructionGalleryImage, db_instance.session, category='Construction'))
    admin_instance.add_view(ConstructionVideoView(ConstructionVideo, db_instance.session, category='Construction'))
    
    admin_instance.add_view(AboutBadgeView(AboutBadge, db_instance.session, category='About'))
    admin_instance.add_view(AboutImageView(AboutImage, db_instance.session, category='About'))
    
    admin_instance.add_view(TeamTextView(TeamText, db_instance.session, category='Team'))
    admin_instance.add_view(TeamImageView(TeamImage, db_instance.session, category='Team'))
    
    admin_instance.add_view(TestimonialTextView(TestimonialText, db_instance.session, category='Testimonials'))
    admin_instance.add_view(TestimonialRatingView(TestimonialRating, db_instance.session, category='Testimonials'))
    admin_instance.add_view(TestimonialVideoView(TestimonialVideo, db_instance.session, category='Testimonials'))
    
    admin_instance.add_view(PartnerImageView(PartnerImage, db_instance.session, category='Partners'))
    
    admin_instance.add_view(WhyUsImageView(WhyUsImage, db_instance.session, category='Why Us'))
    
    admin_instance.add_view(UserView(User, db_instance.session, category='Admin')) 