# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  Member.py
@Description    :  
@CreateTime     :  2020/5/15 11:52 上午
------------------------------------
@ModifyTime     :  
"""
import requests, json

from flask import g, request, jsonify

from application import app, db
from web.controllers.api import route_api
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.member.Member import Member
from common.models.food.WxShareHistory import WxShareHistory
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService


@route_api.route('/member/login', methods=['GET', 'POST'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''

    if not code or len(code) < 1:  # 判断code是否合法
        resp['code'] = -1
        resp['msg'] = 'code缺失'
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)

    if openid is None:
        resp['code'] = -1
        resp['msg'] = '调用微信出错'
        return jsonify(resp)

    # 微信获取用户信息
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    """
        判断是否已经存在过，注册了直接返回一些信息
    """

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()

    if not bind_info:  # 判断是否绑定过

        # 注册到数据库表里
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.created_time = model_member.updated_time = getCurrentDate()

        db.session.add(model_member)
        db.session.commit()

        # 建立绑定关系
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.created_time = model_bind.updated_time = getCurrentDate()

        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = '%s#%s' % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}

    return jsonify(resp)


@route_api.route('/member/check-reg', methods=['GET', 'POST'])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''

    if not code or len(code) < 1:  # 判断code是否合法
        resp['code'] = -1
        resp['msg'] = 'code缺失'
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)

    if openid is None:
        resp['code'] = -1
        resp['msg'] = '调用微信出错'
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定微信'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '未查询到绑定信息'
        return jsonify(resp)

    token = '%s#%s' % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}

    return jsonify(resp)


@route_api.route('/member/share', methods=['POST'])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()

    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()

    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname":member_info.nickname,
        "avatar_url":member_info.avatar
    }
    return jsonify(resp)
