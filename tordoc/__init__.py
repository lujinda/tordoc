#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-10-19 20:57:37
# Filename      : __init__.py
# Description   : 

from .handler import TorDebugHandler, TorStaticFileHandler
import os
from .utils import generate_abspath
from functools import wraps
import base64

__all__ = ['router']

def wrap_base_authenticated(method, username, password):
    correct_authorization = 'Basic ' + base64.b64encode("{username}:{password}".format(
        username = username, password = password))
    @wraps(method)
    def wrap(handler, *args, **kwargs):
        authorization = handler.request.headers.get('Authorization', None)
        if not (authorization and authorization == correct_authorization):
            handler.set_status(401)
            handler.set_header('WWW-Authenticate',
                    'Basic realm="tordoc auth"')
            return

        return method(handler, *args, **kwargs)

    return wrap

def router(url_prefix = '/', kwargs = None):
    kwargs = kwargs or {}
    username = kwargs.pop('username', 'admin')
    password = kwargs.pop('password', 'admin')
    if kwargs.pop('login', False): # if the 'login' is True, said  access need base authenticated
        TorDebugHandler.get = wrap_base_authenticated(
                TorDebugHandler.get,
                username,
                password)

    debug_url = os.path.join(url_prefix, 'debug')
    debug_static_url = os.path.join(debug_url, 'static/')
    kwargs['static_url_prefix'] = debug_static_url
    tor_handlers = [
        (r'%s' % (debug_url, ), TorDebugHandler, kwargs),
        (r'%s(.*)' % (debug_static_url), TorStaticFileHandler, {'path': generate_abspath(__file__, 'static/')}),
        ]

    return tor_handlers

