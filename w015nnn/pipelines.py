# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from w015nnn.spiders.redisopera import RedisOpera
import pymongo, os, redis
from w015nnn.items import W015NnnItem
collectionname = '75aeae'


class W015NnnPipeline(object):
    def __init__(self):
        # 初始化mongodb的连接
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]
        # 初始化redis的连接操作
        self.Redis = redis.Redis(host='192.168.1.247',port=6379,db=0)

    def process_item(self, item, spider):
        item_db = W015NnnItem()
        item_db['tiezi_name'] = item['tiezi_name']
        item_db['tiezi_link'] = item['tiezi_link']
        item_db['tupian_link'] = item['tupian_link']
        data_mongodb = dict(item_db)
        print('帖子：%s的数据写入数据库成功！' % item['tiezi_name'])
        self.post.insert(data_mongodb)
        try:
            dir_name = item['tiezi_name']
            if not os.path.exists(dir_name):  # 创建每个帖子对应的图片存放文件夹
                os.mkdir(dir_name)
            else:  # 已经存在文件夹，所以数据已经保存过了
                return item
            num = 1
            for each in item['tupian_data']:  # 讲图片数据保存到硬盘中
                file_name = str(num)
                num = num + 1
                with open('{}//{}.jpg'.format(dir_name, file_name), 'wb') as f:
                    f.write(each)
            print('帖子：%s的图片保存成功' % item['tiezi_name'])
            item['tupian_data'] = 'Success'
        except Exception as e:
            item['tupian_data'] = 'Fail'
            print('保存到本地失败！')
            print(e)
        try:
            self.Redis.sadd(collectionname, item['tiezi_link'])  # 将已经爬取过的链接插入redis
            print('帖子链接插入Redis成功！')
        except Exception as e:
            item['tupian_data'] = 'Fail'
            print('保存到redis失败！')
            print(e)
        return item
