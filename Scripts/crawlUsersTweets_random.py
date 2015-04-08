#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Sal Aguinaga 2015
## http://stackoverflow.com/questions/17245415/read-and-write-csv-files-including-unicode-with-python-2-7

import json, os, sys
import pandas as pd
import itertools
from twython import Twython
## time stamp for the ouputfile
import datetime
import time
import csv
import pandas as pd
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
def get_timelines(user_ids_filename):
	## Set output file
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
	outputFile = 'Data/followersTweets_SBTribune_'+st+'.txt'
	fout  = open(outputFile,'w')
	k = 0
	tweets_by_users_dict = dict()
	with open(user_ids_filename, 'rb') as inputFile:
		for userId in inputFile:
			print userId
			try:
				#user_timeline = (twitter.get_user_timeline(screen_name='ryanmcgrath', count=2))
				user_timeline = (twitter.get_user_timeline(user_id=userId, 
														   count=200, 
														   include_rts=1) )
				#tweets_by_users_dict[
			except TwythonAuthError as e:
				print e
		
			break;
			#if k == 5: break
			#k += 1	
			## store tweet dump
			
	print user_timeline[u'id_str']
	

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
