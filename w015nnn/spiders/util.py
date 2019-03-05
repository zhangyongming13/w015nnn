# -*- coding: utf-8 -*-

import re


class RedisCollection(object):
    def __init__(self, OneUrl):
        self.collectionname = OneUrl

    def getCollectionname(self):
        if self.IndexAllUrls() is not None:
            name = self.IndexAllUrls()
        else:
            name = 'publicurls'

    def IndexAllUrls(self):
        allurls = []
