# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:48:10 2020

@author: Nabha Subramanya
"""
try: 
	from googlesearch import search 
except ImportError: 
	print("No module named 'google' found") 

import pandas as pd
import re

# to search and find Google Links 
query = "travel clinic"
x = []
for j in search(query, num=100,stop=1000, pause=5, country="UnitedStates", tpe = 'nws'):
    x.append(j)

x = pd.DataFrame(x)
x.columns = ['url']

x['url'] = x['url'].apply(lambda x: re.sub("EAE","",x))
x['url'] = x['url'].apply(lambda x: re.sub("EAQ","",x))

test_list = x['url'][::2]

y = pd.DataFrame(test_list)
y.to_csv(query+'.csv')

