import logging
from flask import current_app
from app import db
from app.models.interior import InteriorCategoryText, InteriorGalleryImage, InteriorVideo
from app.models.construction import ConstructionCategoryText, ConstructionGalleryImage, ConstructionVideo

logger = logging.getLogger(__name__)

def get_used_categories(model_class):
    """Get categories that are already used in the database
    
    Args:
        model_class: The model class to query
        
    Returns:
        list: A list of unique categories used in the database
    """
    try:
        if not hasattr(model_class, 'category'):
            logger.warning(f"Model {model_class.__name__} does not have category attribute")
            return []
            
        # Check if we're in an application context
        try:
            current_app._get_current_object()
        except RuntimeError:
            logger.warning("No application context available, returning empty categories")
            return []
        
        categories = db.session.query(model_class.category).distinct().all()
        return [(cat[0], cat[0].replace('_', ' ').title()) for cat in categories if cat[0]]
        
    except Exception as e:
        logger.exception(f"Error getting used categories: {str(e)}")
        return []

def get_section_for_model(model_class):
    """Get the section name for a model class
    
    Args:
        model_class: The model class
        
    Returns:
        str: The section name or None if not found
    """
    if model_class in [InteriorCategoryText, InteriorGalleryImage, InteriorVideo]:
        return 'interior'
    elif model_class in [ConstructionCategoryText, ConstructionGalleryImage, ConstructionVideo]:
        return 'construction'
    
    logger.warning(f"Unknown model class: {model_class.__name__}")
    return None

def get_all_categories_for_model(model_class):
    """Get all categories for a model (from all models in the same section)
    
    Args:
        model_class: The model class
        
    Returns:
        list: A list of (value, label) tuples for the categories
    """
    section_name = get_section_for_model(model_class)
    
    if not section_name:
        return []
    
    # Get categories from all models in the same section
    all_categories = []
    
    if section_name == 'interior':
        # Get categories from all interior models
        for model in [InteriorCategoryText, InteriorGalleryImage, InteriorVideo]:
            if hasattr(model, 'category'):
                categories = get_used_categories(model)
                all_categories.extend(categories)
    elif section_name == 'construction':
        # Get categories from all construction models
        for model in [ConstructionCategoryText, ConstructionGalleryImage, ConstructionVideo]:
            if hasattr(model, 'category'):
                categories = get_used_categories(model)
                all_categories.extend(categories)
    
    # Remove duplicates by converting to a dictionary and back to a list
    unique_categories = list({cat[0]: cat for cat in all_categories}.values())
    
    # Sort categories alphabetically
    return sorted(unique_categories, key=lambda x: x[1])

def create_category(model_class, category_name):
    """Create a new category for a model class
    
    Args:
        model_class: The model class
        category_name: The name of the new category
        
    Returns:
        tuple: (success, message)
    """
    try:
        # Normalize category name (lowercase, replace spaces with underscores)
        normalized_name = category_name.lower().replace(' ', '_')
        
        # Check if category already exists
        existing_categories = [cat[0] for cat in get_used_categories(model_class)]
        if normalized_name in existing_categories:
            return False, f"Category '{category_name}' already exists"
        
        # Create a new entry with this category
        # This is a placeholder entry that will be used just to establish the category
        section_name = get_section_for_model(model_class)
        if not section_name:
            return False, f"Unknown model class: {model_class.__name__}"
        
        # Create a placeholder entry with the new category
        new_entry = model_class(
            title=f"Category: {category_name}",
            content=f"This is a placeholder for the {category_name} category.",
            category=normalized_name
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        return True, f"Category '{category_name}' created successfully"
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error creating category: {str(e)}")
        return False, f"Error creating category: {str(e)}"

def delete_category(model_class, category_name):
    """Delete a category and all its items
    
    Args:
        model_class: The model class
        category_name: The name of the category to delete
        
    Returns:
        tuple: (success, message)
    """
    try:
        # Find all items with this category
        items = db.session.query(model_class).filter_by(category=category_name).all()
        
        if not items:
            return False, f"No items found with category '{category_name}'"
        
        # Delete all items
        for item in items:
            db.session.delete(item)
        
        db.session.commit()
        return True, f"Category '{category_name}' and all its items deleted successfully"
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error deleting category: {str(e)}")
        return False, f"Error deleting category: {str(e)}" 