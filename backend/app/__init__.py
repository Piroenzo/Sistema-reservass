from flask import Flask
from flask_cors import CORS

from .config import get_config
from .extensions import db, migrate, jwt
from .routes.auth import auth_bp
from .routes.businesses import business_bp
from .routes.services import service_bp
from .routes.schedules import schedule_bp
from .routes.appointments import appointment_bp
from .routes.stats import stats_bp


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(business_bp, url_prefix="/api/businesses")
    app.register_blueprint(service_bp, url_prefix="/api")
    app.register_blueprint(schedule_bp, url_prefix="/api/scheduling")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")

    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    return app
