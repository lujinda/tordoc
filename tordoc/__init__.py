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

__all__ = ['tor_handlers']

def router(url_prefix = '/', kwargs = None):
    kwargs = kwargs or {}
    debug_url = os.path.join(url_prefix, 'debug')
    debug_static_url = os.path.join(debug_url, 'static/')
    kwargs['static_url_prefix'] = debug_static_url
    tor_handlers = [
        (r'%s' % (debug_url, ), TorDebugHandler, kwargs),
        (r'%s(.*)' % (debug_static_url), TorStaticFileHandler, {'path': generate_abspath(__file__, 'static/')}),
        ]

    return tor_handlers

