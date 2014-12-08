#!/usr/local/bin/python

#http://stackoverflow.com/questions/18045717/python-help-in-importerror-no-module-named-google
#http://topics.cs.princeton.edu/Science/
################################################################################
################################################################################
from __future__ import division
import sys
import json, ast, pickle
import pandas as pd
import numpy as np
from pprint import pprint
import re, string
from pattern.en import parse
import nltk
from pprint import pprint
from gensim import corpora, models, similarities
from itertools import chain
import nltk
from nltk.corpus import stopwords
from operator import itemgetter
from bs4 import BeautifulSoup
from pattern.web import Bing, SEARCH, plaintext


#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

def show_header(cmd_line_args):
    print cmd_line_args
    print '-'*80
    return

if __name__ == '__main__':
	# header
    show_header(sys.argv)

    tw_data = []
    with open('Data_Schurz/toy.json', 'rb') as fp:
        for line in fp:
            jObj = json.loads(line)
            if (jObj.get('text',None)):
                tw_data.append(json.dumps(jObj['text']).decode('unicode-escape').encode('utf8'))

#print len(tw_data)

    url_pattern = r'https?:\/\/(.*[\r\n]*)+'

    documents = [processTweet(BeautifulSoup(document).get_text()).strip(string.punctuation)  for document in tw_data]
    stoplist = stopwords.words('english')
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # expanded texts from Bing
    engine = Bing(license=None)
    exp_texts = []
    for tok_text in texts:
        if len(tok_text)>2:
            query=' '.join(tok_text)
            print 'Query',query.encode('utf8')
#            for result in engine.search(query, type=SEARCH, start=1):
#                exp_texts.append( repr(plaintext(result.title)))
#                #print 'Returns: %s Bing Search Titles, such as'%len(exp_texts)
#                print '\t%s' % repr(plaintext(result.title))

    sys.exit()

    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in exp_texts]
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    n_topics = 20
    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics)

    for i in range(0, n_topics):
        temp = lda.show_topic(i, 10)
        terms = []
        for term in temp:
            terms.append(term[1])
        print "Top 10 terms for topic #" + str(i) + ": "+ ", ".join(terms)

    print
    print 'Which LDA topic maximally describes a document?\n'
    print 'Original document: ' + documents[10]
#print 'Preprocessed document: ' + str(texts[10*10])
    print 'Matrix Market format: ' + str(corpus[10])
    print 'Topic probability mixture: ' + str(lda[corpus[10]])
    print 'Maximally probable topic: topic #' + str(max(lda[corpus[10]],key=itemgetter(1))[0])

    print
    print 'Original document: ' + documents[4]
    #print 'Preprocessed document: ' + str(texts[10*10])
    print 'Matrix Market format: ' + str(corpus[4])
    print 'Topic probability mixture: ' + str(lda[corpus[4]])
    print 'Maximally probable topic: topic #' + str(max(lda[corpus[4]],key=itemgetter(1))[0])
    
    print

#    for result in engine.search(query, cached=False):
#        print result.url
#        print result.title
#        #print result.text
#        #print result.groups()
##break