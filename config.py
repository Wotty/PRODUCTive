import os
import secrets

# Set the base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the configuration class for the app
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Define the configuration class for development
class DevelopmentConfig(Config):
    DEBUG = True


# Define the configuration class for testing
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # Use an in-memory database for testing


# Define the configuration class for production
class ProductionConfig(Config):
    pass


# Create a dictionary that maps configuration names to configuration classes
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
