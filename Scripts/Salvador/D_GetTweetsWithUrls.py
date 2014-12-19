#!/usr/local/bin/python
# -*- coding: utf-8; -*-
#
# (c) 2014 S. Aguinaga


# http://nbviewer.ipython.org/github/herrfz/dataanalysis/blob/master/week3/exploratory_graphs.ipynb
#
# http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html
#
# http://ravikiranj.net/drupal/201205/code/machine-learning/how-build-twitter-sentiment-analyzer
# https://pypi.python.org/pypi/textblob

#   CURRENTLY UNUSED CODE
################################################################################
#	pprint(dat_json)

#    for line_str in f:
#        jsonObj = json.loads(line_str)
#
#        for k,v in jsonObj.iteritems():
#            print k,v
#            break
##with open('tweets.json','r') as data_file:
##	#data = json.load(json.dumps([data_file]))
##	#data = json.load(json.dumps([json.JSONEncoder().encode(data_file)]))
##	#pprint(data)
##	data = json.load(data_file)
##	for k,v in data.iteritems():
##		    print k,v
##
##	sys.exit()
#        for k,v in ret.iteritems():
#print k,v

##


#
#                json_object = json.loads(line)
#                data.append(json_object)
#
### parse the twitter stream
#df = pd.DataFrame(columns=['timestamp','name','tweet', 'retweetCnt', 'hastags', 'urlsCnt','mentionsCnt'])
#
#ix = 0
#for jobj in data:
#    #print '----------------------------'
#        #mydata = {  'name': jobj['user']['screen_name'],
#        #        'text': jobj['text']}
#        #print mydata['name'], 'wrote', mydata['text'] # or something
#        #print json.dumps(jobj,indent=2)
##    rtstatus = jobj.get('retweeted_status',None)
##print ix
#    parsedTweet = (jobj.get('created_at',None),
#               jobj.get('user',{}).get('screen_name',None),
#               jobj.get('text',{}),
#               jobj.get('retweeted_status',{}).get('retweet_count',{}),
#               jobj.get('entities',{}).get('hashtags',{}),
#               len(jobj.get('entities',{}).get('urls',{})),
#               len(jobj.get('entities',{}).get('user_mentions',{})))
#
##    print '%s, %s, %s, %s, %s, %i, %i' % (jobj.get('created_at',None),
##                                      jobj.get('user',{}).get('screen_name',None),
##                                      jobj.get('text',{}),
##                                      jobj.get('retweeted_status',{}).get('retweet_count',{}),
##                                          jobj.get('entities',{}).get('hashtags',{}),
##                                          len(jobj.get('entities',{}).get('urls',{})),
##                                      len(jobj.get('entities',{}).get('user_mentions',{})))
#    df.loc[ix] = parsedTweet
#    ix +=1
#print df.shape
#
### time stamp for the ouputfile
#import datetime
#import time
#
#ts = time.time()
#st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
#
#df.to_csv('Data/parsed_wsbt_twitter_stream_%s.txt' % st, sep=',',mode='w',encoding='utf-8',index=False)
################################################################################
################################################################################
from __future__ import division
import sys,argparse
import json, ast, pickle
import pandas as pd
import numpy as np
import itertools
from pprint import pprint
import re
from newspaper import Article
from pattern.en import parse
import nltk
from yaml import load, dump
from pprint import pprint
from twython import Twython
from twython import TwythonAuthError, TwythonError
import math
import time
from string import punctuation

def clean_tweets(input_json_file):
    out_file = input_json_file.rstrip(".csv")+".cln.csv"
    
    print 'Processing file: ',input_json_file
    ## count things
    data = []
    k = j = 0
    with open(input_json_file,'rb') as jsonFile:
        jsonList = json.load(jsonFile)
            #data.append(["id","created_at","text","retweet_count","ent_urls","ent_hashtags", \
            #"ent_mentions","favorite_count","in_reply_to_status_id"])
        for jObj in jsonList:
            #pprint (jObj[0]['entities'])
            ## filter tweets for those that are in English
            if jObj[0]['lang']== 'en':
                # we want id,created_at,text,retweet_count,ent_urls,ent_hashtags,ent_mentions,favorite_count,in_reply_to_status_id
                tweet_vec = [jObj[0]['id'], jObj[0]['created_at'], jObj[0]['text'], jObj[0]['retweet_count'], \
                             jObj[0]['entities']['urls'], jObj[0]['entities']['hashtags'],\
                             jObj[0]['entities']['user_mentions'], \
                             jObj[0]['favorite_count'], jObj[0]['in_reply_to_status_id']]
                data.append(tweet_vec)
                k +=1
            else:
                j +=1

#    print "np.size(data)",np.size(data)
#    print k , 'tweets processed'
#    not_en = (j/(j+k)) * 100.0
#    print '%.2f percent of tweets are not English' % (not_en)
    df = pd.DataFrame(data,columns=["id","created_at","text","retweet_count","ent_urls",
                                    "ent_hashtags", "ent_mentions","favorite_count","in_reply_to_status_id"])
    df.to_csv(out_file, sep=',',mode="w", index=False,encoding='utf-8')
    print 'Wrote cleaned (csv) tweets to:',out_file
    return


def tweets_stats(input_json_file):

    print 'Processing file: ',input_json_file
    
    ## count things
    data = []
    k = j = 0
    with open(input_json_file,'rb') as jsonFile:
        jsonList = json.load(jsonFile)
        for jObj in jsonList:
            #pprint (jObj[0]['lang'])
            ## filter tweets for those that are in English
            if jObj[0]['lang']== 'en':
                ## pop'n the dictionary
                twt_stats ={
                    'usr_ment_cnt': len(jObj[0].get('entities',{}).get('user_mentions', {})),
                    'url_cnt'     : len(jObj[0].get('entities',{}).get('urls',{})),
                    'hstgs_cnt'   : len(jObj[0].get('entities',{}).get('hashtags',{})),
                    'rt_cnt'      : jObj[0].get('retweet_count'),
                    'fv_cnt'      : jObj[0].get('favorite_count')
                }
                #pprint.pprint(tw_stats)
                data.append(twt_stats)
                k +=1
            else:
                j +=1

    print "np.size(data)",np.size(data)
    print k , 'tweets processed'
    not_en = (j/(j+k)) * 100.0
    print '%.2f percent of tweets are not English' % (not_en)
    return data

def getTweetsWithUrls(tweet):
    tst_tweet = re.search('((www\.[\s]+)|(http://\S+\s))',tweet)
    if tst_tweet is not None:
        #print tst_tweet.group(3)
        return tst_tweet.group(3)
    else:
        return None

#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    #Remove puctuation
    for p in list(punctuation):
        tweet=tweet.replace(p,'')
    
    return tweet
#end

def filter_tweets(tweets_json_list):
    out_data = dict()
    for tweet in tweets_json_list:
        out_data[tweet['id']] = [tweet['text'].encode('utf-8'),tweet['created_at'].encode('utf-8'),
                                 tweet['user']['screen_name'].encode('utf-8'),tweet['user']['id'],
                                 tweet['entities']['hashtags'], tweet['retweet_count'],tweet['favorite_count'],
                                 tweet['entities']['urls']]
    
            
    return out_data
def parse_sci_tweets(input_json_file):
    data = []
    k = 0
    with open(input_json_file,'r') as jsonFile:
        for tweet in jsonFile:
            jObj = json.loads(tweet)
            ## filter tweets for those that are in English
            if jObj.get('lang', None) == 'en':
                data.append(jObj)
                k +=1
	print k , 'English tweets processed'
    return data

def enhance_using_url(sUrl):
    a = Article(sUrl, language='en')
    a.download()
    a.parse()
    url_augmented_tweet = ""
    #print "Ehriched tweet:\n"+(min_tweet_dict[rawTweet][1]+","+a.text)
    try:
        url_augmented_tweet= "%s, %s"%(min_tweet_dict[rawTweet][0].decode("utf-8"), a.title.decode("utf-8"))
    except:
        print cnt
        print min_tweet_dict[rawTweet][1],a.title
        url_augmented_tweet = min_tweet_dict[rawTweet][0].decode("utf-8")

#pprint (url_augmented_tweet)

    return url_augmented_tweet


def show_header(cmd_line_args):
    print cmd_line_args
    print '-'*80
    return

if __name__ == '__main__':
    ## header
    show_header(sys.argv)
    
    ## handle arguments
    parser = argparse.ArgumentParser(description='Read Crawled Tweets')
    parser.add_argument('input_file',help='input json file',action='store')
    args = parser.parse_args()

    print args.input_file

    ## Get enginlish tweets parsed
    tweets_dict = parse_sci_tweets(args.input_file)
    
    ## Filter tweets (trim the tweet)
    filt_t_dict = filter_tweets(tweets_dict)

    ## initialize variables
    min_tweet_dict = dict()
    enhanced_cleaned_tw_lst = []
    boolTweetsWithUrls = False

    if boolTweetsWithUrls:
        ## Get tweets with urls
        for tweet in filt_t_dict:
            tstStr = getTweetsWithUrls(filt_t_dict[tweet][0])
            if (tstStr) is not None:
                min_tweet_dict[tweet] =  [tstStr,filt_t_dict[tweet][0]] #(getTweetsWithUrls(filt_t_dict[tweet][0])
        print "tweets filtered: %d" % len(min_tweet_dict)
    else:
        min_tweet_dict = filt_t_dict
    print "tweets to start with : %d" % len(min_tweet_dict)



    ## Further Cleaning/Enhancing the orig tweets
    cnt = 0

    print "Further Cleaning/Enhancing the orig tweets"
    for rawTweet in min_tweet_dict:
        extra_text = ""
        #print min_tweet_dict[rawTweet][0]
        if min_tweet_dict[rawTweet][len(min_tweet_dict[rawTweet])-1]:
            # url has urls
            for urlDict in min_tweet_dict[rawTweet][len(min_tweet_dict[rawTweet])-1]:
                #print urlDict['expanded_url']
                extra_text = extra_text + enhance_using_url(urlDict['expanded_url'])
            #print extra_text
            enhanced_cleaned_tw_lst.append("%s, %s" % (min_tweet_dict[rawTweet][0].decode("utf-8"), extra_text))
        else:
            #print "does not have urls\n", min_tweet_dict[rawTweet][0]
            enhanced_cleaned_tw_lst.append(processTweet(min_tweet_dict[rawTweet][0]))


    print "Generated %d enhanced/cleaned tweets" % len(enhanced_cleaned_tw_lst)
    print enhanced_cleaned_tw_lst[:3]

##  At this point, we can further clean the tweets from their puctuations, but I might
##  want to handle hashtags in a special way

    document = []
    for sentence in enhanced_cleaned_tw_lst:
        document.append( nltk.word_tokenize(sentence))
    fdist1 = nltk.FreqDist(document)
    #print document
    pprint( fdist1.most_common(20))

#        tagged = nltk.pos_tag(tokens)
#        ## identify the named entities:
#        entities = nltk.chunk.ne_chunk (tagged)
#        print entities
#        break

