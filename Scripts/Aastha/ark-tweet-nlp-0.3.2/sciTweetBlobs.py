#!/usr/local/bin/python

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
import json
import pandas as pd
import numpy as np
import itertools
from pprint import pprint
import re
from pattern.en import parse
import nltk
from yaml import load, dump

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def describe_tweets(input_json_file):
    ## count things
    data = []
    k = j = 0
    with open(input_json_file,'r') as jsonFile:
        for tweet in jsonFile:
            jObj = json.loads(tweet)
            print jObj('')
            
            ## filter tweets for those that are in English
            if jObj['lang']== 'en':
                ## pop'n the dictionary
                twt_stats ={
                    'usr_ment_cnt': len(jObj.get('entities',{}).get('user_mentions', {})),
                    'url_cnt'     : len(jObj.get('entities',{}).get('urls',{})),
                    'hstgs_cnt'   : len(jObj.get('entities',{}).get('hashtags',{})),
                    'rt_cnt'      : jObj.get('retweet_count'),
                    'fv_cnt'      : jObj.get('favorite_count')
                }
                pprint.pprint(twt_stats)
                data.append(twt_stats)
                k +=1
            else:
                j +=1
    #print np.size(data)
#    print k , 'tweets processed'
#    not_en = (j/(j+k)) * 100.0
#    print '%.2f percent of tweets are not English' % (not_en)
    return data

#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
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
    # gen stats on given tweets
    #print sys.argv[1]
    stats_list= (describe_tweets(sys.argv[1]))
    k = 0
    for dic in stats_list:
        print k, type(dic), dic
        k +=1

#    # gen stats on given tweets
#    stats_list= (describe_tweets('untrkdData/tweets.send.json'))
#    k = 0
#    for dic in stats_list:
#        print k, type(dic), dic
#        k +=1
#    
#    
#    sys.exit()
#
#    # filer tweets by english
#    cleaned_tweets = parse_sci_tweets('untrkdData/tweets.send.json')
#    
#    
#    # preprocess tweets
#    prproc_tweets = []
#    for tweet in cleaned_tweets:
#        prproc_tweets.append( processTweet(tweet['text']) )
#
#
#    # txt annotated with word types
#    txt_ann = []
#    for clnd_twts in cleaned_tweets:
#        #data = parse(clnd_twts['text'], relation=True, lematta=True)
#        #print data, type(data), np.size(data)
#        tokens = nltk.word_tokenize(clnd_twts['text'])
#        print nltk.pos_tag(tokens)
#        break
##print txt_ann[:4]


