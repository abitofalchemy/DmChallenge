#!/usr/local/bin/python
from TwitterAPI import TwitterAPI
################################################################
##  main
###############################################################
if __name__ == "__main__":
# Go to http://twitter.com/apps/new to create an app and get these items
# See https://dev.twitter.com/docs/auth/oauth for more information on Twitter's OAuth implementation

	CONSUMER_KEY = 'YgK6PAOsHE4z3bbcwG375dtRI'
	CONSUMER_SECRET = 'KNWYsS7rhCdqTja13YH2gqdz7bA7eP8f5N9WmVsoeSaVJ9XwN3'
	OAUTH_TOKEN = '354043186-eoLXgG18vL4ZAdGkL75z2LxwaUcOfL9TGHU9Cuhv'
	OAUTH_TOKEN_SECRET = 'SWVaDYeXxH0hAFqlAR9u4jCpH0hjIOABZb9QFtcZRQEXB'

	api = TwitterAPI(CONSUMER_KEY, \
					 CONSUMER_SECRET, \
					 OAUTH_TOKEN, \
					 OAUTH_TOKEN_SECRET) 
	r = api.request('search/tweets',{'q': 'SBTribune'})
	for item in r:
		print (item['text'] if 'text' in item else item)

	print '\nQUOTA: %s', r.get_rest_quota() 
