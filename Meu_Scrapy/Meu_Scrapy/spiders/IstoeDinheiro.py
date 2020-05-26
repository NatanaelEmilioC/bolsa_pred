# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import datetime
import json

class BraziliantimesSpider(scrapy.Spider):
    #import ipdb; ipdb.set_trace()
    name = 'IstoeDinheiro'
    allowed_domains = ['istoedinheiro.com.br']
    start_urls = ['https://www.istoedinheiro.com.br/categoria/negocios/']

    
    custom_settings={
       #'FEED_URI':"brazilian_times_%(time)s.json",
       'FEED_URI':"istoe_dinheiro_%(time)s.json",
       'FEED_FORMAT': 'json', 
       #'FEED_EXPORT_FIELDS': ["news"]

    }
    
    def parse(self, response):
        
        #links = response.xpath('//article//h3//a/@title').getall()
        #datas = response.xpath('//article//a//time').getall()  

        titulo =response.xpath("//article//h3//a/@title").extract()
        data =response.xpath("//article//a//time").extract()
        
        data_formatada = [datetime.datetime.strptime(((x.split())[-2]).split(">")[-1],'%d/%m/%Y').date() for x in data]

        row_data=zip(data_formatada, titulo)

        #Making extracted data row wise
        for item in row_data:
        #create a dictionary to store the scraped info
            scraped_info = {            
                'data' : item[0],
                'titulo' : item[1],
            }

            #yield or give the scraped info to Scrapy
            yield scraped_info
       
        
        conteudo = open('istoe_dinheiro_ordenado_teste.json').read()
        ultima_atualizacao = [item.get('data') for item in json.loads(conteudo)]

        if ultima_atualizacao[-1] != data_formatada[0].strftime('%Y-%m-%d'):
            next_page_url = response.css('a.next::attr(href)').get()
            yield scrapy.Request(
                response.urljoin(next_page_url),
                callback=self.parse,
                )
