#!/usr/bin/python 
# /afs/crc.nd.edu/x86_64_linux/python/2.7.8/bin/python
# ---------------------------------------------------------------------
##  References:
##  -----------
##  http://stackoverflow.com/questions/17245415/read-and-write-csv-files-including-unicode-with-python-2-7
##  https://developers.google.com/edu/python/introduction
##  https://inkplant.com/code/pull-twitter-feed-into-your-site/
##---------------------------------------------------------------------

import sys
import random
import json
import datetime  # time stamping
import time, math
import csv
import pandas as pd
from pprint import pprint
import re
from twython import Twython
from twython import TwythonAuthError, TwythonError
import argparse
import shelve


APP_KEY = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)




    
if __name__ == '__main__':
    """
    SearchTwitter
    Description: Search Twitter for a given user's tweets,
    its followers, and its followers tweets
    if len(sys.argv) == 3:
        parser = argparse.ArgumentParser(description='Get the tweets for a given organization')
        parser.add_argument('twitter_account', help='screen_name for a given organization')
        parser.add_argument('topicx', help='any word that is either a hash or mention')
        args = parser.parse_args()
        # main( args )
    else:
        parser = argparse.ArgumentParser(description='Get the tweets for a given organization')
        parser.add_argument('twitter_account', help='screen_name for a given organization') 
        args = parser.parse_args()
        SearchTwitter4User( args.twitter_account )

https://twitter.com/WSBT/status/526882173412859904
583312741684908033,
526882173412859904
    """
    try:
        user_timeline = twitter.get_user_timeline(screen_name="WSBT", count=200, max_id=583288998484963328)
    except TwythonAuthError:
        #continue
        print "TwythonAuthError", TwythonAuthError
    if user_timeline is not None:
        #print json.dumps(user_timeline, indent=2)
        parsed_dict = []
        for tweet in user_timeline:
            parsed_dict.append([tweet['id'], tweet['created_at'], tweet['text'].encode('utf-8'), tweet['retweet_count'],
            tweet['entities']['urls'], tweet['entities']['hashtags'],
            tweet['entities']['user_mentions'], tweet['favorite_count'],
            tweet['in_reply_to_status_id']]
        )
    #:
    print parsed_dict


# tweets                          =   []
# MAX_ATTEMPTS                    =   10
# COUNT_OF_TWEETS_TO_BE_FETCHED   =   20 

# for i in range(0,MAX_ATTEMPTS):

#     if(COUNT_OF_TWEETS_TO_BE_FETCHED < len(tweets)):
#         break # we got 500 tweets... !!

#     #----------------------------------------------------------------#
#     # STEP 1: Query Twitter
#     # STEP 2: Save the returned tweets
#     # STEP 3: Get the next max_id
#     #----------------------------------------------------------------#

#     # STEP 1: Query Twitter
#     if(0 == i):
#         # Query twitter for data. 
#         results    = twitter.search(q="WSBT",since='2014-10-27',until='2014-10-29',count='10')
#     else:
#         # After the first call we should have max_id from result of previous call. Pass it in query.
#         results    = twitter.search(q="WSBT",since='2014-10-27',until='2014-10-29', include_entities='true',max_id=next_max_id)
#         #search =t.search(q='AAPL', count="1000",since='2013-12-10')
#         #tweets= search['statuses']

#     # STEP 2: Save the returned tweets
#     for tweet in results['statuses']:
#         tweet_text = [tweet['id'], tweet['created_at'], tweet['text'].encode('utf-8'), tweet['retweet_count'],
#                                 tweet['entities']['urls'], tweet['entities']['hashtags'],
#                                 tweet['entities']['user_mentions'], tweet['favorite_count'],
#                                 tweet['in_reply_to_status_id']]
#         tweets.append(tweet_text)


#     # STEP 3: Get the next max_id
#     try:
#         # Parse the data returned to get max_id to be passed in consequent call.
#         next_results_url_params    = results['search_metadata']['next_results']
#         next_max_id        = next_results_url_params.split('max_id=')[1].split('&')[0]
#     except:
#         # No more next pages
#         break


#     df = pd.DataFrame(tweets)
#     df.columns = ['id', 'created_at','text','retweet_count','urls',
#                                              'hashtags', 'user_mentions', 'favorite_count',
#                                              'in_reply_to_status_id']
#     df.to_csv("wsbt_dataframe.csv","w")