# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  Account.py.py
@Description    :  
@CreateTime     :  2020/5/12 10:58 下午
------------------------------------
@ModifyTime     :  
"""
import json

from flask import Blueprint, jsonify, make_response, redirect, render_template, request, g

from application import app, db
from common.libs.Helper import ops_render
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # 如果是get请求直接返回登录页
        return render_template('/user/login.html')

    # 返回默认值
    resp = {'code': 200, 'msg': '登录成功', 'data': {}}

    # 获取返回值
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    # 判断输入用户名
    # 对登录名和登录密码的有效性校验，不论前端是否做校验
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名'
        return jsonify(resp)

    # 判断输入密码
    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的密码'
        return jsonify(resp)

    # 查询数据库用户名
    user_info = User.query.filter_by(login_name=login_name).first()  # 因为登录名是唯一的，所以根据用户名查出的用户信息也是唯一
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码(-1)'
        return jsonify(resp)

    # 查询数据库密码于加密密码对比
    # 通过数据库中的密码与用户填写信息加密后的密码进行校验,我们将这个函数写进通用模块中的UserService
    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码(-2)'
        return jsonify(resp)

    response = make_response(json.dumps(resp))
    # # 设置了cookie，那么就能设置统一拦截器，防止客户端没有cookie而能进入后台，同时定义cookie的加密方式geneAuthCode
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (UserService.geneAuthCode(user_info), user_info.uid),
                        60 * 60 * 24 * 120)  # 生成cookie形式为 16进制加密字符#uid，保存120天
    return response


@route_user.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        return ops_render('/user/edit.html', {'current': 'edit'})

    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:  # 判断用户名长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return jsonify(resp)

    if email is None or len(email) < 1:  # 判断邮箱长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的邮箱'
        return jsonify(resp)

    user_info = g.current_user
    user_info.nickname = nickname  # 变更用户名
    user_info.email = email  # 变更邮箱
    # app.logger.info(user_info)
    db.session.add(user_info)  # 增加用户信息
    db.session.commit()  # 统一提交

    return jsonify(resp)  # 更改成功


@route_user.route('reset-pwd', methods=['GET', 'POST'])
def resetPwd():
    if request.method == 'GET':
        return ops_render('/user/reset_pwd.html', {'current': 'reset-pwd'})

    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    # 获取参数值
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:  # 判断旧密码是否符合规范
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的原密码'
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:  # 判断新密码是否符合规范
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的新密码'
        return jsonify(resp)

    if old_password == new_password:  # 判断新旧密码是否一样
        resp['code'] = -1
        resp['msg'] = '新旧密码不能相同，请重新输入一个新密码！'
        return jsonify(resp)

    user_info = g.current_user
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)  # 加密新密码

    app.logger.info(user_info)
    db.session.commit()  # 统一提交

    response = make_response(json.dumps(resp))
    # # 设置了cookie，那么就能设置统一拦截器，防止客户端没有cookie而能进入后台，同时定义cookie的加密方式geneAuthCode
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (UserService.geneAuthCode(user_info), user_info.uid),
                        60 * 60 * 24 * 120)  # 生成cookie形式为 16进制加密字符#uid，保存120天
    return response


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])  # 移除cookie
    return response
