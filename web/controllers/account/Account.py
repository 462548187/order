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
from flask import Blueprint, jsonify, redirect, request

from application import app, db
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    req = request.values

    page = int(req['page']) if ('page' in req and req['page']) else 1  # 页码，如果没有默认第1页

    query = User.query

    page_params = {
        'total': query.count(),  # 计算总页数
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': '/account/index'

    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']  # 偏移量
    limit = page * app.config['PAGE_SIZE']  # 每页数量

    user_list = query.order_by(User.uid.desc()).all()[offset: limit]  # 按照uid倒序排列，查询所有数据，计算分页

    resp_data['user_list'] = user_list
    resp_data['pages'] = pages
    return ops_render('/account/index.html', resp_data)


@route_account.route('/info')
def info():
    resp_data = {}
    req = request.values

    uid = int(req.get('id', 0))
    back_url = UrlManager.buildUrl('/account/index')

    if uid < 1:
        return redirect(back_url)

    user_info = User.query.filter_by(uid=uid).first()

    if not user_info:
        return redirect(back_url)

    resp_data['user_info'] = user_info

    return ops_render('/account/info.html', resp_data)


@route_account.route('set', methods=['GET', 'POST'])
def set_page():

    default_pwd = '******'  # 定义个默认密码显示

    if request.method == 'GET':
        resp_data = {}
        req = request.args
        uid = int(req.get('id', 0))
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resp_data['user_info'] = user_info

        return ops_render('/account/set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values

    user_id = req['user_id'] if 'user_id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:  # 判断用户名长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return jsonify(resp)

    if mobile is None or len(mobile) < 11:  # 判断手机长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的手机'
        return jsonify(resp)

    if email is None or len(email) < 1:  # 判断邮箱长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的邮箱'
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:  # 判断登录名
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的登录名'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 6:  # 判断登录密码
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的登录密码'
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != user_id).first()  # 判断用户名是否存在
    if has_in:
        resp['code'] = -1
        resp['msg'] = '该登录名已存在，请重新输入'
        return jsonify(resp)

    user_info = User.query.filter_by(uid=user_id).first()  # 获取uid，判断是否存在，存在是更新，否则就新增
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname  # 变更用户名
    model_user.mobile = mobile  # 变更手机
    model_user.email = email  # 变更邮箱
    model_user.login_name = login_name  # 变更登录名
    model_user.login_salt = UserService.geneSalt()

    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)  # 判断用户是否修改密码，如果修改变更登录密码

    model_user.updated_time = getCurrentDate()

    # app.logger.info(user_info)
    db.session.add(model_user)  # 增加用户信息
    app.logger.info(model_user)
    db.session.commit()  # 统一提交

    return jsonify(resp)
