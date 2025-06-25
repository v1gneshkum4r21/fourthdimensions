from flask import request
from flask_restx import Resource
from app.api import ns_interior
from app.api.resources.auth import token_required
from app.api.schemas.interior import (
    interior_category_text, interior_category_text_response,
    interior_gallery_image, interior_video,
    interior_image_parser, interior_video_parser
)
from app.models.interior import InteriorCategoryText, InteriorGalleryImage, InteriorVideo
from app.utils.file_helpers import save_image, save_video, delete_file
from app import db

# Interior Category Text Resources
@ns_interior.route('/categories/text')
class InteriorCategoryTextList(Resource):
    @ns_interior.doc('list_interior_category_texts')
    @ns_interior.marshal_list_with(interior_category_text_response)
    def get(self):
        """List all interior category texts"""
        return InteriorCategoryText.query.all()
    
    @ns_interior.doc('create_interior_category_text')
    @ns_interior.expect(interior_category_text)
    @ns_interior.marshal_with(interior_category_text_response, code=201)
    @token_required
    def post(self):
        """Create a new interior category text"""
        data = request.json
        interior_text = InteriorCategoryText(
            title=data['title'],
            content=data['content'],
            category=data['category']
        )
        db.session.add(interior_text)
        db.session.commit()
        return interior_text, 201

@ns_interior.route('/categories/text/<int:id>')
@ns_interior.param('id', 'The interior category text identifier')
class InteriorCategoryTextItem(Resource):
    @ns_interior.doc('delete_interior_category_text')
    @ns_interior.response(204, 'Interior category text deleted')
    @token_required
    def delete(self, id):
        """Delete an interior category text given its identifier"""
        interior_text = InteriorCategoryText.query.get_or_404(id)
        db.session.delete(interior_text)
        db.session.commit()
        return '', 204

# Interior Gallery Image Resources
@ns_interior.route('/gallery/images')
class InteriorGalleryImageList(Resource):
    @ns_interior.doc('list_interior_gallery_images')
    @ns_interior.param('category', 'Filter images by category')
    @ns_interior.marshal_list_with(interior_gallery_image)
    def get(self):
        """List all interior gallery images, optionally filtered by category"""
        category = request.args.get('category')
        if category:
            return InteriorGalleryImage.query.filter_by(category=category).all()
        return InteriorGalleryImage.query.all()
    
    @ns_interior.doc('create_interior_gallery_image')
    @ns_interior.expect(interior_image_parser)
    @ns_interior.marshal_with(interior_gallery_image, code=201)
    @token_required
    def post(self):
        """Upload a new interior gallery image"""
        args = interior_image_parser.parse_args()
        
        # Save the image file
        image_result = save_image(args['file'])
        if not image_result:
            ns_interior.abort(400, "Invalid image file")
        
        interior_image = InteriorGalleryImage(
            title=args['title'],
            description=args.get('description', ''),
            category=args['category'],
            image_path=image_result['file_path']
        )
        db.session.add(interior_image)
        db.session.commit()
        return interior_image, 201

@ns_interior.route('/gallery/images/<int:id>')
@ns_interior.param('id', 'The interior gallery image identifier')
class InteriorGalleryImageItem(Resource):
    @ns_interior.doc('delete_interior_gallery_image')
    @ns_interior.response(204, 'Interior gallery image deleted')
    @token_required
    def delete(self, id):
        """Delete an interior gallery image given its identifier"""
        interior_image = InteriorGalleryImage.query.get_or_404(id)
        
        # Delete the image file
        delete_file(interior_image.image_path)
        
        # Delete the database record
        db.session.delete(interior_image)
        db.session.commit()
        return '', 204

# Interior Video Resources
@ns_interior.route('/videos')
class InteriorVideoList(Resource):
    @ns_interior.doc('list_interior_videos')
    @ns_interior.marshal_list_with(interior_video)
    def get(self):
        """List all interior videos"""
        return InteriorVideo.query.all()
    
    @ns_interior.doc('create_interior_video')
    @ns_interior.expect(interior_video_parser)
    @ns_interior.marshal_with(interior_video, code=201)
    @token_required
    def post(self):
        """Upload a new interior video"""
        args = interior_video_parser.parse_args()
        
        # Save the video file
        video_result = save_video(args['file'])
        if not video_result:
            ns_interior.abort(400, "Invalid video file")
        
        interior_video = InteriorVideo(
            title=args['title'],
            description=args.get('description', ''),
            category=args.get('category'),
            video_path=video_result['file_path']
        )
        db.session.add(interior_video)
        db.session.commit()
        return interior_video, 201

@ns_interior.route('/videos/<int:id>')
@ns_interior.param('id', 'The interior video identifier')
class InteriorVideoItem(Resource):
    @ns_interior.doc('update_interior_video')
    @ns_interior.expect(interior_video_parser)
    @ns_interior.marshal_with(interior_video)
    @token_required
    def put(self, id):
        """Update an interior video given its identifier"""
        interior_video = InteriorVideo.query.get_or_404(id)
        args = interior_video_parser.parse_args()
        
        # Update metadata
        interior_video.title = args['title']
        interior_video.description = args.get('description', '')
        interior_video.category = args.get('category', interior_video.category)
        
        # If a new file is provided, update the video
        if args['file']:
            # Delete the old video
            delete_file(interior_video.video_path)
            
            # Save the new video
            video_result = save_video(args['file'])
            if not video_result:
                ns_interior.abort(400, "Invalid video file")
            
            interior_video.video_path = video_result['file_path']
        
        db.session.commit()
        return interior_video
    
    @ns_interior.doc('delete_interior_video')
    @ns_interior.response(204, 'Interior video deleted')
    @token_required
    def delete(self, id):
        """Delete an interior video given its identifier"""
        interior_video = InteriorVideo.query.get_or_404(id)
        
        # Delete the video file
        delete_file(interior_video.video_path)
        
        # Delete the database record
        db.session.delete(interior_video)
        db.session.commit()
        return '', 204 