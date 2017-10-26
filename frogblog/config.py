import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG=True
    JSON_SORT_KEYS=False
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'FrogBlog.db')
    SECRET_KEY=os.urandom(24)
    INDEX=basedir+'/templates/'
    STATIC=basedir+'/statics/'