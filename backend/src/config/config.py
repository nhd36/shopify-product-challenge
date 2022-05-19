from dotenv import load_dotenv
import os

load_dotenv("./env/.env")


class Config:
    """Get configuration for application in .env file"""
    environment = os.getenv("ENVIRONMENT")

    """Config database"""
    db_conn = f"sqlite:///{os.getcwd()}/src/database/database.db"

    """Config static folder"""
    static_folder = f"{os.getcwd()}/static"

    """JWT Secret Key"""
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")

    """Configure Cache Redis"""
    # cache_use = os.getenv("CACHE_USE")
    # cache_type = os.getenv("CACHE_TYPE")
    # cache_host = os.getenv("CACHE_HOST")
    # cache_port = os.getenv("CACHE_PORT")
    # cache_db = os.getenv("CACHE_DB")
    # cache_url = os.getenv("CACHE_URL")
    # cache_default_timeout = os.getenv("CACHE_DEFAULT_TIMEOUT")
