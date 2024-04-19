from flask_restful import Api
from celery import Celery
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

cache = Cache()
api = Api(prefix="/api/v1")
bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()


celery_app = Celery(
    "tasks",
    broker="redis://127.0.0.1:6380/0",
    backend="redis://127.0.0.1:6380/0",
)

celery_app.autodiscover_tasks(['app.tasks'])



