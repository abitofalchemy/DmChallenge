# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:01:29 2014

@author: aastha
"""
from newspaper import Article
import pickle, sys

sal = True
fpath="Data/wsbt_raw_tweets_1.csv.urls"
with open(fpath, 'rb') as f:
    urls = []
    if (sal):
        f.readline()
        for line in f:
            urls.append(line.split(",")[0])
    else:
        urls = pickle.load(f)

print urls [:5]
documents=[]
tweet_data=[]
for u in urls[:5]:
    print u
    try:
        a = Article(u, language='en')
        a.download()
        a.parse()
        tweet_data.append(a.text)
    except Exception:
        continue
documents.append(tweet_data)
print "************************"

fpath="sandBox/DocumentCorpus.txt"
with open(fpath, 'wb') as f:
    pickle.dump(documents, f)


#for u in urls[7]:
#    print u
#    try:
#        a = Article(u, language='en')
#        a.download()
#        a.parse()
#        tweet_data.append(a.text)
#        documents.append(tweet_data)
#    except Exception:
#        continue