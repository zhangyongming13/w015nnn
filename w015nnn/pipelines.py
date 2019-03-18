# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from .settings import collectionname
from w015nnn.spiders.redisopera import RedisOpera
import pymongo, os, redis
from w015nnn.items import W015NnnItem

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


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
        try:
            self.Redis = redis.Redis(host='192.168.1.247', port=6379, db=0)
        except:
            self.Redis = redis.Redis(host='192.168.1.112', port=6379, db=0)

    def process_item(self, item, spider):
        item_db = W015NnnItem()
        item_db['tiezi_name'] = item['tiezi_name']
        item_db['tiezi_link'] = item['tiezi_link']
        item_db['image_urls'] = item['image_urls']
        data_mongodb = dict(item_db)
        self.post.insert(data_mongodb)
        print('帖子：%s的数据写入数据库成功！' % item['tiezi_name'])
        try:
            dir_name = item['tiezi_name']
            # os.getcwd()
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
            return item
        except Exception as e:
            item['tupian_data'] = 'Fail'
            print('保存到redis失败！')
            print(e)
            return item


# class ImagePipeline(ImagesPipeline):
#     def file_path(self, request, response=None, info=None):
#         file_name = request.url.split('/')[-1]
#         image_name = request.meta['item']['tiezi_name']
#         path = image_name + '/' + file_name
#         return path
#
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield Request(image_url, meta={'item':item})
#
#     def item_completed(self, results, item, info):
#         image_path = [x['path'] for ok,x in results if ok]
#         if not image_path:
#             raise DropItem('Item contains no images')
#         return item
