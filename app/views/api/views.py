import json
from flask import jsonify,url_for,request,abort
from . import api
from ... import db
from ...models import User,Article,Category,Tag,Comment


def check_args(args):                                        # 检查数字参数是否合法
    for arg in args:
        if arg is not None and arg.isdigit() is False:
            return 1
    return 0

@api.route('/api/test')
def test():
    return 'true'

@api.route('/api/article')                                   # 获取文章统计
def query_article():
    jsonObj = {}
    error_key = jsonify(error = 'The key is not valid')
    # 获取参数 
    limit = request.args.get('limit')
    page = request.args.get('page')
    pre_page = request.args.get('pre_page')
    tag = request.args.get('tag')
    category = request.args.get('category')
    # 处理参数 str to int 
    if check_args([limit,page,pre_page]):
       return error_key
    # 默认值
    num_of_article = Article.query.count()                                      # 总文章量 
    # 查询参数
    query = Article.query.order_by(Article.update_time.desc())
    if tag is not None:                                                         # 标签查询
        query = query.filter(Article.tags.any(name=tag))

    if category is not None:                                                    # 分类查询
        query = query.join(Category).filter(Category.name == category)

    if page is not None:                                                        # 分页
        page = int(page)
        if pre_page is None:
            pre_page = 5
        else:
            pre_page = int(pre_page)
        if pre_page <= 0 or page <=0:
            return error_key
        _start = (page-1) * pre_page                                            # 计算/分页
        query = query.limit(pre_page).offset(_start)
    
    if limit is not None:                                                       # 限制大小/非分页情况下
        limit = int(limit)
        if page is None:
            query = query.limit(limit)
    
    # 查询
    articles = query.all() 
    # 返回参数
    if len(articles) == 0:                                                      # 没有文章
        abort(404)
    else:
        jsonObj['data'] = []
        for article in articles:
            jsonObj['data'].append(article.get_info())                          # 文章信息加入列表
        jsonObj['page'] = page                                                  # 分页
        jsonObj['num_of_page']=jsonObj['has_next'] = jsonObj['has_prev'] = None
        if page:                                                                # 检测上下页
            if num_of_article%pre_page:
                num_of_page = int(num_of_article/pre_page) + 1
            else:
                num_of_page = int(num_of_article/pre_page)
            jsonObj['num_of_page'] = num_of_page
            if page > 1:
                jsonObj['has_prev'] = True
            if page < num_of_page:
                jsonObj['has_next'] = True
        return jsonify(jsonObj)
  
@api.route('/api/article/<int:id>')                          # 获取文章详情
def get_article(id):
    jsonObj = {}
    article = Article.query.get_or_404(id)
    jsonObj['data'] = article.get_detail()
    article.add_view()
    return jsonify(jsonObj)
@api.route('/api/tag')                                       # 获取全部标签
def get_tag():
    jsonObj = {}
    jsonObj['data'] = []
    tags = Tag.query.all()
    for tag in tags:
        jsonObj['data'].append(tag.get_info())
    return jsonify(jsonObj)
@api.route('/api/category')                                  # 获取全部分类
def get_category():
    jsonObj = {}
    jsonObj['data'] = []
    categories = Category.query.all()
    for category in categories:
        jsonObj['data'].append(category.get_info())
    return jsonify(jsonObj)
@api.route('/api/article/create',methods=['POST'])           # 创建一篇文章
def create_article():
    if request.method == 'POST':
        data = request.get_json()
        # 判断合法
        if 'method' in data.keys() and data['method'] == 'create':
            # 获取到数据
            info = data['data']
            article = Article(title=info['title'],content=info['content'],
                            category=info['category'],tags=info['tag'])
            db.session.add(article)
            db.session.commit()
    return 'true'

@api.route('/api/article/put',methods=['POST'])              # 更新一篇文章
def put_article():
    if request.method == 'POST':
        data = request.get_json()
        if 'method' in data.keys() and data['method'] == 'put':
            data = data['data']
            article = Article.query.get_or_404(data['id'])
            article.put(data)
    return 'true'

@api.route('/api/article/delete',methods=['POST'])           # TODO 删除一篇文章
def delete_article():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'method' in data.keys() and data['method'] == 'delete':
            data = data['data']
            article = Article.query.get_or_404(data['id'])
            db.session.delete(article)
            db.session.commit()
    return 'true'


@api.errorhandler(404)                                       # 404
def page_not_found(e):
    jsonObj = {}
    jsonObj['error'] = 'No article be found'
    return jsonify(jsonObj)