# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  __init__.py
@Description    :  
@CreateTime     :  2020/5/13 12:08 上午
------------------------------------
@ModifyTime     :  
"""

from flask import Blueprint

route_api = Blueprint('api_page', __name__)

from web.controllers.api.Member import *

@route_api.route('/')
def index():
    return 'Mina Api V1.0'
