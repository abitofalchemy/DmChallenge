# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 15:46:01 2014

@author: aastha
"""

import json
import pprint

#path="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/tweets.txt"
##json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
#
#with open(path) as json_data:
#    d = json.loads(json_data)
#    json_data.close()
#    pprint(d)
    
#path="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Codes/sample.json"
path="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/tweets.txt"
logfilepath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/Formattedtweets.txt"

#json_data=open(path)
#
#data = json.load(json_data)
#pprint(data)
#json_data.close()

data = []
with open(path) as f:
    for line in f:
        data.append(json.loads(line))

#with open(logfilepath, "w") as fout:
#    fout.write(pprint.pformat(vars(pprint)))

logfile=open(logfilepath,'w')
pprint.pprint(data,logfile)

#with open('data.json') as data_file:    
#    data = json.load(data_file)
#pprint(data)