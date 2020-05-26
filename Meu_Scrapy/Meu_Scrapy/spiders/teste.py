import scrapy
import numpy as np
import datetime
import json
import os, fnmatch

lista_jsons = fnmatch.filter(os.listdir('.'), '*.json')
print(lista_jsons)
