from flask import request
from flask_restx import Resource
from app.api import ns_hero
from app.api.resources.auth import token_required
from app.api.schemas.hero import hero_text, hero_text_response, hero_video, hero_video_parser
from app.models.hero import HeroText, HeroVideo
from app.utils.file_helpers import save_video, delete_file
from app import db

@ns_hero.route('/text')
class HeroTextList(Resource):
    @ns_hero.doc('list_hero_texts')
    @ns_hero.marshal_list_with(hero_text_response)
    def get(self):
        """List all hero texts"""
        return HeroText.query.all()
    
    @ns_hero.doc('create_hero_text')
    @ns_hero.expect(hero_text)
    @ns_hero.marshal_with(hero_text_response, code=201)
    @token_required
    def post(self):
        """Create a new hero text"""
        data = request.json
        hero_text_item = HeroText(
            title=data['title'],
            content=data['content']
        )
        db.session.add(hero_text_item)
        db.session.commit()
        return hero_text_item, 201

@ns_hero.route('/text/<int:id>')
@ns_hero.param('id', 'The hero text identifier')
class HeroTextItem(Resource):
    @ns_hero.doc('get_hero_text')
    @ns_hero.marshal_with(hero_text_response)
    def get(self, id):
        """Fetch a hero text given its identifier"""
        return HeroText.query.get_or_404(id)
    
    @ns_hero.doc('update_hero_text')
    @ns_hero.expect(hero_text)
    @ns_hero.marshal_with(hero_text_response)
    @token_required
    def put(self, id):
        """Update a hero text given its identifier"""
        hero_text_item = HeroText.query.get_or_404(id)
        data = request.json
        
        hero_text_item.title = data.get('title', hero_text_item.title)
        hero_text_item.content = data.get('content', hero_text_item.content)
        
        db.session.commit()
        return hero_text_item
    
    @ns_hero.doc('delete_hero_text')
    @ns_hero.response(204, 'Hero text deleted')
    @token_required
    def delete(self, id):
        """Delete a hero text given its identifier"""
        hero_text_item = HeroText.query.get_or_404(id)
        db.session.delete(hero_text_item)
        db.session.commit()
        return '', 204

@ns_hero.route('/videos')
class HeroVideoList(Resource):
    @ns_hero.doc('list_hero_videos')
    @ns_hero.marshal_list_with(hero_video)
    def get(self):
        """List all hero videos"""
        return HeroVideo.query.all()
    
    @ns_hero.doc('create_hero_video')
    @ns_hero.expect(hero_video_parser)
    @ns_hero.marshal_with(hero_video, code=201)
    @token_required
    def post(self):
        """Upload a new hero video"""
        args = hero_video_parser.parse_args()
        
        # Save the video file
        video_result = save_video(args['file'])
        if not video_result:
            ns_hero.abort(400, "Invalid video file")
        
        hero_video_item = HeroVideo(
            title=args['title'],
            description=args.get('description', ''),
            video_path=video_result['file_path']
        )
        db.session.add(hero_video_item)
        db.session.commit()
        return hero_video_item, 201

@ns_hero.route('/videos/<int:id>')
@ns_hero.param('id', 'The hero video identifier')
class HeroVideoItem(Resource):
    @ns_hero.doc('get_hero_video')
    @ns_hero.marshal_with(hero_video)
    def get(self, id):
        """Fetch a hero video given its identifier"""
        return HeroVideo.query.get_or_404(id)
    
    @ns_hero.doc('update_hero_video')
    @ns_hero.expect(hero_video_parser)
    @ns_hero.marshal_with(hero_video)
    @token_required
    def put(self, id):
        """Update a hero video given its identifier"""
        hero_video_item = HeroVideo.query.get_or_404(id)
        args = hero_video_parser.parse_args()
        
        # Update metadata
        hero_video_item.title = args['title']
        hero_video_item.description = args.get('description', '')
        
        # If a new file is provided, update the video
        if args['file']:
            # Delete the old video
            delete_file(hero_video_item.video_path)
            
            # Save the new video
            video_result = save_video(args['file'])
            if not video_result:
                ns_hero.abort(400, "Invalid video file")
            
            hero_video_item.video_path = video_result['file_path']
        
        db.session.commit()
        return hero_video_item
    
    @ns_hero.doc('delete_hero_video')
    @ns_hero.response(204, 'Hero video deleted')
    @token_required
    def delete(self, id):
        """Delete a hero video given its identifier"""
        hero_video_item = HeroVideo.query.get_or_404(id)
        
        # Delete the video file
        delete_file(hero_video_item.video_path)
        
        # Delete the database record
        db.session.delete(hero_video_item)
        db.session.commit()
        return '', 204 