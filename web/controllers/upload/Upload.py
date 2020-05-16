# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  Upload.py
@Description    :  
@CreateTime     :  2020/5/16 6:26 下午
------------------------------------
@ModifyTime     :  
"""
import json
import re

from flask import Blueprint, jsonify, request
from common.libs.UploadService import UploadService

from application import app
from common.libs.UrlManager import UrlManager

route_upload = Blueprint('upload_page', __name__)

'''
参考文章：https://segmentfault.com/a/1190000002429055
'''


@route_upload.route('/ueditor', methods=['GET', 'POST'])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''

    if action == 'config':
        root_path = app.root_path
        config_path = f'{root_path}/web/static/plugins/ueditor/upload_config.json'
        with open(config_path, encoding="utf-8") as fp:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)

    if action == 'uploadimage':
        return uploadImage()

    return "upload"


def uploadImage():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
    file_target = request.files
    upfile = file_target['upfile'] if 'upfile' in file_target else None

    if upfile is None:
        resp['state'] = '上传失败'
        return jsonify(resp)

    ret = UploadService.uploadByFile(upfile)

    if ret['code'] != 200:
        resp['state'] = "上传失败：" + ret['msg']
        return jsonify(resp)

    resp['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])

    return jsonify(resp)


def listImage():
    pass