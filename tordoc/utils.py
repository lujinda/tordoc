#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-10-21 23:12:56
# Filename      : utils.py
# Description   : 
import os

def generate_abspath(_file, *path):
    abs_dir = os.path.dirname(os.path.abspath(_file))
    return os.path.join(abs_dir, *path)

