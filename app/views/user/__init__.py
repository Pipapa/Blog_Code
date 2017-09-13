# 存放其他网页
from flask import Blueprint

# 蓝图类
user = Blueprint('user',__name__,
    )

from . import views