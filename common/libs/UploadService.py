# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  UploadService.py
@Description    :  
@CreateTime     :  2020/5/16 6:59 下午
------------------------------------
@ModifyTime     :  
"""
import datetime
import os
import stat
import uuid

from flask import jsonify
from werkzeug.utils import secure_filename
from common.libs.Helper import getCurrentDate
from common.models.Images import Image
from application import app, db


class UploadService:
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '上传成功', 'data': {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1]  # 切割获取扩展名

        if ext not in config_upload['ext']:  # 判断上传的扩展名是否在配置文件内
            resp['code'] = -1
            resp['msg'] = '不允许的扩展类型文件'
            return resp

        root_path = app.root_path + config_upload['prefix_path']
        # 不使用getCurrentDate创建目录，为了保证其他写的可以用，这里改掉，服务器上好像对时间不兼容
        # file_dir = datetime.datetime.now().strftime("%Y%m%d")
        file_dir = getCurrentDate('%Y%m%d')
        save_dir = root_path + file_dir

        if not os.path.exists(save_dir):  # 判断上传日期文件是否存在，不存在创建
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)  # 文件需要777权限

        file_name = str(uuid.uuid4()).replace('-', '') + '.' + ext  # 拼接文件名
        file.save(f'{save_dir}/{file_name}')

        model_image = Image()
        model_image.file_key = file_dir + '/' + file_name
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        # 返回文件名
        resp['data'] = {
            'file_key': model_image.file_key
        }

        return resp
