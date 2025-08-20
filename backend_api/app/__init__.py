import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv
from .config import config_by_name
from .extensions import db, jwt
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.users import blp as users_blp
from .routes.students import blp as students_blp
from .routes.rooms import blp as rooms_blp
from .routes.products import blp as products_blp
from .errors import register_error_handlers

# PUBLIC_INTERFACE
def create_app(config_name: str | None = None) -> Flask:
    """Application factory that initializes extensions, blueprints, and configuration from environment."""
    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    cfg_name = config_name or os.getenv("FLASK_CONFIG", "default")
    app.config.from_object(config_by_name.get(cfg_name, config_by_name["default"]))

    # Docs / OpenAPI
    app.config["API_TITLE"] = app.config.get("API_TITLE", "My Flask API")
    app.config["API_VERSION"] = app.config.get("API_VERSION", "v1")
    app.config["OPENAPI_VERSION"] = app.config.get("OPENAPI_VERSION", "3.0.3")
    app.config["OPENAPI_URL_PREFIX"] = app.config.get("OPENAPI_URL_PREFIX", "/docs")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = app.config.get("OPENAPI_SWAGGER_UI_PATH", "")
    app.config["OPENAPI_SWAGGER_UI_URL"] = app.config.get("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")

    # CORS
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Extensions
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    # Blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(students_blp)
    api.register_blueprint(rooms_blp)
    api.register_blueprint(products_blp)

    # Errors
    register_error_handlers(app)

    # Create DB tables if not exist (for demo; in prod use migrations)
    with app.app_context():
        db.create_all()

    return app

# Backward compatibility for run.py importing app
app = create_app()
