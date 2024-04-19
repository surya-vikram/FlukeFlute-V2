import os
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from app.models import User, Track, Genre, Language, Album
from flask import abort
from app.utils import role_required
from config import Config
from flask import request
from werkzeug.utils import secure_filename
from app.extensions import db
import base64
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import cache

class TracksResource(Resource):
    @cache.cached(500)
    @role_required('Basic')
    def get(self):
        tracks = []
        for track in Track.query.all():
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
        return tracks, 200

    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data

    @role_required('Creator')
    def post(self):
        title = request.form.get('title')
        if not title:
            abort(400, 'Title is empty')
        language = request.form.get('language')
        if not language:
            abort(400, 'Please select a language')
        language_id = Language.query.filter_by(name=language).first().id
        genre = request.form.get('genre')
        if not genre:
            abort(400, "Please select a genre")
        genre_id = Genre.query.filter_by(name=genre).first().id
        audio_file = request.files.get('file')
        if not audio_file:
            abort(400, 'Choose a audio file')
        lyrics = request.form.get('lyrics')
        creator = User.query.get(get_jwt_identity())
        if not creator:
            abort(404, 'Creator not found') 
        filename = secure_filename(audio_file.filename)
        upload_folder = os.path.join(Config().UPLOAD_FOLDER, 'audios')
        audio_path = os.path.join(upload_folder, filename)
        audio_file.save(audio_path)
        track = Track(title=title, genre_id=genre_id, lyrics=lyrics, audio_path=audio_path, creator_id=creator.id, language_id=language_id)
        db.session.add(track)
        db.session.commit()
        cache.clear()
        return {'message':  f'Success! {title} has been created.'}, 200


class TrackResource(Resource):
    @cache.cached(500)
    @role_required('Basic')
    def get(self, id):
        track = Track.query.get(id)
        track.increment_playback()
        trackJson = {}
        trackJson['id'] = track.id
        trackJson['title'] = track.title
        trackJson['lyrics'] = track.lyrics
        trackJson['language'] = Language.query.get(track.language_id).name
        trackJson['genre'] = Genre.query.get(track.genre_id).name
        return trackJson, 200

    @role_required('Creator')
    def put(self, id):
        try:
            track = Track.query.get(id)
            if not track:
                return {'message': 'Track not found'}, 404
            title = request.form.get('title')
            if not title:
                abort(400, 'Title is empty')
            language = request.form.get('language')
            if not language:
                abort(400, 'Please select a language')
            language_id = Language.query.filter_by(name=language).first().id
            genre = request.form.get('genre')
            if not genre:
                abort(400, 'Please select a genre')
            genre_id = Genre.query.filter_by(name=genre).first().id
            audio_file = request.files.get('file')
            lyrics = request.form.get('lyrics')
            track.title = title
            track.genre_id = genre_id
            track.language_id = language_id
            track.lyrics = lyrics
            if audio_file:
                filename = secure_filename(audio_file.filename)
                upload_folder = os.path.join(Config().UPLOAD_FOLDER, 'audios')
                audio_path = os.path.join(upload_folder, filename)
                audio_file.save(audio_path)
                track.audio_path = audio_path
            db.session.commit()
            cache.clear()
            return {'message': f'Track {id} has been updated successfully.'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to update track', 'error': str(e)}, 500

    @role_required('Creator')
    def delete(self, id):
        try:
            track = Track.query.get(id)
            if not track:
                return {'message': 'Track not found'}, 404
            db.session.delete(track)
            db.session.commit()
            cache.clear()
            return '', 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to delete track', 'error': str(e)}, 500


class FilterTracksResource(Resource):
    @cache.cached(120)
    @role_required('Basic')
    def get(self, id):
        filtered_tracks = None
        if id == 1:
            filtered_tracks = Track.top_rated()
        elif id == 2:
            filtered_tracks = Track.trending()
        else: 
            filtered_tracks = Track.query.order_by(Track.release_date.desc()).limit(10).all()
        tracks = []
        for track in filtered_tracks:
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
        return tracks, 200

    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data
    

