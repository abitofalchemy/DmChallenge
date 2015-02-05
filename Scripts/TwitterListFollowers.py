#!/usr/local/bin/python
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
import numpy as np
from pprint import pprint
import re
from twython import Twython
from twython import TwythonAuthError, TwythonError


APP_KEY = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



def find_listOfFollowers_forUser( scr_name ):
    user_details = twitter.show_user(screen_name= scr_name)
    followers_count = user_details['followers_count']
    friends___count = user_details['friends_count']


    fnum = 5000
    ## pnum = pages no.
    pnum = int(math.ceil(float(user_details["followers_count"]) / fnum))
    user_followers_lst = []
    followers = dict()
    followers['next_cursor'] = -1
    ## Get the next pages of user ids
    for i in range(pnum):
        if i > 1: time.sleep(60)
        followers = twitter.get_followers_ids(screen_name = scr_name,
                                     count = fnum,
                                     cursor= followers['next_cursor'])
        #
        for k in range(len(followers['ids'])): user_followers_lst.append(followers['ids'][k])


    # for follower_id in followers:
    print 'Number of ids found:', len(user_followers_lst)
    with  open("Data/"+scr_name+"_followers_ids.csv",'wb') as resultFile:
        wr = csv.writer(resultFile)
        for row in user_followers_lst: wr.writerow([row])
    print 'List written to disk.',u'\u25FC'

    return

if __name__ == '__main__':
    """
    TwitterListOfFollowers
    Description: Search Twitter for a given user's tweets,
    its followers, and its followers tweets
    """
    scr_name = (sys.argv[1])
    find_listOfFollowers_forUser(scr_name)
