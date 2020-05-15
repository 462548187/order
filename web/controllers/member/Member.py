# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, redirect, request
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate, ops_render, iPagination
from common.libs.UrlManager import UrlManager
from common.models.log.AppAccessLog import AppAccessLog
from common.models.member.Member import Member
from application import app, db

route_member = Blueprint('member_page', __name__)


@route_member.route("/index")
def index():
    resp_data = {}

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query

    if 'mix_kw' in req:
        # 关键字混合查询
        rule = or_(Member.nickname.ilike('%{0}'.format(req['mix_kw'])), Member.mobile.ilike('%{0}'.format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        # 状态查询
        query = query.filter(Member.status == int(req['status']))

    # 分页
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    member_list = query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['list'] = member_list
    resp_data['pages'] = pages

    resp_data['current'] = index
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("member/index.html", resp_data)


@route_member.route("/info")
def info():
    resp_data = {}
    req = request.args

    uid = int(req.get('id', 0))
    back_url = UrlManager.buildUrl('/member/index')

    if uid < 1:
        return redirect(back_url)

    member_info = Member.query.filter_by(id=uid).first()

    if not member_info:
        return redirect(back_url)

    resp_data['member_info'] = member_info
    resp_data['current'] = 'index'
    return ops_render("member/info.html", resp_data)


@route_member.route("/set", methods=['GET', 'POST'])
def member_set():
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        uid = int(req.get('id', 0))
        back_url = UrlManager.buildUrl('/member/index')

        if uid < 1:
            return redirect(back_url)

        member_info = Member.query.filter_by(id=uid).first()
        if not member_info:
            return redirect(back_url)

        resp_data['member_info'] = member_info
        resp_data['current'] = 'index'
        return ops_render('/member/set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values

    member_id = req['member_id'] if 'member_id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''

    if nickname is None or len(nickname) < 1:  # 判断用户名长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return jsonify(resp)

    if mobile is None or len(mobile) < 11:  # 判断手机长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的手机'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=member_id).first()  # 获取uid，判断是否存在，存在是更新，否则就新增

    if not member_info:
        resp['code'] = -1
        resp['msg'] = '指定的会员不存在'
        return jsonify(resp)

    member_info.nickname = nickname  # 变更用户名
    member_info.mobile = mobile  # 变更手机
    member_info.updated_time = getCurrentDate()

    db.session.add(member_info)  # 增加用户信息
    db.session.commit()  # 统一提交

    return jsonify(resp)


@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html")


# 删除和恢复
@route_member.route('/ops', methods=['POST'])
def ops():
    resq = {'code': '200', 'msg': '操作成功！', 'data': {}}
    req = request.values

    member_id = req['member_id'] if 'member_id' in req else ''
    act = req['act'] if 'act' in req else ''

    if not member_id:
        resq['code'] = -1
        resq['msg'] = '请选择要操作的账号'
        return jsonify(resq)

    if act not in ['remove', 'recover']:
        resq['code'] = -1
        resq['msg'] = '操作有误，请重试'
        return jsonify(resq)

    # 查询用户信息是否存在
    member_info = Member.query.filter_by(id=member_id).first()

    if not member_info:
        resq['code'] = -1
        resq['msg'] = '指定账号不存在'
        return jsonify(resq)

    if act == 'remove':
        member_info.status = 0
    elif act == 'recover':
        member_info.status = 1
    else:
        return False

    member_info.update_time = getCurrentDate()  # 更新操作时间
    db.session.add(member_info)
    db.session.commit()

    return jsonify(resq)


