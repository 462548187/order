# -*- coding: utf-8 -*-
from common.libs.Helper import getCurrentDateString


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s" % (getCurrentDateString())
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)
