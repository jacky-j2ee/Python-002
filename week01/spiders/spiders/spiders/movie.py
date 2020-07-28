# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
from scrapy.selector import Selector

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        movie_count = 10
        for movie in movies:
            if movie_count > 0:
                link = movie.xpath('./a/@href')
                title = movie.xpath('./a/text()')
                item = SpidersItem()
                item['title'] = title.extract_first().strip()
                item['link'] = link.extract_first().strip()
                url = 'https://maoyan.com' + movie.xpath('./a/@href').extract_first().strip()
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)
                movie_count -= 1

    def parse2(self, response):
        item = response.meta['item']
        detail = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        contents = detail[0].xpath('./ul/li[@class="ellipsis"]')
        categories = contents[0].xpath('./a/text()')
        category = ''
        for a in categories:
            category = category + a.get().strip() + ' '
        showtime = Selector(text=contents[2].get()).xpath('//li/text()').get()
        item['category'] = category
        item['showtime'] = showtime
        yield item
