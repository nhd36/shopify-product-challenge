from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.config.config import Config
from src.database.models import db

app = Flask(__name__)

# Config database
app.config["SQLALCHEMY_DATABASE_URI"] = Config.db_conn
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

# # Config JWT
# app.config["JWT_SECRET_KEY"] = Config.jwt_secret_key
# app.config["JWT_BLACKLISTED_ENABLED"] = True
# app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

# Config CORS
app.config["CORS_HEADERS"] = ["Content-Type"]
app.config["CORS_ORIGIN"] = "*"
app.config["CORS_SUPPORT_CREDENTIALS"] = True

"""
I was implementing caching, but it seems like Replit does not allow to use Redis or any caching service.
"""
# app.config["CACHE_TYPE"] = Config.cache_type
# app.config["CACHE_REDIS_HOST"] = Config.cache_host
# app.config["CACHE_REDIS_PORT"] = Config.cache_port
# app.config["CACHE_REDIS_DB"] = Config.cache_db
# app.config["CACHE_REDIS_URL"] = Config.cache_url
# app.config["CACHE_DEFAULT_TIMEOUT"] = Config.cache_default_timeout

cors = CORS(app=app)


def create_app():
    from .services.inventory.transport import inventory_service

    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)

    app.register_blueprint(inventory_service)

    return app
