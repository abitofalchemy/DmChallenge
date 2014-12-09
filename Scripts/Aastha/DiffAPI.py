# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 01:58:43 2014

@author: aastha
"""

from google import search
from google import filter_result
from google import get_page
from newspaper import Article

retreived_urls=[]
for url in search('try game tribez. URL gameinsight', stop=20):
    print(url)
    retreived_urls.append(url)
    
data=[]

for i in range(len(retreived_urls)):
    a = Article(retreived_urls[i], language='en')
    a.download()
    a.parse()
    #data = sock.recv(256)
    print a.text
    data.append(a.text)   
    

#html_doc=get_page(retreived_urls[2])    
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc)
#data=soup.get_text()

from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]
             
lda = LdaModel(corpus, num_topics=100)  # train model
print(lda[doc_bow]) # get topic probability distribution for a document