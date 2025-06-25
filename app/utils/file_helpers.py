import os
import uuid
import logging
from werkzeug.utils import secure_filename
from flask import current_app, url_for, request

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov'}

def allowed_image_file(filename):
    if '.' not in filename:
        logger.warning(f"No file extension in filename: {filename}")
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    result = ext in ALLOWED_IMAGE_EXTENSIONS
    if not result:
        logger.warning(f"File extension not allowed: {ext}")
    return result

def allowed_video_file(filename):
    if '.' not in filename:
        logger.warning(f"No file extension in filename: {filename}")
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    result = ext in ALLOWED_VIDEO_EXTENSIONS
    if not result:
        logger.warning(f"File extension not allowed: {ext}")
    return result

def get_file_url(file_path):
    """Get the full URL for a file path"""
    if file_path and file_path.startswith('uploads/'):
        return url_for('static', filename=file_path, _external=True)
    return file_path

def normalize_path(path):
    """Normalize path to use forward slashes even on Windows"""
    return path.replace('\\', '/')

def handle_admin_file_upload(file_data, file_type='image'):
    """Handle file upload from Flask-Admin's FileUploadField
    
    Args:
        file_data: The FileStorage object from the form
        file_type: 'image' or 'video'
        
    Returns:
        The relative path to the saved file or None if failed
    """
    if file_type == 'image':
        return save_image(file_data)
    elif file_type == 'video':
        return save_video(file_data)
    return None

def save_image(file):
    """Save an uploaded image file
    
    Args:
        file: The FileStorage object from the form
        
    Returns:
        Dict with file_path and url_path or None if failed
    """
    try:
        if not file:
            logger.error("No file provided to save_image")
            return None
            
        if not hasattr(file, 'filename') or not file.filename:
            logger.error("File has no filename")
            return None
            
        logger.debug(f"Processing image file: {file.filename}")
        
        if not allowed_image_file(file.filename):
            logger.error(f"Invalid image format: {file.filename}")
            return None
            
        filename = secure_filename(file.filename)
        logger.debug(f"Secured filename: {filename}")
        
        # Generate a unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        logger.debug(f"Generated unique filename: {unique_filename}")
        
        # Ensure upload directory exists
        upload_folder = current_app.config.get('UPLOAD_FOLDER_IMAGES')
        if not upload_folder:
            logger.error("UPLOAD_FOLDER_IMAGES not configured")
            return None
            
        os.makedirs(upload_folder, exist_ok=True)
        logger.debug(f"Ensured upload directory exists: {upload_folder}")
        
        file_path = os.path.join(upload_folder, unique_filename)
        logger.debug(f"Saving file to: {file_path}")
        
        file.save(file_path)
        logger.debug(f"File saved successfully")
        
        # Return the relative path for database storage - use forward slashes
        relative_path = normalize_path(os.path.join('uploads/images', unique_filename))
        # Generate a URL path that can be used directly in templates
        url_path = url_for('static', filename=relative_path, _external=True)
        
        logger.info(f"Successfully saved image: {relative_path}")
        
        return {
            'file_path': relative_path,
            'url_path': url_path
        }
    except Exception as e:
        logger.exception(f"Error saving image: {str(e)}")
        return None

def save_video(file):
    """Save an uploaded video file
    
    Args:
        file: The FileStorage object from the form
        
    Returns:
        Dict with file_path and url_path or None if failed
    """
    try:
        if not file:
            logger.error("No file provided to save_video")
            return None
            
        if not hasattr(file, 'filename') or not file.filename:
            logger.error("File has no filename")
            return None
            
        logger.debug(f"Processing video file: {file.filename}")
        
        if not allowed_video_file(file.filename):
            logger.error(f"Invalid video format: {file.filename}")
            return None
            
        filename = secure_filename(file.filename)
        logger.debug(f"Secured filename: {filename}")
        
        # Generate a unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        logger.debug(f"Generated unique filename: {unique_filename}")
        
        # Ensure upload directory exists
        upload_folder = current_app.config.get('UPLOAD_FOLDER_VIDEOS')
        if not upload_folder:
            logger.error("UPLOAD_FOLDER_VIDEOS not configured")
            return None
            
        os.makedirs(upload_folder, exist_ok=True)
        logger.debug(f"Ensured upload directory exists: {upload_folder}")
        
        file_path = os.path.join(upload_folder, unique_filename)
        logger.debug(f"Saving file to: {file_path}")
        
        file.save(file_path)
        logger.debug(f"File saved successfully")
        
        # Return the relative path for database storage - use forward slashes
        relative_path = normalize_path(os.path.join('uploads/videos', unique_filename))
        # Generate a URL path that can be used directly in templates
        url_path = url_for('static', filename=relative_path, _external=True)
        
        logger.info(f"Successfully saved video: {relative_path}")
        
        return {
            'file_path': relative_path,
            'url_path': url_path
        }
    except Exception as e:
        logger.exception(f"Error saving video: {str(e)}")
        return None

def delete_file(file_path):
    """Delete a file from the filesystem
    
    Args:
        file_path: The path to the file to delete, can be relative to static folder
                  or an absolute path
                  
    Returns:
        bool: True if the file was deleted successfully, False otherwise
    """
    if not file_path:
        logger.warning("No file path provided for deletion")
        return False
        
    logger.debug(f"Attempting to delete file: {file_path}")
    
    try:
        # Convert relative path to absolute path
        if file_path.startswith('uploads/'):
            full_path = os.path.join(current_app.static_folder, file_path)
            logger.debug(f"Converting relative path to absolute: {full_path}")
        else:
            # If it's already an absolute path
            full_path = file_path
            
        # Normalize path for Windows
        full_path = os.path.normpath(full_path)
        logger.debug(f"Normalized path for deletion: {full_path}")
        
        if os.path.exists(full_path):
            logger.debug(f"File exists, deleting: {full_path}")
            os.remove(full_path)
            logger.info(f"Successfully deleted file: {file_path}")
            return True
        else:
            logger.warning(f"File not found for deletion: {full_path}")
            return False
    except Exception as e:
        logger.exception(f"Error deleting file {file_path}: {str(e)}")
        return False 