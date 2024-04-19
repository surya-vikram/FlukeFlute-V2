from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.models import User, Role, Album, Track, Language, Genre
from flask import abort
from app.utils import role_required
from config import Config
from app.utils import validate_email, validate_name, validate_username, validate_unique_username, validate_unique_email, validate_password
from app.extensions import db
import base64
from app.extensions import cache
import os

class UserResource(Resource):
    @cache.cached(100)
    @role_required('Basic')
    def get(self):
        userJson = {}
        user = User.query.get(get_jwt_identity())
        userJson['name'] = user.name
        userJson['username'] = user.username
        userJson['email'] = user.email
        if user.pfp_path:
            userJson['pfp'] = self.encode_image(user.pfp_path)
        else:
            userJson['pfp'] = self.encode_image(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'default.jpg')))
        userJson['stage_name'] = user.stage_name
        userJson['bio'] = user.bio
        userJson['tracks'] = len(user.tracks)
        userJson['albums'] = len(user.albums)
        userJson['playlists'] = len(user.playlists)
        userJson['visits'] = len(user.visits)
        return userJson, 200
    
    def encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    def post(self):        
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('confirmPassword')
        
        args = parser.parse_args()
        name = args['name']
        validate_name(name)
        username = args['username']
        validate_username(username)
        validate_unique_username(username)
        email = args['email']
        validate_email(email)
        validate_unique_email(email)
        password, confirm_password = args['password'], args['confirmPassword']
        validate_password(password)
        print(password, confirm_password)
        if password != confirm_password:
            abort(400, 'Passwords do not match')

        user_to_register = User(name=name, username=username, email=email, password=password, roles=[Role.query.filter_by(name='Basic').first()])
        db.session.add(user_to_register)
        db.session.commit()
        cache.clear()
        
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, 'User not found')
        user_roles = [ role.name for role in user.roles ]

        token_expires = Config().JWT_ACCESS_TOKEN_EXPIRES
        access_token = create_access_token(identity=user.id, expires_delta=token_expires)
        return {'user_id': user.id, 'roles': user_roles, 'access_token': access_token}, 200


class SearchResource(Resource):
    @cache.cached(100)
    @role_required('Basic')
    def get(self, searched):
        artists = User.query.filter(User.stage_name.contains(searched), User.is_flagged == False).all()
        tracks = Track.query.filter(Track.title.contains(searched) | Track.lyrics.contains(searched)).all()
        albums = Album.query.filter( Album.title.contains(searched) | Album.description.contains(searched)).all() 
        genre = Genre.query.filter(Genre.name.contains(searched)).first()
        lang = Language.query.filter(Language.name.contains(searched)).first()
        if genre:
            tracks.extend(genre.tracks)
        if lang:
            tracks.extend(lang.tracks)
        searchJson = {'artists': [], 'tracks': [], 'albums': []}
        for album in albums:
            albumJson = {}
            albumJson['id'] = album.id
            albumJson['title'] = album.title
            albumJson['description'] = album.description
            albumJson['cover'] = self.encode_image(album.cover_path)
            albumJson['creator'] = User.query.get(album.creator_id).stage_name
            albumJson['date_created'] = str(album.date_created)
            searchJson['albums'].append(albumJson)
        
        for artist in artists:
            artistJson = {}
            artistJson['id'] = artist.id
            artistJson['name'] = artist.stage_name
            artistJson['pfp'] = self.encode_image(artist.pfp_path)
            artistJson['popularity'] = artist.popularity()
            artistJson['is_flagged'] = artist.is_flagged
            searchJson['artists'].append(artistJson)

        for track in tracks:
            trackJson = {}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            trackJson['lyrics'] = track.lyrics
            trackJson['audio'] = self.encode_audio(track.audio_path)
            trackJson['playback_count'] = track.playback_count
            trackJson['release_date'] = str(track.release_date)
            trackJson['creator'] = User.query.get(track.creator_id).stage_name
            trackJson['language'] = Language.query.get(track.language_id).name
            trackJson['genre'] = Genre.query.get(track.genre_id).name
            trackJson['rating'] = track.avg_rating()
            searchJson['tracks'].append(trackJson)
        return searchJson, 200

    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data

    def encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
                      

                      