import json
import pandas as pd
import itertools
from pprint import pprint
from twython import Twython
from twython import TwythonAuthError, TwythonError
import math
import time

APP_KEY     = CONSUMER_KEY    = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

################################################################################
def fetch_timeline(screen_name = "WSBT"):
    
def getFollowers(user_screen_name):
    suser = twitter.show_user(screen_name=user_screen_name)
    fnum = 200
    pnum = int(math.ceil(float(suser["followers_count"]) / fnum))
    
    user_followers  =[]
    pages = []
    for i in range(pnum):
        pages.append("p"+str(i+1))
    
    oldpages = []
    for i in range(pnum):
        oldpages.append("p"+str(i))
    
    p0 = { "next_cursor": -1 } # So the following exec() call doesn't fail.
    
    for i in range(pnum):
        if i>1 :time.sleep(60)
        exec(pages[i]+" = twitter.get_followers_list(screen_name=user_screen_name, count=fnum, skip_status=1, cursor="+oldpages[i]+"['next_cursor'])")
    
    followers = []

    for p in range(pnum):
        try:
            exec("for i in range(fnum): followers.append("+pages[p]+"['users'][i])")
            except(IndexError):
                pass

    print(len(followers))
    
    
    for x in followers:
        #        print("""Name:  %s
        #            Username:  %s
        #            """ % (x["name"], x["screen_name"]))
        user_followers.append([user_screen_name,x["name"], x["screen_name"],x["location"]])

    ## convert to data frame
    user_followers_df = pd.DataFrame(user_followers,
                                     columns = ["prolific_user","f_name","f_screen_name", "f_location"])
                                     user_followers_df.to_csv("Data/prolific_tweeters.followers.csv", sep=',',mode="a", header=False,
                                                              encoding='utf-8',index=False)
return

#data = []
#with open('Data/tweets_from_followers_wsbt_sbt_08Nov14_130417.txt') as data_file:
#    for line in data_file:
#        json_object = json.loads(line)
#        data.append(json_object)
#
### parse the twitter stream
#df = pd.DataFrame(columns=['timestamp','name','tweet', 'retweetCnt', 'hastags', 'urlsCnt','mentionsCnt'])
#
#ix = 0
#for jobj in data:
#    #print '----------------------------'
#        #mydata = {  'name': jobj['user']['screen_name'],
#        #        'text': jobj['text']}
#        #print mydata['name'], 'wrote', mydata['text'] # or something
#        #print json.dumps(jobj,indent=2)
##    rtstatus = jobj.get('retweeted_status',None)
##print ix
#    parsedTweet = (jobj.get('created_at',None),
#               jobj.get('user',{}).get('screen_name',None),
#               jobj.get('text',{}),
#               jobj.get('retweeted_status',{}).get('retweet_count',{}),
#               jobj.get('entities',{}).get('hashtags',{}),
#               len(jobj.get('entities',{}).get('urls',{})),
#               len(jobj.get('entities',{}).get('user_mentions',{})))
#    
##    print '%s, %s, %s, %s, %s, %i, %i' % (jobj.get('created_at',None),
##                                      jobj.get('user',{}).get('screen_name',None),
##                                      jobj.get('text',{}),
##                                      jobj.get('retweeted_status',{}).get('retweet_count',{}),
##                                          jobj.get('entities',{}).get('hashtags',{}),
##                                          len(jobj.get('entities',{}).get('urls',{})),
##                                      len(jobj.get('entities',{}).get('user_mentions',{})))
#    df.loc[ix] = parsedTweet
#    ix +=1
#print df.shape
#
### time stamp for the ouputfile
#import datetime
#import time
#
#ts = time.time()
#st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')
#
#df.to_csv('Data/parsed_wsbt_twitter_stream_%s.txt' % st, sep=',',mode='w',encoding='utf-8',index=False)

def show_header(cmd_line_args):
    print cmd_line_args
    print '-'*80
    return

if __name__ == '__main__':
    # header
    show_header(sys.argv)

    #
    fetch_timeline("WSBT")