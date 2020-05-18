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
import decimal
import json

from flask import g, jsonify, request

from common.libs.UrlManager import UrlManager
from web.controllers.api import route_api
from common.models.food.Food import Food


@route_api.route("/order/info", methods=['POST'])
def orderInfo():
    resp = {'code': 200, 'msg': '提交成功', 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None
    member_info = g.member_info
    params_goods_list = []
    if params_goods:
        params_goods_list = json.loads(params_goods)

    food_dic = {}
    for item in params_goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []

    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "pic_url": UrlManager.buildImageUrl(item.main_image),
                "number": food_dic[item.id]
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(tmp_data)

    default_address = {
        "name": "编程浪子",
        "mobile": "12345678901",
        "address": "上海市浦东新区XX",
    }
    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['default_address'] = default_address

    return jsonify(resp)
