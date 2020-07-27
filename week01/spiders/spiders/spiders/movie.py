# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def parse(self, response):
        pass
