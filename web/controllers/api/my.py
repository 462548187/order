# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  cart.py
@Description    :  
@CreateTime     :  2020/5/18 4:28 下午
------------------------------------
@ModifyTime     :  
"""
import json

from flask import g, jsonify, request

from application import app, db
from common.libs.UrlManager import UrlManager
from common.libs.pay.WeChatService import WeChatService
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.member.OauthMemberBind import OauthMemberBind
from web.controllers.api import route_api
from common.models.food.Food import Food
from common.libs.Helper import selectFilterObj, getDictFilterField


@route_api.route("/my/order")
def myOrderList():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values

    status = int(req['status']) if 'status' in req else 0
    query = PayOrder.query.filter_by(member_id=member_info.id)

    if status == -8:  # 待付款
        query = query.filter(PayOrder.status == -8)
    elif status == -7:  # 待发货
        query = query.filter(PayOrder.status == 1, PayOrder.status == -7, PayOrder.comment_status == 0)
    elif status == -6:  # 待确认
        query = query.filter(PayOrder.status == 1, PayOrder.status == -6, PayOrder.comment_status == 0)
    elif status == -5:  # 待评价
        query = query.filter(PayOrder.status == 1, PayOrder.status == -5, PayOrder.comment_status == 0)
    elif status == 1:  # 已完成
        query = query.filter(PayOrder.status == 1, PayOrder.status == 1, PayOrder.comment_status == 1)
    else:
        query = query.filter(PayOrder.status == 0)

    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    data_pay_order_list = []

    if pay_order_list:
        pay_order_ids = selectFilterObj(pay_order_list, "id")
        pay_order_item_list = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        food_ids = selectFilterObj(pay_order_item_list, "food_id")
        food_map = getDictFilterField(Food, Food.id, "id", food_ids)

        pay_order_item_map = {}
        if pay_order_item_list:
            for item in pay_order_item_list:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []

                tmp_food_info = food_map[item.food_id]
                pay_order_item_map[item.pay_order_id].append({
                    "id": item.id,
                    "food_id": item.food_id,
                    "quantity": item.quantity,
                    "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
                    "name": tmp_food_info.name
                })

        for item in pay_order_list:
            tmp_data = {
                "status": item.pay_status,
                "status_desc": item.status_desc,
                "date": item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "order_number": item.order_number,
                "order_sn": item.order_sn,
                "note": item.note,
                "total_price": str(item.total_price),
                "goods_list": pay_order_item_map[item.id]
            }
            data_pay_order_list.append(tmp_data)

    resp['data']['pay_order_list'] = data_pay_order_list
    return jsonify(resp)


@route_api.route('/order/pay', methods=['POST'])
def orderPay():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试"
        return jsonify(resp)

    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试"
        return jsonify(resp)

    config_mina = app.config['MINA_APP']
    notify_url = app.config['APP']['domain'] + config_mina['callback_url']

    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    data = {
        "appid": config_mina['appid'],
        "mch_id": config_mina['mch_id'],
        "nonce_str": target_wechat.get_nonce_str(),
        "body": "官方商城",
        "out_trade_no": pay_order_info.order_sn,
        "total_fee": int(pay_order_info.total_price * 100),
        "notify_url": notify_url,
        "trade_type": "JSAPI",
        "openid": oauth_bind_info.openid
    }

    pay_info = target_wechat.get_pay_info(data)

    # 保存prepay_id 为了后面发模板消息
    pay_order_info.prepay_id = pay_info['prepay_id']
    db.session.add(pay_order_info)
    db.session.commit()

    resp['data']['pay_info'] = pay_info

    return jsonify(resp)
