#!/usr/local/bin/python
# -*- coding: utf-8; -*-
#
# (c) 2014 S. Aguinaga


# http://nbviewer.ipython.org/github/herrfz/dataanalysis/blob/master/week3/exploratory_graphs.ipynb
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
# http://ravikiranj.net/drupal/201205/code/machine-learning/how-build-twitter-sentiment-analyzer
# https://pypi.python.org/pypi/textblob
# http://nbviewer.ipython.org/github/herrfz/dataanalysis/blob/master/week3/exploratory_graphs.ipynb

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
import sys
import json, ast, pickle
import pandas as pd
import numpy as np
import itertools
from pprint import pprint
import re
from pattern.en import parse
import nltk
from yaml import load, dump
from pprint import pprint
from twython import Twython
from twython import TwythonAuthError, TwythonError
import math
import time

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
    return tweet
#end


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
	print k , 'tweets processed'
    return data


def show_header(cmd_line_args):
    print cmd_line_args
    print '-'*80
    return

if __name__ == '__main__':
	# header
	show_header(sys.argv)
    #tweets_stats(sys.argv[1])
        
    # clean tweets
	clean_tweets(sys.argv[1])





