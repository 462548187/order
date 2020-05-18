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
from flask import g, jsonify, request

from common.libs.member.MemberService import MemberService
from common.models.member.Member import Member

"""
api认证
"""


@app.before_request
def before_request():
    api_ignore_urls = app.config['API_IGNORE_URLS']

    path = request.path
    if '/api' not in path:
        return

    member_info = check_member_login()
    g.member_info = None
    if member_info:
        g.member_info = member_info

    pattern = re.compile('%s' % '|'.join(api_ignore_urls))
    if pattern.match(path):
        return

    if not member_info:
        resp = {'code': -1, 'msg': '未登录', 'data': {}}
        return jsonify(resp)

    return


"""
判断用户是否已经登录
"""


def check_member_login():
    auth_cookie = request.headers.get('Authorization')

    if auth_cookie is None:  # 如果页面中没有cookies
        return False

    auth_info = auth_cookie.split('#')  # de0e0f7e2848bcbb9e00fd5458393257#1

    app.logger.info(auth_info)
    if len(auth_info) != 2:  # 不是标准的cookies
        return False

    try:
        member_info = Member.query.filter_by(id=auth_info[1]).first()  # 查询能否和数据库中cookies对应
    except Exception as e:
        return False  # 查不到接收异常为False

    if member_info is None:  # 有效性检验，但我感觉没必要，应该会有值，因为数据表设置的是非空，不过显得更加严谨
        return False

    if auth_info[0] != MemberService.geneAuthCode(member_info):  # 如果得到的cookies值和通过我们对数据库中值加密过后的不一样，则是伪造
        return False

    if member_info.status != 1:  # 已登录禁用账号刷新后退出登录
        return False

    return member_info
