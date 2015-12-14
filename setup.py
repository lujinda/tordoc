#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-10-25 12:19:44
# Filename      : setup.py
# Description   : 
from setuptools import setup

setup(
        include_package_data=True,
        name = 'tordoc',
        author = 'tuxpy',
        version = '0.0.4',
        packages = [
            'tordoc', 
            ],
        description = 'generate api doc and online debug',
        )

