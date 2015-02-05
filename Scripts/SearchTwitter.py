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


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def parse_to_csv(in_tweet_json):
    ## count things
    data = []
    k = j = 0
    for tweet in in_tweet_json:
        ## filter tweets for those that are in English
        if jObj.get('lang', None) == 'en':
            ## pop'n the dictionary
            twt_stats = {
                'usr_ment_cnt': len(jObj.get('entities', {}).get('user_mentions', {})),
                'url_cnt': len(jObj.get('entities', {}).get('urls', {})),
                'hstgs_cnt': len(jObj.get('entities', {}).get('hashtags', {})),
                'rt_cnt': jObj.get('retweet_count'),
                'fv_cnt': jObj.get('favorite_count')
            }
            print (twt_stats)
            k += 1
        else:
            j += 1
    return data


def tweets_for_random_list(rand_followers_list):
    print 'tweets_for_random_list'
    ## Set output file
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y_%H%M%S')
    # for dev: st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
    out_file = 'Data/tweets_from_followers_wsbt_sbt_' + st + '.txt'

    inx = 0
    data = []
    with open(out_file, 'w') as f:
        wrt = csv.writer(f)
        wrt.writerow(
            ["id", "created_at", "text", "retweet_count", "ent_urls", "ent_hashtags", "ent_mentions", "favorite_count",
             "in_reply_to_status_id"])
        for scrnName in rand_followers_list:
            try:
                user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=10)
            except TwythonAuthError:
                continue
            except TwythonError:
                continue
            if user_timeline is not None:
                for tweet in user_timeline:
                    parsed_tweet_arr = [tweet['id'], tweet['created_at'], tweet['text'].encode('utf-8'),
                                        tweet['retweet_count'], tweet['entities']['urls'],
                                        tweet['entities']['hashtags'], tweet['entities']['user_mentions'],
                                        tweet['favorite_count'], tweet['in_reply_to_status_id']];
                    wrt.writerow(parsed_tweet_arr)  # raw data

    return


# def tweets_for_random_list(rand_followers_list):
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
    print 'tweets_by'

    ## Set output file
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
    outputFile = 'Data/followersTweets_SBTribune_' + st + '.txt'
    fout = open(outputFile, 'w')
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
            inx += 1

        #if inx > 170: break

        ##                    print '%s, %s, %s, %s, %s, %s, %s' % (tweet['created_at'],tweet['user']['screen_name'],tweet['user']['id'], tweet['text'],tweet['entities']['hashtags'], tweet['retweet_count'],tweet['favorite_count'])
        #                    csv.writer(fout).writerow([tweet['created_at'],tweet['user']['screen_name'], \
        #                                            tweet['user']['id'], u"tweet['text']", \
        #                                            tweet['entities']['hashtags'], \
        #                                            tweet['retweet_count'],tweet['favorite_count']])

        #fout.close()
    print inx
    return


"""
    Trends near south bend
"""


def trendind_near_south_bend():
    closest_trends = twitter.get_closest_trends(lat=41.677101,
                                                long=-86.269073)

    trnding_nearby = twitter.get_place_trends(id=closest_trends[0]['woeid'])
    print 'Trends near South Bend as of ', trnding_nearby[0]['created_at']
    for trend in trnding_nearby[0]['trends']:
        print json.dumps((trend['name'], trend['url']), indent=2)
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
#from twython import TwythonError, TwythonAuthError, TwythonRateLimitError

def getTweetUser(sys_argv):
    data = []

    with open(sys_argv, 'r') as f:
        with open(sys_argv + '.userids', 'a') as fout:
            wrt = csv.writer(fout)
            f.readline()
            for line in f:
                token = line.split(",")[0]
                try:
                    tmpStr = twitter.show_status(id=token, trim_user=True, include_entities=True)
                except TwythonAuthError:

                    continue
                except TwythonError:
                    continue

                    #pprint (tmpStr)
                if (tmpStr.get("id", None)):
                    #data.append([tmpStr['id'], tmpStr['user']['id'],tmpStr['text']])
                    wrt.writerow([tmpStr['id'], tmpStr['user']['id'], tmpStr['text'].encode('utf-8')])

    return


#
def TwitterFollowersForUser(scrnName):
    suser = twitter.show_user(screen_name=scrnName)
    fnum = 10
    pnum = int(math.ceil(float(suser["followers_count"]) / fnum))

    user_followers = []
    pages = []
    for i in range(pnum):
        pages.append("p" + str(i + 1))

    oldpages = []
    for i in range(pnum):
        oldpages.append("p" + str(i))

    p0 = {"next_cursor": -1}  # So the following exec() call doesn't fail.

    for i in range(pnum):
        if i > 1: time.sleep(60)

        exec (
            pages[i] + " = twitter.get_followers_list(screen_name=scrnName, count=fnum, skip_status=1, cursor=" +
            oldpages[
                i] + "['next_cursor'])")

    followers = []

    for p in range(pnum):
        try:
            exec ("for i in range(fnum): followers.append(" + pages[p] + "['users'][i])")
        except(IndexError):
            pass

    print(len(followers))

    for x in followers:
        #        print("""Name:  %s
        #            Username:  %s
        #            """ % (x["name"], x["screen_name"]))
        user_followers.append([user_screen_name, x["name"], x["screen_name"], x["location"]])

    ## convert to data frame
    user_followers_df = pd.DataFrame(user_followers,
                                     columns=["prolific_user", "f_name", "f_screen_name", "f_location"])
    user_followers_df.to_csv("../Data/" + scrnName + "_followers.csv",
                             sep=',', mode="a", header=True,
                             encoding='utf-8', index=False)

    return user_followers


def searchTwitterUser(scrnName):
    try:
        user_timeline = twitter.get_user_timeline(screen_name=scrnName, count=20)
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
    #
    return parsed_dict


##---------------------------------------------------------------------
##  main() function calls
##---------------------------------------------------------------------
#def main():
#    ## define arrays
#    mylist = tweets = []
#
#    ## Get list of followers for both WSBT & SBT
#    followers_wsbt_infile = 'Data/sbtribune_all_followers_screen_names.txt'
#    followers_sbt_infile = 'Data/wsbt_all_followers_screen_names.txt'
#
#    with open(followers_wsbt_infile) as f:
#        l1 = f.read().splitlines()
#    with open(followers_sbt_infile) as f:
#        l2 = f.read().splitlines()
#
#    ## merge lists
#    mrgList = list(set(l1 + l2))
#
#    ## Random sampling select N random followers
#    followersAtRandomLst = [mrgList[i] for i in sorted(random.sample(xrange(len(mrgList)), 128))]
#
#    ## Get tweets from followers
#    tweets = tweets_for_random_list(followersAtRandomLst)
#
#    #    print tweets
#    #    print type(tweets)
#    print 'Done'


if __name__ == '__main__':
    """
    SearchTwitter
    Description: Search Twitter for a given user's tweets,
    its followers, and its followers tweets
    """

    #getTweetUser(sys.argv[1])
    tweet_data = searchTwitterUser(sys.argv[1])
    df = pd.DataFrame(tweet_data, columns = ['id', 'created_at','text','retweet_count','urls',
                                            'hashtags', 'user_mentions', 'favorite_count',
                                            'in_reply_to_status_id']
                     )
    df.to_csv("../Data/df_"+sys.argv[1]+".dat", sep=',', mode='a',index=False,encoding='utf-8')
