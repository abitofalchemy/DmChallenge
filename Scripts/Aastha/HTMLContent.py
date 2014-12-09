# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 14:07:32 2014

@author: aastha
"""

from bs4 import BeautifulSoup
import urllib2

data=urllib2.urlopen("http://www.washingtonpost.com/blogs/capitals-insider/wp/2014/11/02/after-tough-night-in-tampa-braden-holtby-accepts-the-blame/").read()
#parser = MyHTMLParser()

soup = BeautifulSoup(data)
print(soup.get_text())