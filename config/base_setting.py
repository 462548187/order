# -*- coding: utf-8 -*-
SERVER_PORT = 8999
DEBUG = True

AUTH_COOKIE_NAME = "mooc_food"

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/food_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

PAGE_SIZE = 50  # 每页显示多少条数据量
PAGE_DISPLAY = 10  # 共显示分页数量
STATUS_MAPPING = {  # 账户搜索状态定义
    '1': '正常',
    '0': '已删除'
}

# 过滤不需要登录url
IGNORE_URLS = [
    '^/user/login'  # 登录地址
]

IGNORE_CHECK_LOGIN_URLS = [  # 静态文件路径
    '^/static',
    '^/favicon.ico'
]

# 上线变量
# RELEASE_VERSION = '20200513001'
