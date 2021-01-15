# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.images import ImagesPipeline
from . import settings

class ScrapyMhgPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用的，其实这个方法本身就是去发送下载请求的
        request_objs=super(ImagesPipeline, self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item=item
        return request_objs
    # todo 文件重命名
    def file_path(self, request, response=None, info=None):
        #获取文件名
        img_name = request.url[-5:]+".jpg"

        #获取itme中保存的漫画名字
        comic_name = request.item.get('name')
        # 获取item中保存的文件名
        comic_title=request.item.get('title')
        # 获取setting文件中设置的保存路径
        image_store=settings.IMAGES_STORE
        comic_path = os.path.join(image_store,comic_name)
        category_path=os.path.join(comic_path,comic_title)
        image_path=os.path.join(category_path,img_name)
        return image_path