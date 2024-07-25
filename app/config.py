import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'app/static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads
