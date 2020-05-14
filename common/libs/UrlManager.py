# -*- coding: utf-8 -*-

class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s" % (2020051302033313324433344433334433111)
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)
