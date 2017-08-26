from flask import jsonify
from . import api
from .. import db
from ..models import User,Article,Category,Tag

# 不需要登录api 
@api.route('/api/articles')
def get_articles():
    articles = Article.query.all()
    for article in articles:
    return 'test'
# 
