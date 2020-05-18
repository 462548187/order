# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  ErrorInterceptor.py
@Description    :  
@CreateTime     :  2020/5/15 9:45 上午
------------------------------------
@ModifyTime     :  
"""
from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService


@app.errorhandler(404)
def error_404(e):
    LogService.addErrorLog(str(e))
    return ops_render('error/error.html', {'status': 404, 'msg': '很抱歉！您访问的页面不存在'})
