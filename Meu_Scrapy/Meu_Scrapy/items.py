# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json    
from collections import OrderedDict


class MeuScrapyItem(scrapy.Item):
    data = scrapy.Field()
    titulo = scrapy.Field()