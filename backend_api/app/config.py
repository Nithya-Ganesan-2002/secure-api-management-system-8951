import os
from datetime import timedelta

class BaseConfig:
    """Base configuration loaded from environment variables."""
    APP_NAME = os.getenv("APP_NAME", "My Flask API")
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = os.getenv("FLASK_TESTING", "0") == "1"

    # OpenAPI / Docs
    API_TITLE = os.getenv("API_TITLE", APP_NAME)
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = os.getenv("OPENAPI_VERSION", "3.0.3")
    OPENAPI_URL_PREFIX = os.getenv("OPENAPI_URL_PREFIX", "/docs")
    OPENAPI_SWAGGER_UI_PATH = os.getenv("OPENAPI_SWAGGER_UI_PATH", "")
    OPENAPI_SWAGGER_UI_URL = os.getenv("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MIN", "60")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "30")))

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": ProductionConfig,
}
