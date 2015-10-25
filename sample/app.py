#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-10-25 13:40:20
# Filename      : app.py
# Description   : 
from __future__ import print_function, unicode_literals
import tordoc
from tornado.web import RequestHandler, Application
from tornado import httpserver, options, ioloop
from tornado.options import define, options
define('port', type="int", default=1234)

API_MODULE_DOC = '测试登录'

class ApiLoginHandler(RequestHandler):
    def post(self):
        """
        restapi: 登录账号
        warning: 必须要输入正常哦
        request:
            username: 用户名
            password: 密码 
        response:
            uid: 用户uid
        """
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        self.write({'code': 0, 'uid': 111})

if __name__ == "__main__":
    options.parse_command_line()
    
    debug_handler = tordoc.router('/', {'public_response_params':{
        'code': 'api响应状态码'}}) # 这里的'/' 表示url前缀。也就是/debug就是本插件的页面地址。比如是/api，那本插件的页面地址就是/api/debug

    app = Application([('/api/login', ApiLoginHandler)] + debug_handler,
            debug = True)
    server = httpserver.HTTPServer(app, xheaders = True)
    server.listen(options.port)
    ioloop.IOLoop().instance().start()

