import os
from flask import Flask
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from .utils import add_roles, add_genres, add_languages, add_admin


load_dotenv()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    
    from app.extensions import api, bcrypt, cache, db, jwt, celery_app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    celery_app.conf.update(app.config)
    cache.init_app(
        app,
        config={
            "CACHE_TYPE": "redis",
            "CACHE_REDIS_URL": "redis://localhost:6380/1",
            "prefix": "cache_",
        },
    )
    
    db.create_all()
    add_roles()
    add_genres()
    add_languages()
    add_admin(username=os.getenv('ADMIN_USERNAME'), email=os.getenv('ADMIN_EMAIL'), password=os.getenv('ADMIN_PASSWORD'))
   
    from app.apis import UserLogin, AdminLogin
    api.add_resource(UserLogin, '/login/user')
    api.add_resource(AdminLogin, '/login/admin') 
    
    from app.apis import UserResource
    api.add_resource(UserResource, '/user')

    from app.apis import CreatorResource
    api.add_resource(CreatorResource, '/artists')
    
    from app.apis import RolesResource
    api.add_resource(RolesResource, "/roles")
    
    from app.apis import GenresResource
    api.add_resource(GenresResource, "/genres")
    
    from app.apis import LanguagesResource
    api.add_resource(LanguagesResource, "/languages")

    from app.apis import PlaylistResource, PlaylistsResources
    api.add_resource(PlaylistsResources, '/playlists')
    api.add_resource(PlaylistResource, '/playlist/<int:id>')
    
    from app.apis import TracksResource, TrackResource, FilterTracksResource
    api.add_resource(TracksResource, "/tracks")
    api.add_resource(TrackResource, "/track/<int:id>")
    api.add_resource(FilterTracksResource, "/filter/<int:id>")

    from app.apis import CreatorOrphanTracks
    api.add_resource(CreatorOrphanTracks, '/creator/orphan')

    from app.apis import AlbumsResource
    api.add_resource(AlbumsResource, '/albums')
  
    from app.apis import AlbumResource, AvailabeTracks
    api.add_resource(AlbumResource, '/album/<int:id>')
    api.add_resource(AvailabeTracks, '/available_tracks/<int:album_id>')

    from app.apis import ArtistResource
    api.add_resource(ArtistResource, '/artist/<int:id>')

    from app.apis import SearchResource
    api.add_resource(SearchResource, '/search/<string:searched>')

    from app.apis import RatingResource
    api.add_resource(RatingResource, '/rate')

    from app.apis import CreatorAlbums
    api.add_resource(CreatorAlbums, '/creator/albums')
    
    from app.apis import CreatorTracks
    api.add_resource(CreatorTracks, '/creator/tracks')
    
    from app.apis import AdminResource, ManageTracks, ManageCreators, ManageAlbums, AllCreators, AllTracks, AllAlbums
    api.add_resource(AdminResource, '/stats')
    api.add_resource(ManageAlbums, '/remove_album/<int:id>')
    api.add_resource(ManageCreators, '/flag/<int:id>')
    api.add_resource(ManageTracks, '/remove_track/<int:id>')
    api.add_resource(AllCreators, '/creators')
    api.add_resource(AllTracks, '/all_tracks')
    api.add_resource(AllAlbums, '/all_albums')
    
    api.init_app(app)
    return app


