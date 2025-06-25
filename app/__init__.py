from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask_admin import Admin
from flask_login import LoginManager
from flask_babel import Babel
import os
import sqlite3

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fourth_dimensions.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER_IMAGES'] = os.path.join(app.static_folder, 'uploads/images')
    app.config['UPLOAD_FOLDER_VIDEOS'] = os.path.join(app.static_folder, 'uploads/videos')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    
    # Flask-Admin configuration
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_VIDEOS'], exist_ok=True)
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    babel.init_app(app)
    
    # Register API blueprint
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize admin
    from app.admin.views import MyAdminIndexView
    admin = Admin(
        app, 
        name='Fourth Dimensions Admin', 
        template_mode='bootstrap3',
        index_view=MyAdminIndexView(),
        base_template='admin/master.html'
    )
    
    # Register admin views
    from app.admin.views import register_admin_views
    register_admin_views(admin, db)
    
    # Check if we need to add the last_login column to the User table
    with app.app_context():
        try:
            # Try to update the database schema if needed
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'fourth_dimensions.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if the last_login column exists
            cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'last_login' not in columns:
                print("Adding last_login column to user table...")
                cursor.execute("ALTER TABLE user ADD COLUMN last_login TIMESTAMP")
                conn.commit()
                print("Column added successfully.")
            
            conn.close()
            
            # Now create tables for any new models
            db.create_all()
            
            # Create admin user if it doesn't exist
            from app.models.user import User
            if not User.query.filter_by(username='admin').first():
                from werkzeug.security import generate_password_hash
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    password=generate_password_hash('admin')
                )
                db.session.add(admin_user)
                db.session.commit()
        except Exception as e:
            print(f"Error updating database schema: {str(e)}")
    
    # Add a route to demonstrate media rendering
    @app.route('/media-example')
    def media_example():
        from app.models.hero import HeroVideo
        from app.models.interior import InteriorGalleryImage
        
        images = InteriorGalleryImage.query.all()
        videos = HeroVideo.query.all()
        
        return render_template('media_example.html', images=images, videos=videos)
    
    return app 