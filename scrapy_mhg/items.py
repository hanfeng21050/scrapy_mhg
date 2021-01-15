# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyMhgItem(scrapy.Item):
    name = scrapy.Field()  # 漫画名称
    title = scrapy.Field()  # 章节
    page_url = scrapy.Field()  # 章节地址
    image_urls = scrapy.Field()  # 图片
