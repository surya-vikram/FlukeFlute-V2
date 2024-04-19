from app.extensions import cache
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
import os
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from app.models import *
from flask import abort
from app.utils import role_required
from config import Config
from flask import request
from werkzeug.utils import secure_filename
from app.extensions import db
from app.utils import pie_chart, column_chart, hist_chart
import base64
from config import Config

image_path = Config().PLOTS_FOLDER

def plotter():
    users = User.query.filter(User.stage_name.is_(None)).count()
    creators = User.query.filter(User.stage_name.isnot(None)).count()
    ratings = [ rating.rating_value for rating in Rating.query.all() ]
    genres = [(genre.name, len(genre.tracks)) for genre in Genre.query.all()]
    languages = [(lang.name, len(lang.tracks)) for lang in Language.query.all()]
    tracks = Track.query.count()
    albums = Album.query.count()
    playlists = Playlist.query.count()
    hist_chart(Visit.query.all(), 'activity.png')
    column_chart(['Tracks','Albums','Playlists'], [tracks, albums, playlists],'taps_chart.png')
    column_chart([i for i in range(1,6)], [ ratings.count(i) for i in range(1,6)], 'ratings_chart.png')
    pie_chart(['Users', 'Creators'], [users, creators], 'ucs_chart.png')
    pie_chart([genre[0] for genre in genres], [genre[1] for genre in genres], 'genres_chart.png')
    pie_chart([language[0] for language in languages], [language[1]  for language in languages], 'languages_chart.png')


class AdminResource(Resource):
    @role_required('Admin')
    @cache.cached(timeout=500)
    def get(self):
        plotter()
        albumJson = {}
        albumJson['users'] = User.query.filter(User.stage_name.is_(None)).count()
        albumJson['creators'] = User.query.filter(User.stage_name.isnot(None)).count()
        albumJson['albums'] = Album.query.count()
        albumJson['tracks'] = Track.query.count()
        albumJson['playlists'] = Playlist.query.count()
        albumJson['usersCreatorsChart'] = self.encode_image(os.path.join(image_path, 'ucs_chart.png'))
        albumJson['genresChart'] = self.encode_image(os.path.join(image_path, 'genres_chart.png'))
        albumJson['languagesChart'] = self.encode_image(os.path.join(image_path, 'languages_chart.png'))
        albumJson['statsChart'] = self.encode_image(os.path.join(image_path, 'taps_chart.png'))
        albumJson['ratingsChart'] = self.encode_image(os.path.join(image_path, 'ratings_chart.png'))
        albumJson['appActivity'] = self.encode_image(os.path.join(image_path, 'activity.png'))
        return albumJson, 200

    def encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')


class ManageCreators(Resource):
    @role_required('Admin')
    def put(self, id):
        creator = User.query.get(id)
        creator.is_flagged = not creator.is_flagged
        db.session.commit()
        cache.clear()
        return '', 200
    

class ManageTracks(Resource):
    @role_required('Admin')
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

class ManageAlbums(Resource):
    @role_required('Admin')
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


class AllCreators(Resource):
    @role_required('Admin')
    def get(self):
        artists = []
        creators = User.query.filter(User.stage_name.isnot(None)).all()
        for artist in creators:
            artistJson = {}
            artistJson['id'] = artist.id
            artistJson['name'] = artist.stage_name
            artistJson['popularity'] = artist.popularity()
            artistJson['is_flagged'] = artist.is_flagged
            artists.append(artistJson)
        return artists, 200
    
class AllAlbums(Resource):
    @role_required('Admin')
    def get(self):
        albums = []
        for album in Album.query.all():
            albumJson = {}
            albumJson['id'] = album.id
            albumJson['title'] = album.title
            albumJson['date_created'] = str(album.date_created)
            albums.append(albumJson)
        return albums, 200
    
class AllTracks(Resource):
    @role_required('Admin')
    def get(self):
        tracks = []
        for track in Track.query.all():
            trackJson = {}
            trackJson['id'] = track.id
            trackJson['title'] = track.title
            trackJson['rating'] = track.avg_rating()
            tracks.append(trackJson)
        return tracks, 200
    
    
