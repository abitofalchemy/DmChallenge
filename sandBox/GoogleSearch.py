# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 01:12:36 2014

@author: aastha
"""

import urllib2
import urllib
import simplejson

# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.

query="Ebola Virus"

url = ('https://ajax.googleapis.com/ajax/services/search/web'
       '?v=1.0&q=Paris%20Hilton&userip=USERS-IP-ADDRESS')

request = urllib2.Request(url, None)
response = urllib2.urlopen(request)

# Process the JSON string.
results = simplejson.load(response)
# now have some fun with the results...