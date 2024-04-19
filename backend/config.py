import os
from datetime import timedelta

class Config():
    SECRET_KEY = "zerotwo"
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "data")
    PLOTS_FOLDER = os.path.join(os.getcwd(),"app/static/images")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "data/database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    CELERY_BROKER_URL = "redis://localhost:6380/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6380/0"

    

    
