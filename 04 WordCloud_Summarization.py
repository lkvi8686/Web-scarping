# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 18:42:07 2020

@author: Nabha Subramanya
"""

from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
import pandas as pd 
import re
import tldextract as domain
from textblob import TextBlob
#import matplotlib.pyplot as plt 

#import itertools


#from collections import Counter


##############Read File
fname = 'Travel Vaccine'
df = pd.read_csv('C:/Users/Nabha Subramanya/Documents/Projects/MonkeyPox/FINAL/'+fname+'NLP.csv', sep = '|')
############
l=[]
linkes = df['url']
for i in range(len(linkes)):
    main=domain.extract(linkes[i])
    l.append(main.domain)


df['domain'] = df['url'].apply(lambda x: x.split("/")[2])
freq = pd.value_counts(df['domain'])

#COUNTRY
#df['country'] = df['country'].apply(lambda x: re.sub("United States","US",x))
#df['country'] = df['country'].apply(lambda x: re.sub("United Kingdom","Uk",x))

cntry_cnt = df['country'].str.split(',',expand = True).stack()
cntry_cnt = cntry_cnt.apply(lambda x: re.sub("[^a-zA-Z0-9]","",x) )
cntry_cnt = cntry_cnt.apply(lambda x: re.sub(" ","",x) )
cntry_cnt = pd.DataFrame(cntry_cnt.value_counts())

#KeyWORDS
kywrd_cnt = df['keywords'].str.split(',',expand = True).stack()
kywrd_cnt = kywrd_cnt.apply(lambda x: re.sub("[^a-zA-Z0-9]","",x) )
kywrd_cnt = kywrd_cnt.apply(lambda x: re.sub(" ","",x) )
kywrd_cnt = pd.DataFrame(kywrd_cnt.value_counts())

#Entities
entty_cnt = df['entities'].str.split(',',expand = True).stack()
entty_cnt = entty_cnt.apply(lambda x: re.sub("[^a-zA-Z0-9]","",x) )
entty_cnt = entty_cnt.apply(lambda x: re.sub(" ","",x) )
entty_cnt = pd.DataFrame(entty_cnt.value_counts())

#########WORDCLOUD
stop_words_lst = ['travel','vaccine','vaccination','google scholar','september',
                  'available online','human',"s'", "dr", "december","january","november","ministry"]
nv = ','.join(df['nounblob'])
nv = re.sub("'","",nv)
for w in stop_words_lst:
    pattern = r'\b'+w+r'\b'
    nv = re.sub(pattern, '', nv)
    

wordcloud = WordCloud(width = 1200, height = 800, 
                background_color ='white',
                min_font_size = 8).generate(nv) 


# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 

###########################TOP N BiGrams

from sklearn.feature_extraction.text import CountVectorizer
def get_top_n_bigram(corpus, n=None):
    vec = CountVectorizer(ngram_range=(2, 2), stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

common_words = get_top_n_bigram(df['content_full'].dropna(), 20)

for word, freq in common_words:
    print(word, freq)

df4 = pd.DataFrame(common_words, columns = ['content_full' , 'count'])


# The distribution of top part-of-speech tags of review corpus
blob = TextBlob(str(df['content_full']))
pos_df = pd.DataFrame(blob.tags, columns = ['word' , 'pos'])
pos_df = pos_df.pos.value_counts()

























