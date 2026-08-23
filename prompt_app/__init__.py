from flask import Flask

from .config import Config
from .db import init_app as init_db
from .extensions import csrf
from .routes.adobe import adobe_bp
from .routes.generators import generators_bp
from .routes.main import main_bp
from .routes.prompts import prompts_bp


def create_app(config_object=Config):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_object)
    csrf.init_app(app)
    init_db(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(prompts_bp)
    app.register_blueprint(generators_bp)
    app.register_blueprint(adobe_bp)
    return app
