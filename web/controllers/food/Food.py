# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from application import app, db
from common.libs.Helper import getCurrentDate, ops_render
from common.models.food.FoodCat import FoodCat

route_food = Blueprint('food_page', __name__)


@route_food.route("/index")
def index():
    return ops_render("food/index.html")


@route_food.route("/info")
def info():
    return ops_render("food/info.html")


@route_food.route("/set", methods=['GET', 'POST'])
def foodSet():
    if request.method == 'GET':

        return ops_render("food/set.html")


@route_food.route("/cat")
def cat():
    resp_data = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == int(req['status']))

    cat_list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()

    resp_data['list'] = cat_list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'

    return ops_render("food/cat.html", resp_data)


@route_food.route("/cat-set", methods=['GET', 'POST'])
def catSet():
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        set_info = None
        if id:
            set_info = FoodCat.query.filter_by(id=id).first()
        resp_data['set_info'] = set_info
        resp_data['current'] = 'cat'

        return ops_render("food/cat_set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values

    set_id = req['set_id'] if 'set_id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    food_cat_info = FoodCat.query.filter_by(id=set_id).first()   # 获取uid，判断是否存在，存在是更新，否则就新增

    if name is None or len(name) < 1:  # 判断用户名长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的分类名称'
        return jsonify(resp)

    if weight is None or weight < 1:  # 判断邮箱长度
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的权重，并且至少要大于1'
        return jsonify(resp)

    if food_cat_info:
        model_food_cat = food_cat_info
    else:
        model_food_cat = FoodCat()
        model_food_cat.created_time = getCurrentDate()

    model_food_cat.name = name  # 变更用户名
    model_food_cat.weight = weight  # 变更邮箱
    model_food_cat.updated_time = getCurrentDate()
    db.session.add(model_food_cat)  # 增加用户信息
    db.session.commit()  # 统一提交

    return jsonify(resp)  # 更改成功
