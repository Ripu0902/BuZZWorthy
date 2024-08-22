import os
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    # SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopementConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir,"../database")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR,"maindb.sqlite3")
    SQLALCHEMY_DATABASE_URI = "sqlite:///maindb.sqlite3"
    DEBUG = True
    SECRET_KEY = 'knlfbuyerwbgjfbneruobv'