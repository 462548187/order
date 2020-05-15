# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  MemberService.py
@Description    :  
@CreateTime     :  2020/5/15 4:23 下午
------------------------------------
@ModifyTime     :  
"""
import hashlib
import json
import random
import string

import requests

from application import app


class MemberService:

    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = '%s-%s-%s' % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ''.join(key_list)

    @staticmethod
    def getWeChatOpenId(code):
        # 获取微信用户的openid
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code' \
            .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid