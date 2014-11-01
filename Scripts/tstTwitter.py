#!/usr/local/bin/python

import twitter
#from twitter import oauth

import json

# Go to http://twitter.com/apps/new to create an app and get these items
# See https://dev.twitter.com/docs/auth/oauth for more information on Twitter's OAuth implementation

CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#print api.VerifyCredentials()
print ' \
----------------------------------------------------------\n \
tstTwitter.py\n \
----------------------------------------------------------'
statuses = api.GetUserTimeline(screen_name='abitofalchemy')
for s in statuses:
	print s.text


#users = api.GetFriends()
#print [u.name for u in users]

#status = api.PostUpdate('I love python-twitter!')
#print status.text

#returns a twitter.User instance for each follower
users = api.GetFriends(screen_name='abitofalchemy') 
#print 'twitter instance of each follower', [u.screen_name for u in users]
for u in users:
	print u.screen_name

