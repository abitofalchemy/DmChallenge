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

APP_KEY     = CONSUMER_KEY    = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

################################################################################

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def getFollowers(user_screen_name):
    suser = twitter.show_user(screen_name=user_screen_name)
    fnum = 200
    pnum = int(math.ceil(float(suser["followers_count"]) / fnum))

    user_followers  =[]
    pages = []
    for i in range(pnum):
        pages.append("p"+str(i+1))

    oldpages = []
    for i in range(pnum):
        oldpages.append("p"+str(i))

    p0 = { "next_cursor": -1 } # So the following exec() call doesn't fail.

    for i in range(pnum):
        exec(pages[i]+" = twitter.get_followers_list(screen_name=user_screen_name, count=fnum, skip_status=1, cursor="+oldpages[i]+"['next_cursor'])")

    followers = []

    for p in range(pnum):
        try:
            exec("for i in range(fnum): followers.append("+pages[p]+"['users'][i])")
        except(IndexError):
            pass

    print(len(followers))


    for x in followers:
#        print("""Name:  %s
#            Username:  %s
#            """ % (x["name"], x["screen_name"]))
        user_followers.append([user_screen_name,x["name"], x["screen_name"],x["location"]])

    ## convert to data frame
    user_followers_df = pd.DataFrame(user_followers,
                                     columns = ["prolific_user","f_name","f_screen_name", "f_location"])
    user_followers_df.to_csv("Data/prolific_tweeters.followers.csv", sep=',',mode="a", header=False,
                                 encoding='utf-8',index=False)
    return


def describe_users(input_json_file):
    """
        this code is used to get the list of most prolific users for wsbt/sbt
    """
    data = []
    k = j = 0
    ##
    proc_prol_users_lst = []
    
    with open ("Data/prolific_tweeters.followers.csv","r") as f_file:
        last = ""
        f_file.readline()
        for line in f_file:
            new = line.split(",")[0]
            if (new == last):
                continue
            else:
                last = new
                proc_prol_users_lst.append(new)

    with open(input_json_file,'r') as jsonFile:
        for tweet in jsonFile:
            jObj = json.loads(tweet)
			#pprint(jObj)
            if (jObj.get('user',None) is not None):
                if (jObj['user']['screen_name'] in proc_prol_users_lst):
                    continue
                else:
                    ## Get these user's followers and friends
                    getFollowers(jObj['user']['screen_name'])
                    time.sleep(60)
                    data.append([jObj['user']['screen_name'],
                                 jObj['user']['id_str'], 
                                 jObj['user']['friends_count'], 
                                 jObj['user']['followers_count'],
                                 jObj['user']['location']])
    
    
    ## convert to data frame
    df = pd.DataFrame(data, columns = ["user_screen_name","user_id","friends_count",
                                       "followers_count", "userLocation"])
    print df.head()
    df.to_csv("Data/prolific_tweeters.csv", sep=',',mode='w',encoding='utf-8',index=False)
    
	
    return

def quick_stats(in_csv_file):
    my_data = json.loads(open(in_csv_file).read())
    print "len(my_data)",len(my_data)
#    twt_data = []
#    urls_sum = 0
#    for jObj in my_data:
#        urls_sum += len(jObj[0]['entities']['urls'])
#        for jUrl in jObj[0]['entities']['urls']:
    return

def describe_timelines(in_csv_file):
    my_data = json.loads(open(in_csv_file).read())
    twt_data = []
    urls_sum = 0
    for jObj in my_data:
        urls_sum += len(jObj[0]['entities']['urls'])
        for jUrl in jObj[0]['entities']['urls']:
            twt_data.append([jUrl['url'], jUrl['expanded_url']])
        
#        twt_data.append(jObj[0]['entities']['urls'])
#        twt_stats ={
#            'usr_ment_cnt': len(jObj[0].get('entities',{}).get('user_mentions', {})),
#            'url_cnt'     : len(jObj[0].get('entities',{}).get('urls',{})),
#            'hstgs_cnt'   : len(jObj[0].get('entities',{}).get('hashtags',{})),
#            'rt_cnt'      : jObj[0].get('retweet_count'),
#            'fv_cnt'      : jObj[0].get('favorite_count')
#        }

    df = pd.DataFrame(twt_data,columns=['url','extended_url'])
    print df.head()
    df.to_csv(in_csv_file+".urls",sep=',',mode='w',encoding='utf-8',index=False)

    ## describe
    print '\n# of urls: ',urls_sum
    print 'Percent of tweets with urls: %.2f' % (urls_sum/len(my_data) * 100)

    return

def describe_tweets(input_json_file):
    ## count things
    data = []
    k = j = 0
    with open(input_json_file,'r') as jsonFile:
        for tweet in jsonFile:
            jObj = json.loads(tweet)
            
            ## filter tweets for those that are in English
            if jObj[0]['lang']== 'en':
                ## pop'n the dictionary
                twt_stats ={
                    'usr_ment_cnt': len(jObj.get('entities',{}).get('user_mentions', {})),
                    'url_cnt'     : len(jObj.get('entities',{}).get('urls',{})),
                    'hstgs_cnt'   : len(jObj.get('entities',{}).get('hashtags',{})),
                    'rt_cnt'      : jObj.get('retweet_count'),
                    'fv_cnt'      : jObj.get('favorite_count')
                }
                pprint.pprint(tw_stats)
                data.append(twt_stats)
                k +=1
            else:
                j +=1
    #print np.size(data)
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
    
	# list most prolific tweeters
    #describe_users('Data_Schurz/tweets.json')

    # list stats on the wsbt/sbtribune
    #describe_timelines("Data/sbtribune_raw_tweets_1.csv")
	quick_stats("Data/sbtribune_raw_tweets_1.csv")
	quick_stats("Data/wsbt_raw_tweets_1.csv")



