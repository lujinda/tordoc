#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-10-19 17:38:27
# Filename      : tordoc.py
# Description   : 
from __future__ import print_function, unicode_literals
from tornado.web import RequestHandler, HTTPError, StaticFileHandler
import os
from urlparse import urljoin
from .utils import generate_abspath

class DocParserError(Exception):
    pass

class DocPaser(object):
    def __init__(self, raw_data = None):
        self.raw_data = raw_data

    def parse(self, raw_data = None):
        raw_data = raw_data or self.raw_data
        if not raw_data:
            return raw_data

        current_fork = tree = {}
        parent_line = None
        last_node = None

        for line in raw_data.split('\n'):
            if self.is_space_line(line):
                continue
            key, value = self.parse_line(line)

            # 判断是否进入了子节点，如果不是，则表示是在父节点的
            if parent_line == None or self.entry_child_node(line, parent_line) == False:
                if last_node and (not current_fork):
                    tree[last_node] = self.parse_line(parent_line)[1]
                current_fork = tree.setdefault(key, {})
                last_node = key
                parent_line = line
            else:
                current_fork[key] = value

        return tree

    def entry_child_node(self, line, last_line):
        return self.get_line_indent(line) > self.get_line_indent(last_line)

    def is_space_line(self, line):
        return not bool(line.strip())

    def parse_line(self, line):
        if ':' not in line:
            raise DocParserError

        return [item.strip() for item in line.split(':', 1)]

    def get_line_indent(self, line):
        return len(line) - len(line.lstrip())


def parse_doc(raw_doc):
    if not raw_doc:
        return None
    doc_parser = DocPaser(raw_doc)
    try:
        return doc_parser.parse()
    except DocParserError:
        return None

class TorDebugHandler(RequestHandler):
    def get(self):
        api_docs = self.generate_api_docs()
        api_module_tree = api_docs.keys()
        self.render('doc.html', api_docs = api_docs, 
                api_module_tree = api_module_tree, 
                db_tables = self.db_tables)

    def initialize(self, static_url_prefix, public_response_params = None, api_description = None, tables = None, **kwargs):
        self.static_url_prefix = static_url_prefix
        self.public_response_params = public_response_params or {}
        self.api_description = api_description
        self.db_tables = tables

    @property
    def filter_handlers(self):
        return ('StaticFileHandler', )

    @property
    def allow_parse_method_list(self):
        return ('GET', 'POST', 'DELETE', 'PUT', 'PATCH')

    def generate_api_docs(self):
        handlers = self.get_handlers()
        api_docs = {}
        for url, handler in handlers:
            api_doc = self.generate_handler_api_doc(handler)
            if not api_doc:
                continue
            module_name = handler.__module__
            _module = __import__(module_name, fromlist = [module_name])
            module_doc = getattr(_module, 'API_MODULE_DOC', None)
            if module_doc:
                module_name += '(%s)' % (module_doc, )

            api_docs.setdefault(module_name, 
                    []).append((url, handler, api_doc))

        return api_docs

    def generate_handler_api_doc(self, handler):
        handler_api_doc = []
        for method_name in self.allow_parse_method_list:
            method = getattr(handler, method_name.lower())
            raw_doc = method.__doc__
            api_doc = parse_doc(raw_doc)
            if (not api_doc) or ('restapi' not in api_doc):
                continue
            api_doc['method'] = method_name
            handler_api_doc.append(api_doc)

        return handler_api_doc

    def get_handlers(self):
        """获取所有的handlers,格式[(url, handler), ...]"""
        handlers = []
        for urlspec in self.application.handlers[0][1]:
            re_url, handler = urlspec.regex, urlspec.handler_class
            if handler.__name__ in self.filter_handlers:
                continue
            handlers.append((re_url.pattern[:-1], handler))

        return handlers

    def render(self, path, *args, **kwargs):
        path = self.get_template_abspath(path)
        kwargs['api_description'] = self.api_description
        kwargs['cat_response_params'] = self.cat_response_params
        kwargs['generate_sql'] = self.generate_sql
        super(TorDebugHandler, self).render(path, *args, **kwargs)

    def generate_sql(self, table_name, table_columns):
        _table_columns = []
        for keys in table_columns:
            column_attr = len(keys) == 4 and keys[3] or ''
            _table_columns.append("%s %s %s" % (keys[0], keys[1].upper(),
                column_attr))

        sql = 'CREATE TABLE %s (%s);' % (table_name, 
                ', '.join(_table_columns))

        return sql

    def cat_response_params(self, response_params = None):
        if not response_params:
            return self.public_response_params

        response_params = response_params or {}
        for param_name, param_value in self.public_response_params.items():
            if param_name in response_params:
                response_params[param_name] = param_value + ' ' + response_params[param_name]
            else:
                response_params[param_name] = param_value

        return response_params

    def get_static_abspath(self, file_path):
        return generate_abspath(__file__, self.static_path, file_path)

    def get_template_abspath(self, file_path):
        return generate_abspath(__file__, self.template_path, file_path)

    def static_url(self, path):
        return urljoin(self.static_url_prefix, path)

    @property
    def static_path(self):
        return 'static/'

    @property
    def template_path(self):
        return 'template/'

class TorStaticFileHandler(StaticFileHandler):
    pass

