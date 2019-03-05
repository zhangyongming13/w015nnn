# -*- coding: utf-8 -*-
import redis


collectionname = '75aeae'


class RedisOpera:
    def __init__(self):  # 初始化redis的链接
        self.r = redis.Redis(host='192.168.1.247',port=6379,db=1)

    def write(self, value):  # 进行插入的操作
        self.r.sadd(collectionname,value)

    def query(self, value):  # 进行查询的操作
        return self.r.sismember(collectionname, value)
