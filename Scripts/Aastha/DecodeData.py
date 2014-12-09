# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 15:46:01 2014

@author: aastha
"""

import json
import pprint

path="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/tweets.txt"
logfilepath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/Formattedtweets.txt"
out_path="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/TwitterFields.csv"

data = []
with open(path) as f:
    for line in f:
        data.append(json.loads(line))

logfile=open(logfilepath,'w')
pprint.pprint(data,logfile)

creation_time=""
actual_creation=""
actual_favcount=""
actual_user_id=""
actual_user_screenname=""
hashtag=""
retweet_count = "" 
fav_count=""
replyto= ""
text = ""
user_screenname=""
user_screenname=""

out_file=open(out_path,'w')
out_file.write("creation_time, actual_creation, actual_favcount, actual_user_id, actual_user_screenname, hashtag, retweet_count,fav_count, replyto, text, user_screenname, user_id\n")

for i in range(len(data)):
    #if we do not have creation time, then we can skip that tweet and all other fields about it    
    if data[i].has_key('created_at'):
        creation_time=data[i]['created_at']
    else:
        continue
    if(data[i].has_key('retweeted_status')):
        #retweet status (we need to keep track if it SBT) 
        actual_creation=data[i]['retweeted_status']['created_at']
        actual_favcount=data[i]['retweeted_status']['favorite_count']
        actual_user_id=data[i]['retweeted_status']['user']['id_str']
        actual_user_screenname=data[i]['retweeted_status']['user']['screen_name']
    
    #more Tweet information
    if(data[i]['entities'].has_key('hashtags')):
        if(len(data[i]['entities']['hashtags'])>0):
            hashtag= data[i][u'entities'][u'hashtags'][0]['text']
    #url1= data[i][u'entities'][u'media'][0][u'expanded_url']
    #url2= data[i][u'entities'][u'media'][0][u'url']
    retweet_count = data[i]['retweet_count']    
    fav_count=data[i]['favorite_count']
    replyto= data[i]['in_reply_to_screen_name']
    text = data[i][u'text'].replace(',','')
    text = text.replace('\n','')
    text = text.replace('\r','')

    #user information (to know what each individual user is doing)
    user_screenname=data[i]['user']['screen_name']
    user_id=data[i]['user']['id_str']  
    out_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'% (creation_time, actual_creation, actual_favcount, actual_user_id, actual_user_screenname, hashtag, retweet_count,fav_count, replyto, text, user_screenname, user_id))    
    
out_file.flush()
out_file.close()
