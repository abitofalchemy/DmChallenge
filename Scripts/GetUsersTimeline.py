#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
## http://stackoverflow.com/questions/17245415/read-and-write-csv-files-including-unicode-with-python-2-7

import json, os, sys
import numpy as np 
import pandas as pd
import itertools
from twython import Twython
## time stamp for the ouputfile
import datetime
import time
import csv
import pprint
from twython import TwythonAuthError


APP_KEY	 = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
				  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



"""
# define user to get tweets for. accepts input from user
scrnName = raw_input("Please enter the twitter username: ")
user = twitter.show_user(screen_name=scrnName)
#print (json.dumps(user, indent=4))

# First, let's grab a user's timeline. Use the
# 'screen_name' parameter with a Twitter user name.
user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=2)
#user_timeline=twitter.get_user_timeline(screen_name="dksbhj", count=50)
for tweet in user_timeline:
	print tweet['text'] + "\n"

"""
"""
	Tweets by SBT followers 
"""
def handle_rate_limiting():
    app_status = {'remaining':1} # prepopulating this to make the first 'if' check fail
    while True:
        wait = 0
        if app_status['remaining'] &gt; 0:
            status = twitter.get_application_rate_limit_status(resources = ['statuses', 'application'])
            app_status = status['resources']['application']['/application/rate_limit_status']
            home_status = status['resources']['statuses']['/statuses/home_timeline']
            if home_status['remaining'] == 0:
                wait = max(home_status['reset'] - time.time(), 0) + 1 # addding 1 second pad
                time.sleep(wait)
            else:
                return
        else :
            wait = max(app_status['reset'] - time.time(), 0) + 10
            time.sleep(wait)
 
def get_timelines(user_ids_filename):
	latest = None   # most recent id scraped
	try:
	    last_tweet = tweets.find(limit=1, sort=[('id',-1)])[0] # sort: 1 = ascending, -1 = descending
	    if last_tweet:
	        latest = last_tweet['id']
	except:
	    print "Error retrieving tweets. Database probably needs to be populated before it can be queried."
 
	no_tweets_sleep = 1
	while True:
	    try:
	        newest = None # this is just a flag to let us know if we should update the "latest" value
	        params = {'count':200, 'contributor_details':True, 'since_id':latest}
	        handle_rate_limiting()
	        home = twitter.get_home_timeline(**params)
	        if home:
	            while home:
	                store_tweets(home)
	 
    	            # Only update "latest" if we're inside the first pass through the inner while loop
    	            if newest is None:
    	                newest = True
    	                latest = home[0]['id']
 
    	            params['max_id'] = home[-1]['id'] - 1
    	            handle_rate_limiting()
    	            home = twitter.get_home_timeline(**params)
    	    else:
    	        time.sleep(60*no_tweets_sleep)
 
    	except TwythonRateLimitError, e:
    	    reset = int(twitter.get_lastfunction_header('x-rate-limit-reset'))
    	    wait = max(reset - time.time(), 0) + 10 # addding 10 second pad
    	    time.sleep(wait)
    	except Exception, e:
    	    print e
    	    print "Non rate-limit exception encountered. Sleeping for 15 min before retrying"
    	    time.sleep(60*15)

	
	
	outFile = "Data/tweets_nytimes_followers.dat"
	titlesMasterDict = shelve.open(outFile, "n")
	titlesMasterDict.update(masterDict)
	titlesMasterDict.close()

	print "\n","-"*80
	
	return
def tweets_by(screen_names_file):
	## Set output file
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
	outputFile = 'Data/followersTweets_SBTribune_'+st+'.txt'
	fout  = open(outputFile,'w')
	inx = 0
	with open(screen_names_file, 'rb') as inputFile:
		for scrnName in inputFile:
			try:
				user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=2)
			except TwythonAuthError:
				continue
			if user_timeline is not None:
				#print json.dumps(user_timeline, indent=2)
				csv.writer(fout).writerow(user_timeline)
#				for tweet in user_timeline:
#					csv.writer(fout).writerow(json.dumps(tweet))
#					print inx,':',scrnName
			inx +=1

			if inx > 170: break

##					print '%s, %s, %s, %s, %s, %s, %s' % (tweet['created_at'],tweet['user']['screen_name'],tweet['user']['id'], tweet['text'],tweet['entities']['hashtags'], tweet['retweet_count'],tweet['favorite_count'])
#					csv.writer(fout).writerow([tweet['created_at'],tweet['user']['screen_name'], \
#											tweet['user']['id'], u"tweet['text']", \
#											tweet['entities']['hashtags'], \
#											tweet['retweet_count'],tweet['favorite_count']])

	fout.close()
	print inx
	return
"""
	Trends near south bend
"""
def trendind_near_south_bend():
	closest_trends = twitter.get_closest_trends(lat=41.677101,
												long= -86.269073)

	trnding_nearby = twitter.get_place_trends(id=closest_trends[0]['woeid'])
	print 'Trends near South Bend as of ',trnding_nearby[0]['created_at']
	for trend  in trnding_nearby[0]['trends']:
		print json.dumps((trend['name'],trend['url']), indent=2)
	return
################################################################
##  main
###############################################################
if __name__ == "__main__":
	#tweets_by('Data/wsbt_all_followers_screen_names.txt')
	default_path = "/home/northwind/Development/DmChallenge/"
	os.chdir(default_path)
	user_ids = "Data/nytimes_followers_ids.csv"
	get_timelines(user_ids)
	#tweets_by('Data/sbtribune_all_followers_screen_names.txt')
	print '-'*80
