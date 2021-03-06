# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  AuthInterceptor.py
@Description    :  
@CreateTime     :  2020/5/13 6:45 下午
------------------------------------
@ModifyTime     :  
"""
import re

from application import app
from flask import g, request, redirect
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.LogService import LogService

"""
拦截器
"""


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']

    path = request.path

    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    if '/api' in path:
        return


    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info

    #加入日志
    LogService.addAccessLog()
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info :
        return redirect( UrlManager.buildUrl( "/user/login" ) )

    return


"""
判断用户是否已经登录
"""


def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None


    if '/api' in request.path:
        app.logger.info(request.path)
        auth_cookie = request.headers.get("Authorization")
        app.logger.info( request.headers.get("Authorization") )
    if auth_cookie is None:  # 如果页面中没有cookies
        return False

    auth_info = auth_cookie.split("#")  # de0e0f7e2848bcbb9e00fd5458393257#1
    if len(auth_info) != 2:   # 不是标准的cookies
        return False

    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()  # 查询能否和数据库中cookies对应
    except Exception as e:
        return False   # 查不到接收异常为False

    if user_info is None:  # 有效性检验，但我感觉没必要，应该会有值，因为数据表设置的是非空，不过显得更加严谨
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):  # 如果得到的cookies值和通过我们对数据库中值加密过后的不一样，则是伪造
        return False

    if user_info.status != 1:  # 已登录禁用账号刷新后退出登录
        return False

    return user_info

