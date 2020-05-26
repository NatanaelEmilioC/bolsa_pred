# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import datetime
import json

class BraziliantimesSpider(scrapy.Spider):
    #import ipdb; ipdb.set_trace()
    name = 'BrazilianTimes'
    allowed_domains = ['braziliantimes.com']
    start_urls = ['https://www.braziliantimes.com/noticias/economia']

    
    custom_settings={
       #'FEED_URI':"brazilian_times_%(time)s.json",
       'FEED_URI':"brazilian_times.json",
       'FEED_FORMAT': 'json', 
       #'FEED_EXPORT_FIELDS': ["news"]

    }
    
    def parse(self, response):
        
        links = response.xpath(
            '//ul//li/a[re:test(@href, "braziliantimes.com/economia/201")]/@href').getall()
        
        print("links visitados:",links)

        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_new
            )

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        
        #print("Página visitada: " , next_page_url)

        if next_page_url != "/noticias/economia/2":
            yield scrapy.Request(
                response.urljoin(next_page_url),
                callback=self.parse,
                )

    def parse_new(self, response):
        data = (response.css('p.date::text').get().split())[2]
        titulo = str(response.css('h1::text').getall())
        
        datetime_obj = datetime.datetime.strptime(data, '%d/%m/%Y')

        yield{
            'data': datetime_obj.date(),
            'titulo': titulo,
        }
        

    