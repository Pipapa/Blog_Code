import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG=True
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'FrogBlog.db')