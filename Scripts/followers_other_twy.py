from twython import Twython
import time
import csv
import pandas as pd
from pprint import pprint
import json

APP_KEY     = CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


############################################################################

user_timeline = twitter.get_user_timeline(screen_name='SBTribune', count=1,include_rts=False)
last_post_id = user_timeline[0]['id']
post_id = [0]
cnt = 50
tweet_data = []
while (cnt >1 and post_id[0] != last_post_id):
    print last_post_id
    user_timeline = twitter.get_user_timeline(screen_name='SBTribune', max_id=last_post_id, count=200,include_rts=False)
    for tweet in user_timeline:
        tweet_data.append([tweet])
    post_id = [x['id'] for x in user_timeline]
    last_post_id = post_id[len(post_id)-1]

    cnt -= 1
    time.sleep(60)

#df  = pd.DataFrame(tweet_data) #("Data/sbtribune_raw_tweets.csv") as cache_file:
##print df.head()
#df.to_csv("Data/wsbt_raw_tweets.csv", sep=',',mode='a',encoding='utf-8',index=False, header=False)
#print json.dumps(tweet_data)
with open('Data/sbtribune_raw_tweets_1.csv', 'a') as outfile:
    json.dump(tweet_data, outfile)

#time.sleep(60)

#print df.head()
#df.to_csv('out_file.txt', sep=',',mode='w',encoding='utf-8',index=False)
#print(twitter.get_followers_list()['ids'])
#for result in search['users']:
#    #time_zone =result['time_zone'] if result['time_zone'] != None else "N/A"
#    #print result["screen_name"].encode('utf-8')
#    df.loc[inx]= result["screen_name"].encode('utf-8')
#        inx +=1
#        next_cursor = search["next_cursor"]


