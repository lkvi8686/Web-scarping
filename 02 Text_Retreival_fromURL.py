# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:34:12 2020
@author: Nabha Subramanya
"""

import newspaper as npr
import pandas as pd
#from bs4 import BeautifulSoup
#from urllib.request import urlopen

#from datetime import datetime as dt

fname = 'travel clinic'
x = pd.read_csv('C:\\Users\\Nabha Subramanya\\Documents\\Projects\\MonkeyPox\\FINAL\\'+fname+'.csv')
x.shape
x.columns = ['slno','url']
x = x['url']
#dcont=[]
#keyw = []
#keywrddf = []
#titledf = []



fin_df = []
#url = "http://www.pmlive.com/pharma_news/gsk_divests_travel_vaccines_to_bavarian_nordic_as_part_of_strategic_refocus_1321293?sa=X&ved=2ahUKEwjQ6YbA9PPmAhUzxzgGHT50C7sQxfQBMAF6BAgHEAE"
for url in x:
    try:    
        dc = npr.Article(url)
        dc.download()
        dc.parse()
        dc.nlp() 
#        dcont.append(dc.text)
#        keyw.append(dc.keywords)
#        dauth = dc.authors
#        authdf.append(dauth)
#        dpdate = dc.publish_date
#        datedf.append(dpdate)
#        print(url, dc.keywords, sep = '|')
        fin_df.append([url,dc.text,dc.keywords,dc.authors,dc.publish_date])
    except Exception:
        continue

#titl_df = []
#for url in x:
#    try:
#        soup = BeautifulSoup(urlopen(url))
#        print(soup.title.string)
#        titl_df.append([url,soup.title.string])
#    except:
#        continue
#
#titl_df = pd.DataFrame(titl_df)
#titl_df.columns = ['url','Title']   
    
fin_df = pd.DataFrame(fin_df)
fin_df.columns = ['url','content','keywords','authors','publishDate']

#joindf = fin_df.join(titl_df, on = 'url')
#joindf = fin_df.set_index('url').join(titl_df.set_index('url'))
#joindf.to_csv(fname+'_Parsed.csv')
fin_df.to_csv(fname+'_Parsed.csv')