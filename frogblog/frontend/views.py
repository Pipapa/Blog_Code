import os
from flask import Blueprint,send_from_directory
from flask_login import login_required

from frogblog import db,login_manager
from frogblog.config import Config
from frogblog.models import User,Article,Category,Tag,Comment

frontend = Blueprint('user',__name__)

@frontend.route('/',defaults={'path':''})
@frontend.route('/<path:path>')
def index(path):
    return open(Config.INDEX+'index.html').read()

@frontend.route('/static/<string:dir>/<string:filename>')
def static(dir,filename):
    return send_from_directory(Config.STATIC+dir,filename)