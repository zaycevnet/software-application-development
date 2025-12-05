import os

class Config:
    # Подключение к базе данных PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ Flask-приложения
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

