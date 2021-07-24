# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:10:34 2020

@author: Nabha Subramanya
"""
import pandas as pd
#from sklearn.feature_extraction.text import TfidfVectorizer
#import numpy as np
#import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import pycountry
from textblob import TextBlob
import en_core_web_sm
from nltk.stem.porter import PorterStemmer
import re
fname = 'travel clinic'
df = pd.read_csv('C:/Users/Nabha Subramanya/Documents/Projects/MonkeyPox/FINAL/'+fname+'_Parsed.csv')
df['content'] = df['content'].astype(str)

def remove_punct(text):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct

# Remove Name Entity Pairs
nlp = en_core_web_sm.load()

def remove_ents(text):
    lst = []
    doc = nlp(text)
    for ent in doc.ents: 
        lst.append(ent.text)
    words = " ".join([c for c in text.split() if c not in lst])
    return words

def get_ents(text):
    lst = []
    doc = nlp(text)
    for ent in doc.ents: 
        lst.append(ent.text)
    return lst

#
tokenizer = RegexpTokenizer(r'\w+')

def remove_stopw(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words

# Lemmatizer
lemm = WordNetLemmatizer()
def word_lemm(text):
    lem_text = [lemm.lemmatize(l) for l in text]
    return lem_text

# Stemmer
stemmer = PorterStemmer()
def word_stemm(text):
    stem_text = [stemmer.stem(s) for s in text]
    return stem_text


def find_country(text):
    lst = []
    for country in pycountry.countries:
        if country.name in text: lst.append(country.name)
    return lst


def noun_blob(text):
    blob = TextBlob(text)
    list_blob = blob.noun_phrases
    return list_blob
############################CONTENT
df['content_full'] = df['content']
df['content_full'] = df['content_full'].astype('str')
df['content'] = [re.sub("(,[ ]*!.*')$", "", x) for x in df['content']]
df['entities'] = df['content'].apply(lambda x: get_ents(x))
df['content'] = df['content'].apply(lambda x: remove_ents(x))
df['nounblob'] = df['content'].apply(lambda x: noun_blob(x))
df['content'] = df['content'].apply(lambda x: remove_punct(x))
df['content'] = df['content'].apply(lambda x: tokenizer.tokenize(x.lower()))
df['content'] = df['content'].apply(lambda x: remove_stopw(x))
df['content'] = df['content'].apply(lambda x: word_lemm(x))
df['content'] = df['content'].apply(lambda x: word_stemm(x))

print(df['content'][2])
len(df['content'][1])


############################TITLE
#df['Title_full'] = df['Title']
#df['Title'] = df['Title'].astype(str)
#df['Title'] = [re.sub("(,[ ]*!.*)$", "", x) for x in df['Title']]
#df['Title'] = df['Title'].apply(lambda x: remove_punct(x))
#df['Title'] = df['Title'].apply(lambda x: tokenizer.tokenize(x.lower()))
#df['Title'] = df['Title'].apply(lambda x: remove_stopw(x))
#df['Title'] = df['Title'].apply(lambda x: word_lemm(x))
##df['content'] = df['content'].apply(lambda x: word_stemm(x))
##print(df['Title'])

df['country'] = df['content_full'].apply(lambda x: find_country(x))
#df['nounblob'] = df['content_full'].apply(lambda x: noun_blob(x))


df.to_csv(fname+"NLP.csv", sep = '|')

