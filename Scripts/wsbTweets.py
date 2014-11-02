import json
import pandas as pd
import itertools

from pprint import pprint
data = []
with open('Data/tweets.json') as data_file:
    for line in data_file:
        json_object = json.loads(line)
        data.append(json_object)

for jobj in data:
    #w print json.dumps(jobj)
#    for user in jobj.iteritems():
#        print user['screen_name']
    print '----------------------------'
    mydata = {  'name': jobj['user']['screen_name'],
                'text': jobj['text']}
    print mydata['name'], 'wrote', mydata['text'] # or something
    break
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
