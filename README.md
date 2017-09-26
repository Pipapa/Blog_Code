# FrogBlog 
### 设计说明
采用RESTful API风格做到前后端分离设计
### 代码结构

### 路由说明
| 方式   |                  URL                                      | 说明                  |
|:------:|:---------------------------------------------------------:|:---------------------:|
| GET    | /api/posts?page=&pre_page=                                | 获取文章列表          | DONE
| POST   | /api/posts                                                | 创建一篇文章          | DONE
| GET    | /api/posts/{id}                                           | 获取一片文章          | DONE
| PUT    | /api/posts/{id}                                           | 更新一篇文章          | DONE
| DELETE | /api/posts/{id}                                           | 删除一篇文章          | DONE
| GET    | /api/tags?key=                                            | 获取标签              | DONE
| GET    | /api/categories?key=                                      | 获取分类              | DONE
| POST   | /api/users                                                | 增加用户              |
| PUT    | /api/users/{name}                                         | 更新用户              | DONE
| DELETE | /api/users/{name}                                         | 删除用户              |
| GET    | /posts/pages/{page}                                       | 展示页面              | DONE
| GET    | /posts/tags/{tag}                                         | 展示标签页            | DONE
| GET    | /posts/categories/{category}                              | 展示分类页            | DONE
| GET    | /posts/{id}                                               | 展示文章　　　　　　　| DONE
| GET    | /admin/login                                              | 后台登录              | DONE
| GET    | /admin                                                    | 后台管理              | DONE
| GET    | /admin/writer                                             | 编辑文章              | DONE
| GET    | /admin/writer/{id}                                        | 修改文章              | DONE


