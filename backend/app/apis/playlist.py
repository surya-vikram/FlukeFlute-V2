import os
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import get_jwt_header, get_jwt_identity
from app.models import User, Track, Genre, Language, Album, Playlist
from flask import abort
from app.utils import role_required
from config import Config
from flask import request
from werkzeug.utils import secure_filename
from app.extensions import db
import base64
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import cache

playlist_fields = {
    'id': fields.Integer,
    'name': fields.String
}
class PlaylistsResources(Resource):
    @cache.cached(100)
    @marshal_with(playlist_fields)
    @role_required('Basic')
    def get(self):
        user = User.query.get(get_jwt_identity())
        return user.playlists, 200
    
    @role_required('Basic')
    def post(self):
        data = request.json
        name = data.get('name')
        track_ids = data.get('track_ids', [])
        tracks = [Track.query.get(int(track_id)) for track_id in track_ids]
        playlist = Playlist(name=name, creator_id=get_jwt_identity(), tracks=tracks)
        db.session.add(playlist)
        db.session.commit()
        cache.clear()
        return 'Playlist created successfully !', 200


class PlaylistResource(Resource):
    @cache.cached(100)
    @role_required('Basic')
    def get(self, id):
        playlist = Playlist.query.get(id)
        if not playlist:
            abort(404, 'Playlist not found')
        playlistJson = {}
        playlistJson['name'] = playlist.name
        tracks = []
        for track in playlist.tracks:
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
            tracks.append(trackJson)
        playlistJson['tracks'] = tracks
        return playlistJson, 200

    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data

    @role_required('Basic')
    def put(self, id):
        data = request.json
        name = data.get('name')
        track_ids = data.get('track_ids', [])
        tracks = [Track.query.get(int(track_id)) for track_id in track_ids]
        playlist = Playlist.query.get(id)
        playlist.name = name
        playlist.tracks = tracks
        db.session.commit()
        cache.clear()
        return 'Playlist updated successfully !', 200

    @role_required('Basic')
    def delete(self, id):
        playlist = Playlist.query.get(id)
        if not playlist:
            return {'message': 'Playlist not found'}, 404
        try:
            db.session.delete(playlist)
            db.session.commit()
            cache.clear()
            return {'message': 'Playlist deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': str(e)}, 500

