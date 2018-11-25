#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong

import scrapy

# from spider.chia.chia.items import ChiaItem
import time
from scrapy.loader import ItemLoader

# from spider.chia.chia.items import ChiaItem
from ..items import ChiaItem


class HxSpider(scrapy.Spider):
    name = "hx"
    task_domain = "cn.reuters.com"

    def start_requests(self):
        urls = [
            'https://www.huxiu.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        all_links = set(response.css(".wrap-left .transition::attr(href)").extract())
        print(len(all_links))
        for each in all_links:
            yield response.follow(each, self.parse_detail)
            break

    def parse_detail(self, response):
        title = "".join(response.css(".t-h1::text").extract()).strip()
        content = "".join(response.css('.article-content-wrap p::text').extract())[-50:]
        html_content = "".join(response.css('.article-content-wrap p').extract())
        imgs = response.css(".article-content-wrap img::attr(src)").extract()
        item = ChiaItem(
            title=title,
            content=content,
            html_content=html_content,
            imgs=imgs,
            data=int(time.time())
        )
        yield item

