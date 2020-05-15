# -*- coding: utf-8 -*-
from flask import Blueprint, request
from sqlalchemy import or_

from common.libs.Helper import ops_render, iPagination
from common.models.member.Member import Member
from application import app

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
    return ops_render("member/info.html")


@route_member.route("/set")
def set():
    return ops_render("member/set.html")


@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html")



