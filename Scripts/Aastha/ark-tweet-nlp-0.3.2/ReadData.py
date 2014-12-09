# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 01:04:51 2014

@author: aastha
"""

import pandas as pd
import re

MODULE = '/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/pattern-2.6'
import sys; 
if MODULE not in sys.path: sys.path.append(MODULE)
from sciTweetBlobs import processTweet

inputpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/DmChallenge-master/Data/tweets_from_followers_wsbt_sbt_27Nov14_060910.txt"

data=pd.read_csv(inputpath)
ids=[]
clean_tweets=[]

for index, row in data.iterrows():
    #print row['id'],row['text']
    t=processTweet(row['text'])
    t = t.replace(",", "")
    t = t.replace("'", "")
    t=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",t).split())
    if(t!=''):
        clean_tweets.append(t)
        ids.append(row['id'])
          
#sys.path.append('/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Codes/ark-tweet-nlp-0.3.2')
from CMUTweetTagger import runtagger_parse
print runtagger_parse(['example tweet 1', 'example tweet 2'])

#RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Codes/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"
pos_tweet = runtagger_parse(clean_tweets)

query_list=[]
for i in range(len(pos_tweet)):
    query_words=[]
    for tag in pos_tweet[i]:
        if(tag[1]=='N'):
            query_words.append(tag[0])
    query_list.append(query_words)

from google import search
import time 

retreived_urls=[]
for i in range(len(query_list)):
    print i
    print "\n"
    myurl=[]
    if(len(query_list[i])==0):
        print "no nouns"
        query=clean_tweets[i]
    else:
        query=' '.join(query_list[i])
    for url in search(query, stop=20):
        print(url)
        myurl.append(url)
    retreived_urls.append(myurl)
    if(i%5==0):
        time.sleep(60)
    if(i%50==0):
        time.sleep(60*15)
    print "*************************\n"
    
import pickle
fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/URL_list_full.txt"
with open(fpath, 'wb') as f:
    pickle.dump(retreived_urls, f)

fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/tweetids.txt"
with open(fpath, 'wb') as f:
    pickle.dump(ids, f)

fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/cleantweets.txt"
with open(fpath, 'wb') as f:
    pickle.dump(clean_tweets, f)

fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/querywords.txt"
with open(fpath, 'wb') as f:
    pickle.dump(query_list, f)
    
with open(fpath, 'rb') as f:
    my_list = pickle.load(f)