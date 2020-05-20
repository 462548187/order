# -*- coding: utf-8 -*-
SERVER_PORT = 8999
DEBUG = True

AUTH_COOKIE_NAME = "mooc_food"

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/food_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

SEO_TITLE = "Python Flask构建微信小程序订餐系统"

# 过滤不需要登录url
IGNORE_URLS = [
    "^/user/login"  # 登录地址
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

# 过滤不需要登录url
API_IGNORE_URLS = [
    "^/api"  # 不需要api接口
]

PAGE_SIZE = 20  # 每页显示多少条数据量
PAGE_DISPLAY = 10  # 共显示分页数量
STATUS_MAPPING = {  # 账户搜索状态定义
    "1": "正常",
    "0": "已删除"
}
# 小程序的配置
MINA_APP = {
    'appid': 'wxca67a230b48dacfe',
    'appkey': '5fbe74929aa67db05ca4b0cef5cb164a',
    'paykey': 'cbhvrwnpkoadwxwfi1jwdugn13zymcsp',
    'mch_id': '1341938001',
    'callback_url': '/api/order/callback'
}

# 文件上传配置
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'http://127.0.0.1:8999/'
}

# 上线变量
# RELEASE_VERSION = '20200513001'

PAY_STATUS_MAPPING = {
    "0": "已关闭",
    "1": "已支付",
    "-8": "待付款",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "已关闭",
    "1": "已完成",
    "-8": "待付款",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}
