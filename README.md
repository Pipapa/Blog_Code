## 前后端分离风格
后端采用python(flask)提供API接口,用于数据处理
前端采用Vue,使用vue-router提供路由功能(flask只需要提供一个index路由,其余由前端处理)

## 博客RESTful API设计
| 方式   |                  URL                                      | 说明                 |
|:------:|:---------------------------------------------------------:|:-------------------:|
| GET    | /api/info                                                 | 获取分类/标签         | 
| GET    | /api/posts                                                | 获取文章列表          | 
| POST   | /api/posts                                                | 创建一篇文章          | 
| GET    | /api/posts/{id}                                           | 获取一片文章          | 
| PUT    | /api/posts/{id}                                           | 更新一篇文章          | 
| DELETE | /api/posts/{id}                                           | 删除一篇文章          | 
| POST   | /api/users                                                | 增加用户             |
| PUT    | /api/users/{name}                                         | 更新用户             |
| DELETE | /api/users/{name}                                         | 删除用户             |