from flask import Blueprint,jsonify,request,redirect,url_for,request,abort,send_file
from flask_login import login_required

from frogblog import db,login_manager
from frogblog.config import Config
from frogblog.models import User,Article,Category,Tag,Comment

frontend = Blueprint('user',__name__)

@frontend.route('/',defaults={'path':''})
@frontend.route('/<path:path>')
def index(path):
    return send_file(Config.INDEX,'index.html',as_attachment=True)

@frontend.route('/static/<string:dir>/<string:filename>')
def static(dir,filename):
    return send_file(Config.INDEX+'/static/'+dir+'/'+filename)