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
def tweets_by(screen_names_file):
    ## Set output file
    outputFile = 'tweets_by_followes.txt'

    with open(screen_names_file, 'rb') as inputFile:
        for scrnName in inputFile:
            user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=10)
    #        print json.dumps(user_timeline, indent=2)
            if user_timeline is not None:
                for tweet in user_timeline:
                    print '%s, %s, %s, %s, %s, %s, %s' % (tweet['created_at'],tweet['user']['screen_name'],tweet['user']['id'], tweet['text'],tweet['entities']['hashtags'], tweet['retweet_count'],tweet['favorite_count'])
            break
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
    tweets_by('Data/wsbt_all_followers_screen_names.txt')

