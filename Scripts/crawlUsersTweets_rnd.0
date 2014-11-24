##---------------------------------------------------------------------
##  References:
##  -----------
##  http://stackoverflow.com/questions/17245415/read-and-write-csv-files-including-unicode-with-python-2-7
##  https://developers.google.com/edu/python/introduction
##
##---------------------------------------------------------------------

import sys
import random
import json
## time stamp for the ouputfile
import datetime
import time
#import itertools
import csv
#import pandas as pd
import pprint

from twython import Twython
from twython import TwythonAuthError, TwythonError


APP_KEY     = CONSUMER_KEY    = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def tweets_for_random_list(rand_followers_list):
    ## Set output file
    ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y_%H%M%S')
    st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
    out_file = 'Data/tweets_from_followers_wsbt_sbt_'+st+'.txt'
    
    inx = 0
    with open(out_file,'w') as f:
        wrt = csv.writer(f)
        
        for scrnName in rand_followers_list:
            try:
                user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=2)
            except TwythonAuthError:
                continue
            except TwythonError:
                continue
            if user_timeline is not None:
                for tweet in user_timeline:
                    #print tweet
                    wrt.writerow([tweet])
            #()
            #json_output = ast.literal_eval(json.dumps(user_timeline)) #[s.encode('utf-8') for s in user_timeline]
            #pprint.pprint (json_output)
            #
            #                csv.writer(file).writerow([tweet])
            #                inx +=1
            break ##if inx > 4: break
    
    #    print inx
    f.close()
    return
#def tweets_for_random_list(rand_followers_list):
#    ## Set output file
#    ts = time.time()
#    #st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y_%H%M%S')
#    st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
#    outputFile = 'Data/tweets_from_followers_wsbt_sbt_'+st+'.txt'
#    file = open(outputFile, 'w')
#    inx = 0
#    
#    for scrnName in rand_followers_list:
#        try:
#            user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=2)
#        except TwythonAuthError:
#            continue
#        except TwythonError:
#            continue
#        if user_timeline is not None:
#            json.dump(user_timeline, file)
#            file.write('\n')
#            #json_output = ast.literal_eval(json.dumps(user_timeline)) #[s.encode('utf-8') for s in user_timeline]
#            #pprint.pprint (json_output)
#        #            for tweet in user_timeline:
#        #                csv.writer(file).writerow([tweet])
#        #                inx +=1
#        break ##if inx > 4: break
#    
#    #    print inx
#    file.close()
#    return


##---------------------------------------------------------------------
##  main() function calls
##---------------------------------------------------------------------
def main():
    ## define arrays
    mylist = []
    tweets = []


    ## Get list of followers for both WSBT & SBT
    followers_wsbt_infile = 'Data/sbtribune_all_followers_screen_names.txt'
    followers_sbt_infile  = 'Data/wsbt_all_followers_screen_names.txt'
    
    with open(followers_wsbt_infile) as f:
        l1 = f.read().splitlines()
    with open(followers_sbt_infile) as f:
        l2 = f.read().splitlines()
    
    ## merge lists
    mrgList = list(set(l1 + l2))

    ## Random sampling select N random followers
    rand_smpl = [ mrgList[i] for i in sorted(random.sample(xrange(len(mrgList)), 128)) ]

    ## Get tweets from followers
    tweets = tweets_for_random_list(rand_smpl)

    print tweets
    print type(tweets)


if __name__ == '__main__':
    main()



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
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
    outputFile = 'Data/followersTweets_SBTribune_'+st+'.txt'
    fout  = open(outputFile,'w')
    inx = 0
    with open(screen_names_file, 'rb') as inputFile:
        
        for scrnName in inputFile:
            #print '>', scrnName
            try:
                user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=2)
            except TwythonAuthError:
                continue
            if user_timeline is not None:
                #print json.dumps(user_timeline, indent=2)
                csv.writer(fout).writerow(user_timeline)
#                for tweet in user_timeline:
#                    csv.writer(fout).writerow(json.dumps(tweet))
#                    print inx,':',scrnName
            inx +=1

            if inx > 170: break

##                    print '%s, %s, %s, %s, %s, %s, %s' % (tweet['created_at'],tweet['user']['screen_name'],tweet['user']['id'], tweet['text'],tweet['entities']['hashtags'], tweet['retweet_count'],tweet['favorite_count'])
#                    csv.writer(fout).writerow([tweet['created_at'],tweet['user']['screen_name'], \
#                                            tweet['user']['id'], u"tweet['text']", \
#                                            tweet['entities']['hashtags'], \
#                                            tweet['retweet_count'],tweet['favorite_count']])

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

###########
#csv.writer(f).writerow(tweet)

#json.dump(user_timeline,f)
#csv.writer(f).writerow(json.dump(tweet))
#sthash.DgniJDHX.dpuf
#print json.dumps(user_timeline, indent=2)
#csv.writer(fout).writerow(user_timeline)
#                for tweet in user_timeline:
#                    csv.writer(fout).writerow(json.dumps(tweet))
#                    print inx,':',scrnName
