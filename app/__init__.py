from flask import Flask, jsonify
from flask_restful import Api

from app.common.error_handling import ObjectNotFound, AppErrorBaseClass
from app.db import db
from app.citas.api_v1_0.resources import appointment_v1_0_bp
from .ext import ma, migrate


def create_app(settings_module):
    flask_app = Flask(__name__)
    flask_app.config.from_object(settings_module)

    # Inicializa las extensiones
    db.init_app(flask_app)
    ma.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # Captura todos los errores 404
    Api(flask_app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    flask_app.url_map.strict_slashes = False

    # Registra los blueprints
    flask_app.register_blueprint(appointment_v1_0_bp)

    from .views import views

    flask_app.register_blueprint(views, url_prefix='/')

    # Registra manejadores de errores personalizados
    register_error_handlers(flask_app)

    return flask_app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        print(e)
        return jsonify({'msg': 'Internal server error','error':str(e)}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed','error':str(e)}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404