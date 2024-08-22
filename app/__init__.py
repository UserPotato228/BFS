# flask app init file
import os

# imports
from flask import Flask, request, send_from_directory
from config import Config
from app.extensions import db

# create app func
def create_app(config_class = Config):
    # start flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init db
    db.init_app(app)

    # session
    app.secret_key = "1122331122"

    # blueprints
    from app.index import bp as index_bp
    app.register_blueprint(index_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from app.folder import bp as folder_bp
    app.register_blueprint(folder_bp)

    # on 404 error
    @app.errorhandler(404)
    def request_file_not_found(e):
        return f"<h1>{request.url} не найден</h1>"

    @app.route('/favicon.ico/')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', "imgs"), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @app.route('/pdf')
    def pdf():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'Реквизиты счёта.pdf',
                                   mimetype='application/pdf')

    return app
