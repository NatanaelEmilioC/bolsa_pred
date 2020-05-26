"""from googlefinance.get import get_datum

df = get_datum('KRX:005930', period='2M', interval =86400)

print(df)
"""
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize  
import json

#print(pd.read_csv('historico_petr4.csv', delimiter=','))

with open("spiders/istoe.json") as datafile:
    data = json.load(datafile)
dataframe = pd.DataFrame(data)

grouped = dataframe.groupby('data')


#grp = df.groupby('Name') 
for name, group in grouped: 
    print(str(name)) 
    print(str(group)) 
    print() 

#print(grouped.groups)
