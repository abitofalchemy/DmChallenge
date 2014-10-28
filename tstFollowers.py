#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import twitter

################################################################
##  main
###############################################################
if __name__ == "__main__":
	
	api = twitter.Api()	
	## my account 
	a = mod_twitter.Api('abitofalchemy', 'twit!0xB')
	friends, counter = [], 1
	while not len(friends) % 100:
		# Get all Friends and store in 'friends',
		# till num of a page is < 100
		friends += a.GetFriends('SBTribune', page=counter)
		# page=integer is the new keyword argument
		counter += 1

	print len(friends) # To verify
