import os

from dotenv import load_dotenv

load_dotenv()

# Application Settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TIMEZONE = os.getenv("TIMEZONE", "US/Pacific")
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "full-date")
LOCAL_NETWORK = os.getenv("LOCAL_NETWORK", "192.168.0.0/16")

# Flask Settings
DEBUG = os.getenv("DEBUG", False)
TESTING = os.getenv("TESTING", False)
SECRET_KEY = os.getenv("SECRET_KEY", "development-and-testing-key-not-for-production")

# Flask-SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
