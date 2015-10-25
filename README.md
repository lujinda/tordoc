## tordoc

这是一款为`tornado`开发的根据request method的doc, 生成api文档, 进行在线debug接口的插件。是自己在开发api过程中，发现写文档太麻烦了。。。前端人员也可以使用这工具看到 response结果，更容易沟通。`本来是打算写gale(我自己的一套web开发框架)的`


## 使用

首先你得开启tornado的`debug`模式, 然后在handlers后面加上tordoc.router([url_prefix], [kwargs])

* `url_prefix`: 指本插件的访问地址__前缀__，默认是/debug，如果url_prefix是/api，则访问地址是/api/debug
* kwargs: 一个参数字段。可以是`public_response_params` 全局响应参数，`api_description` api整体介绍

