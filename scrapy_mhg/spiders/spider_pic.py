# -*- coding: utf-8 -*-
import json
import re
import sys

import dukpy
import lzstring
from scrapy_redis.spiders import RedisSpider

sys.path.append("../")
import scrapy
from scrapy_mhg.items import ScrapyMhgItem

baseURL = "https://www.manhuagui.com"
imgURL = "https://i.hamreus.com"


def get_core_info(html):
    jsSlic = re.search(r">window.*(\(function\(p.*?)</script>", html).group(1)
    coreStr = re.search(r"[0-9],'([A-Za-z0-9+/=]+?)'", jsSlic).group(1)
    decStr = lzstring.LZString.decompressFromBase64(coreStr)
    jsNew = re.sub(r"'[A-Za-z0-9+/=]*'\[.*\]\('\\x7c'\)", "'" + decStr + "'.split('|')", jsSlic)
    sol = dukpy.evaljs(jsNew)
    return json.loads(re.search(r"(\{.*\})", sol).group(1))


def get_dl_setting(html):
    data = get_core_info(html)
    pathURLs = []
    picid = 0
    for pic in data['files']:
        mangaurl = imgURL + data['path'] + pic
        fullurl = mangaurl + "?e=" + str(data['sl']['e']) + "&m=" + data['sl']['m']
        pathURLs.append({"Name": "%05d" % picid, "URL": fullurl})
        picid += 1
    refURL = baseURL + "/comic/" + str(data['bid']) + "/" + str(data['cid']) + ".html"
    return pathURLs


class SpiderPicSpider(RedisSpider):
    name = 'spider_pic_mhg'
    allowed_domains = ['manhuagui.com']
    redis_key = 'mhg:start_urls'

    def parse(self, response):
        # 章节名称
        titles = response.xpath("//div[@class='chapter-list cf mt10'][1]/ul/li/a/@title").extract()

        # 章节url
        urls = response.xpath("//div[@class='chapter-list cf mt10'][1]/ul/li/a/@href").extract()

        # 漫画名
        name = response.xpath("//div[@class='book-title']/h1/text()").extract_first()

        print(name)

        for title, url in zip(titles, urls):
            item = ScrapyMhgItem()
            item['name'] = name
            item['title'] = title
            item['page_url'] = url
            yield scrapy.Request(
                baseURL + url,
                callback=self.get_img,
                meta={"item": item}
            )

    def get_img(self, response):
        item = response.meta['item']
        data = get_dl_setting(response.text)
        image_urls = [x['URL'].replace(".webp", "") + "#" + x['Name'] for x in data]
        item['image_urls'] = image_urls
        yield item
