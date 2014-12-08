#!/usr/local/bin/python

import json, re, pprint, io, sys
import cPickle as pickle
import csv
from twython import Twython
from twython import TwythonAuthError, TwythonError

APP_KEY     = CONSUMER_KEY    = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET  = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

path = "Data/toy.csv"

#xx = re.search(r" (\w+@\w+\.com) ", "this xyz@example.com that")
#
#if xx:
#	print xx.group(1) # xyz@xyz.com
#else:
#	print "no"


def getTweetUser(sys_argv):
    data = []
    
    
    with open(sys_argv, 'r') as f:
        with open(sys_argv+'.userids','a') as fout:
            wrt = csv.writer(fout)
            f.readline()
            for line in f:
                token = line.split(",")[0]
                print token
                try:
                    tmpStr= twitter.show_status(id=token,trim_user=True,include_entities=True)
                except TwythonAuthError:
                    print TwythonAuthError
                    continue
                except TwythonError:
                    print TwythonError
                    continue
                
                #pprint (tmpStr)
                if (tmpStr.get("id",None)):
                    data.append( [tmpStr['id'], tmpStr['user']['id'],tmpStr['text']])
                    wrt.writerow([tmpStr['id'], tmpStr['user']['id'],tmpStr['text'].encode('utf-8')])

    print len(data), data[1:4]

    return

getTweetUser(sys.argv[1])

sys.exit()

with open(path,'rb') as infile:
	infile.readline()
	data = dict()
	for line in infile:
		xx = re.search(r"([0-9]+),([0-9]+),(.*)",line.rstrip())
		if xx:
			data[xx.group(1)] = { "userid": xx.group(2), "tweet": xx.group(3) } 
		#pprint.pprint (data)
		break

#json.dump("Data/temp.json", 
with open('Data/data.json', 'w') as f:
	json.dump(json.dumps(data),f) #f.write(unicode(json.dumps(data)))
	#pickle.dump(data,f)

with open('Data/data.json', 'rb') as fp:
	data = pickle.load(fp)
	print json.dumps(data, indent=2)
