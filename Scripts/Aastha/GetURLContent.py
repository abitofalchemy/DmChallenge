# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 12:39:28 2014

@author: aastha
"""

#import urllib2
#from HTMLParser import HTMLParser
#
## create a subclass and override the handler methods
#class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        print "Encountered a start tag:", tag
#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag
#    def handle_data(self, data):
#        print "Encountered some data  :", data
#
#data=urllib2.urlopen("http://www.washingtonpost.com/blogs/capitals-insider/wp/2014/11/02/after-tough-night-in-tampa-braden-holtby-accepts-the-blame/").read()
#parser = MyHTMLParser()
#parser.feed(data)

url="http://www.washingtonpost.com/blogs/capitals-insider/wp/2014/11/02/after-tough-night-in-tampa-braden-holtby-accepts-the-blame/"
#url="http://courageguy.tumblr.com/post/34667568793/a-true-courageous-moment-and-a-great-reminder-as-a"

from newspaper import Article
a = Article(url, language='en')

a.download()
a.parse()

print a.text