# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  FoodService.py
@Description    :  
@CreateTime     :  2020/5/19 12:35 上午
------------------------------------
@ModifyTime     :  
"""
from application import db
from common.libs.Helper import getCurrentDate
from common.models.food.Food import Food
from common.models.food.FoodStockChangeLog import FoodStockChangeLog


class FoodService:

    @staticmethod
    def setStockChangeLog(food_id=0, quantity=0, note=''):
        if food_id < 1 or quantity < 1:
            return False
        food_info = Food.query.filter_by(id=food_id).first()

        if not food_info:
            return False

        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        model_stock_change.unit = quantity
        model_stock_change.total_stock = food_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()
        db.session.add(model_stock_change)

        db.session.commit()

        return True
