from flask import Blueprint,render_template,jsonify,request,redirect,url_for,request,abort
from flask_login import login_required

from frogblog import db,login_manager
from frogblog.models import User,Article,Category,Tag,Comment

frontend = Blueprint('user',__name__)

@frontend.route('/')
def index():
    return render_template('index.html')