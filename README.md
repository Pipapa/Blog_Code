## 前后端分离风格
后端采用python(flask)提供API接口,用于数据处理
前端采用Vue,使用vue-router提供路由功能(flask只需要提供一个路由,其余由前端处理)

## RESTful API
REST是万维网软件架构的一种设计风格,目的在于方便不同软件/程序在网络中互相传递信息   
REST(Representational State Transfer,具象状态传输,表现层状态转移)   
Representational: 资源的一种表现形式(json,xml,jpeg,etc..)   
State Transfer: 状态的变化.通过HTTP动词实现(GET,POST,PUT,DELETE)   
通过 名词(资源)+动词(操作) 的方式来操作服务器资源   
连接中不应该出现动词形式,应该全部是名词形式   
由HTTP方法(method)担任动词形式表明操作类型   

## 博客API设计
| 方式   |                  URL                                      | 说明                  |
|:------:|:---------------------------------------------------------:|:---------------------:|
| GET    | /api/info                                                 | 获取分类/标签         | 
| GET    | /api/posts?page=&pre_page=                                | 获取文章列表          | 
| POST   | /api/posts                                                | 创建一篇文章          | 
| GET    | /api/posts/{id}                                           | 获取一片文章          | 
| PUT    | /api/posts/{id}                                           | 更新一篇文章          | 
| DELETE | /api/posts/{id}                                           | 删除一篇文章          | 
| GET    | /api/tags/{key}                                           | 获取标签              |
| GET    | /api/categories/{key}                                     | 获取分类              |
| POST   | /api/users                                                | 增加用户              |
| PUT    | /api/users/{name}                                         | 更新用户              |
| DELETE | /api/users/{name}                                         | 删除用户              |

