# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas
import datetime

class MeuScrapyPipeline(object):

    def open_spider(self, spider):
        self.list_items = []
        self.file = open('istoe.json', 'w')

    def close_spider(self, spider):
        ordered_list = [None for i in range(len(self.list_items))]

        self.file.write("[\n")

        for i in self.list_items:
            ordered_list[int(i['id'])-1] = json.dumps(dict(i))
            
        for i in ordered_list:
            self.file.write("\n,"+str(i)+",\n")

        self.file.write("]\n")
        self.file.close()

    def process_item(self, item, spider):
        self.list_items.append(item)
        return item
