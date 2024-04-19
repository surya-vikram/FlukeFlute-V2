import os
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity
from app.models import User, Track, Album, Language, Genre, Rating
from flask import abort
from app.utils import role_required
from config import Config
from flask import request
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
import base64
from app.extensions import cache

class CreatorResource(Resource):
    @role_required('Basic')
    @cache.cached(timeout=100)
    def get(self):
        artists = []
        creators = User.query.filter_by(is_flagged=False).filter(User.stage_name.isnot(None)).all()
        for artist in creators:
            artistJson = {}
            artistJson['id'] = artist.id
            artistJson['name'] = artist.stage_name
            artistJson['pfp'] = self.encode_image(artist.pfp_path)
            artistJson['popularity'] = artist.popularity()
            artistJson['is_flagged'] = artist.is_flagged
            artists.append(artistJson)
        return artists, 200

    def encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')


    @role_required('Basic')
    def post(self):
        stage_name = request.form.get('stageName')
        if not stage_name:
            abort(400, 'Stage Name is required')
        bio = request.form.get('bio')
        if not bio:
            abort(400, 'Bio is required')
        file = request.files.get('pfp')
        if not file:
            abort(400, 'PFP is required')     
        user = User.query.get(get_jwt_identity())
        if not user:
            abort(404, 'User not found')      
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(Config().UPLOAD_FOLDER, 'images')
        image_path = os.path.join(upload_folder, filename)
        file.save(image_path)
        user.make_creator(stage_name=stage_name, bio=bio, pfp=image_path)
        cache.clear()
        return {'message': "Congrats! You're a creator now"}, 200


orphan_tracks_field = {
    'id': fields.Integer,
    'title': fields.String
}


class CreatorOrphanTracks(Resource):
    
    @marshal_with(orphan_tracks_field)
    @role_required('Creator')
    def get(self):  
        creator_id = get_jwt_identity()
        orphan_tracks = Track.query.filter(and_(Track.creator_id == creator_id, Track.album_id == None)).all()
        return orphan_tracks, 200    


class CreatorTracks(Resource):
    @role_required('Creator')
    @cache.cached(timeout=100)
    def get(self):  
        creator = User.query.get(get_jwt_identity())
        tracks = []
        for track in creator.tracks:
            trackJson =  {}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            trackJson['rating'] = track.avg_rating()
            tracks.append(trackJson)
        return tracks, 200 


class CreatorAlbums(Resource):
    @role_required('Creator')
    @cache.cached(timeout=100)
    def get(self):
        creator = User.query.get(get_jwt_identity())
        albums = []
        for album in creator.albums:
            albumJson = {}
            albumJson['id'] = album.id
            albumJson['title'] = album.title
            albumJson['description'] = album.description
            albumJson['cover'] = self.encode_image(album.cover_path)
            albumJson['creator'] = User.query.get(album.creator_id).stage_name
            albumJson['date_created'] = str(album.date_created)
            albums.append(albumJson)
        return albums, 200

    def encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')


class ArtistResource(Resource):
    @role_required('Basic')
    @cache.cached(timeout=100)
    def get(self, id):
        artist = User.query.get(int(id))
        artistJson = {}
        artistJson['id'] = artist.id
        artistJson['name'] = artist.stage_name
        artistJson['bio'] = artist.bio
        artistJson['popularity'] = artist.popularity()
        tracks = []
        for track in artist.tracks:
            trackJson = {}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            trackJson['lyrics'] = track.lyrics
            trackJson['audio'] = self.encode_audio(track.audio_path)
            trackJson['playback_count'] = track.playback_count
            trackJson['release_date'] = str(track.release_date)
            trackJson['language'] = Language.query.get(track.language_id).name
            trackJson['genre'] = Genre.query.get(track.genre_id).name
            trackJson['rating'] = track.avg_rating()
            tracks.append(trackJson)
        artistJson['tracks'] = tracks
        return artistJson, 200
    
    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data
