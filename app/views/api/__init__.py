# 存放api有关网页,返回json数据
from flask import Blueprint

api = Blueprint('api',__name__)

from . import views