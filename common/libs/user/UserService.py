# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  UserService.py.py
@Description    :  
@CreateTime     :  2020/5/13 2:47 下午
------------------------------------
@ModifyTime     :  
"""
import base64
import hashlib, random, string


class UserService:

    @staticmethod
    def geneAuthCode(user_info=None):
        m = hashlib.md5()
        str = '%s-%s-%s-%s' % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        # 对密码先进行base64再使用哈希加密
        str = '%s-%s' % (base64.encodebytes(pwd.encode('utf-8')), salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ''.join(key_list)
