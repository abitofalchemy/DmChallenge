import json
import pandas as pd
import itertools

from pprint import pprint
data = []
with open('Data/tweets_from_followers_wsbt_sbt_08Nov14_130417.txt') as data_file:
    for line in data_file:
        json_object = json.loads(line)
        data.append(json_object)

## parse the twitter stream
df = pd.DataFrame(columns=['timestamp','name','tweet', 'retweetCnt', 'hastags', 'urlsCnt','mentionsCnt'])

ix = 0
for jobj in data:
    #print '----------------------------'
        #mydata = {  'name': jobj['user']['screen_name'],
        #        'text': jobj['text']}
        #print mydata['name'], 'wrote', mydata['text'] # or something
        #print json.dumps(jobj,indent=2)
#    rtstatus = jobj.get('retweeted_status',None)
#print ix
    parsedTweet = (jobj.get('created_at',None),
               jobj.get('user',{}).get('screen_name',None),
               jobj.get('text',{}),
               jobj.get('retweeted_status',{}).get('retweet_count',{}),
               jobj.get('entities',{}).get('hashtags',{}),
               len(jobj.get('entities',{}).get('urls',{})),
               len(jobj.get('entities',{}).get('user_mentions',{})))
    
#    print '%s, %s, %s, %s, %s, %i, %i' % (jobj.get('created_at',None),
#                                      jobj.get('user',{}).get('screen_name',None),
#                                      jobj.get('text',{}),
#                                      jobj.get('retweeted_status',{}).get('retweet_count',{}),
#                                          jobj.get('entities',{}).get('hashtags',{}),
#                                          len(jobj.get('entities',{}).get('urls',{})),
#                                      len(jobj.get('entities',{}).get('user_mentions',{})))
    df.loc[ix] = parsedTweet
    ix +=1
print df.shape

## time stamp for the ouputfile
import datetime
import time

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%d%b%y')

df.to_csv('Data/parsed_wsbt_twitter_stream_%s.txt' % st, sep=',',mode='w',encoding='utf-8',index=False)

##############################################################
#   Unsed code, but saved in case it's needed
#
##############################################################
#	pprint(dat_json)

#    for line_str in f:
#        jsonObj = json.loads(line_str)
#
#        for k,v in jsonObj.iteritems():
#            print k,v
#            break
##with open('tweets.json','r') as data_file:
##	#data = json.load(json.dumps([data_file]))
##	#data = json.load(json.dumps([json.JSONEncoder().encode(data_file)]))
##	#pprint(data)
##	data = json.load(data_file)
##	for k,v in data.iteritems():
##		    print k,v
##
##	sys.exit()
#        for k,v in ret.iteritems():
#            print k,v
