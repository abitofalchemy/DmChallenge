# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:01:29 2014

@author: aastha
"""
from newspaper import Article

import pickle
fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/URL_list_full.txt"
with open(fpath, 'rb') as f:
    urls = pickle.load(f)
    
documents=[]
for i in range(len(urls)):
    print i
    tweet_data=[]    
    for u in urls[i]:
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

fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/DocumentCorpus.txt"
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