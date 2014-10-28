#!/usr/local/bin/python

import twitter
#from twitter import oauth

import json

# Go to http://twitter.com/apps/new to create an app and get these items
# See https://dev.twitter.com/docs/auth/oauth for more information on Twitter's OAuth implementation

CONSUMER_KEY = 'YgK6PAOsHE4z3bbcwG375dtRI'
CONSUMER_SECRET = 'KNWYsS7rhCdqTja13YH2gqdz7bA7eP8f5N9WmVsoeSaVJ9XwN3'
OAUTH_TOKEN = '354043186-eoLXgG18vL4ZAdGkL75z2LxwaUcOfL9TGHU9Cuhv'
OAUTH_TOKEN_SECRET = 'SWVaDYeXxH0hAFqlAR9u4jCpH0hjIOABZb9QFtcZRQEXB'

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#print api.VerifyCredentials()

statuses = api.GetUserTimeline(screen_name='SBTribune')
#print [s.text for s in statuses]

#users = api.GetFriends()
#print [u.name for u in users]

#status = api.PostUpdate('I love python-twitter!')
#print status.text

#returns a twitter.User instance for each follower
users = api.GetFriends('SBTribune') 
#print 'twitter instance of each follower', [u.screen_name for u in users]
for u in users:
	print u.screen_name

