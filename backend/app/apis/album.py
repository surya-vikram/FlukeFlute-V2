from operator import and_
import os
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from matplotlib.style import available
from app.models import User, Album, Track, Genre, Language
from flask import abort
from app.utils import role_required
from config import Config
from flask import request
from werkzeug.utils import secure_filename
from app.extensions import db, cache
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

import base64

class AlbumsResource(Resource):
    @role_required('Basic')
    @cache.cached(timeout=20)
    def get(self):
        albums = []
        for album in Album.query.all():
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
        
    @role_required('Creator')
    def post(self):
        title = request.form.get('title')
        if not title:
            abort(400, 'Title is empty')
        track_ids = request.form.get('tracks')
        if not track_ids:
            abort(400, "Please select a tracks")
        cover_file = request.files.get('file')
        if not cover_file:
            abort(400, 'Choose a album cover')
        description = request.form.get('description')
        creator = User.query.get(get_jwt_identity())
        if not creator:
            abort(404, 'Creator not found') 
        filename = secure_filename(cover_file.filename)
        upload_folder = os.path.join(Config().UPLOAD_FOLDER, 'images')
        cover_path = os.path.join(upload_folder, filename)
        cover_file.save(cover_path)
        tracks = []
        for track_id in track_ids.split(','):
            track_id = track_id.strip()  
            if track_id:
                track = Track.query.get(int(track_id))
                if track:
                    tracks.append(track)
        album = Album(title=title, description=description, cover_path=cover_path, creator_id=creator.id, tracks=tracks)
        db.session.add(album)
        db.session.commit()
        cache.clear()
        return {'message': f'Success! {title} has been created.'}, 200

    
class AlbumResource(Resource):
    @role_required('Basic')
    @cache.cached(timeout=20)
    def get(self, id):
        album = Album.query.get(int(id))
        albumJson = {}
        albumJson['id'] = album.id
        albumJson['title'] = album.title
        albumJson['description'] = album.description
        albumJson['cover_path'] = album.cover_path
        albumJson['creator'] = User.query.get(album.creator_id).stage_name
        albumJson['date_created'] = str(album.date_created)
        tracks = []
        for track in album.tracks:
            trackJson = {}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            trackJson['lyrics'] = track.lyrics
            trackJson['audio'] = self.encode_audio(track.audio_path)
            trackJson['playback_count'] = track.playback_count
            trackJson['release_date'] = str(track.release_date)
            trackJson['creator'] = User.query.get(track.creator_id).stage_name
            trackJson['album'] = Album.query.get(track.album_id).title
            trackJson['language'] = Language.query.get(track.language_id).name
            trackJson['genre'] = Genre.query.get(track.genre_id).name
            trackJson['rating'] = track.avg_rating()
            tracks.append(trackJson)
        albumJson['tracks'] = tracks
        return albumJson, 200
        
    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data



    @role_required('Creator')
    def put(self, id):
        try:
            album = Album.query.get(id)
            if not album:
                return {'message': 'Album not found'}, 404

            title = request.form.get('title')
            if not title:
                abort(400, 'Title is empty')

            track_ids = request.form.get('tracks')
            if not track_ids:
                abort(400, "Please select tracks")

            description = request.form.get('description')

            album.title = title
            album.description = description

            cover_file = request.files.get('file')
            if cover_file:
                filename = secure_filename(cover_file.filename)
                upload_folder = os.path.join(Config().UPLOAD_FOLDER, 'images')
                cover_path = os.path.join(upload_folder, filename)
                cover_file.save(cover_path)
                album.cover_path = cover_path

            tracks = []
            for track_id in track_ids.split(','):
                track_id = track_id.strip()
                if track_id:
                    track = Track.query.get(int(track_id))
                    if track:
                        tracks.append(track)

            album.tracks = tracks

            db.session.commit()
            cache.clear()

            return {'message': f'Album {id} has been updated successfully.'}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to update album', 'error': str(e)}, 500


    def delete(self, id):
        try:
            album = Album.query.get(id)
            if not album:
                return {'message': 'Album not found'}, 404

            db.session.delete(album)
            db.session.commit()
            cache.clear()
            return '', 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to delete album', 'error': str(e)}, 500
        
class AvailabeTracks(Resource):
    @role_required('Creator')
    def get(self, album_id):
        creator_id = get_jwt_identity()
        orphan_tracks = Track.query.filter(and_(Track.creator_id == creator_id, Track.album_id == None)).all()
        album_tracks = Album.query.get(album_id).tracks
        available_tracks = orphan_tracks + album_tracks
        tracks = []
        for track in available_tracks:
            trackJson={}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            tracks.append(trackJson)
        return tracks, 200

