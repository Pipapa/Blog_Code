import json
from flask import jsonify,url_for
from . import api
from .. import db
from ..models import User,Article,Category,Tag

# 不需要登录api 
@api.route('/api/articles')
def get_articles():
    articles = Article.query.all()
    jsonObj = {'status':'OK'} 
    for article in articles:
        info={}
        info['title']=article.title
        info['url']=url_for('user.articles_index',article_id=article.id)
        info['public_time']=article.public_time.strftime('%B %d %Y - %H:%M:%S')
        info['update_time']=article.update_time.strftime('%B %d %Y - %H:%M:%S')
        jsonObj[str(article.id)]=info
    return jsonify(jsonObj)
# 