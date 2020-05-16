# -*- coding: utf-8 -*-
import time
from application import app


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = app.config.get('RELEASE_VERSION')
        ver = "%s" % (int(time.time())) if not release_version else release_version
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        # url = '域名' + '图片前缀' + 'key'
        app_config = app.config['APP']
        upload_config = app.config['UPLOAD']['prefix_url']
        url = app_config['domain'] + upload_config + path
        return url
