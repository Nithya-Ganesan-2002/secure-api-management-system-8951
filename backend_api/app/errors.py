from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError

def register_error_handlers(app):
    """Register global error handlers for the Flask app."""
    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        response = {
            "code": err.code,
            "status": err.name,
            "message": err.description,
        }
        return jsonify(response), err.code

    @app.errorhandler(Exception)
    def handle_generic_exception(err: Exception):
        app.logger.exception("Unhandled exception: %s", err)
        return jsonify({"message": "Internal server error"}), 500
