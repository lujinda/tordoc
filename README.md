## tordoc

这是一款为`tornado`开发的根据request method的doc, 生成api文档, 进行在线debug接口的插件。是自己在开发api过程中，发现写文档太麻烦了。。。前端人员也可以使用这工具看到 response结果，更容易沟通。`本来是打算写gale(我自己的一套web开发框架)的`


## 使用

需要在tornado application中的handlers后面加上tordoc.router([url_prefix], [kwargs])

* `url_prefix`: 指本插件的访问地址__前缀__，默认是`/debug`，如果url_prefix是`/api`，则访问地址是`/api/debug`

* kwargs: 一个参数字典。
    + `public_response_params` 全局响应参数.
    + `api_description` api整体介绍 
    + `login`: 是否需要401认证
    + `username`: 针对上面的login
    + `password`: 针对上面的password

