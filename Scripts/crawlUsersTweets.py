import json
import pandas as pd
import itertools
from twython import Twython
import time
import csv
import pandas as pd
import pprint

APP_KEY     = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
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
## Set output file
outputFile = sbt_fllwrs_tweets
with open('Data/wsbt_followers.txt') as inputFile:
    user_timeline = twitter.get_user_timeline(screen_name=scrnName,
                                              count=2)
    for tweet in user_timeline:
        print tweet['text'] + "\n"
""" 
    Trends near south bend
"""
closest_trends = twitter.get_closest_trends(lat=41.677101,
                                            long= -86.269073)

trnding_nearby = twitter.get_place_trends(id=closest_trends[0]['woeid'])
print 'Trends near South Bend as of ',trnding_nearby[0]['created_at']
for trend  in trnding_nearby[0]['trends']:
    print json.dumps((trend['name'],trend['url']), indent=2)

