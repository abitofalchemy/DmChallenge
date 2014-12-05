# -*- coding: utf-8 -*-
"""
@author: aastha
"""

import nltk
from pygoogle import pygoogle
from newspaper import Article
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from itertools import izip

tweet="i have completed the quest 'another try' in the android game the tribez. URL androidgames, gameinsight"
tokens = nltk.word_tokenize(tweet)
tagged_tweet=nltk.pos_tag(tokens)

tweet_nouns=[]

for i in range(len(tagged_tweet)):
    if(tagged_tweet[i][1].find('NN')!=-1):
        tweet_nouns.append(tagged_tweet[i][0])

query=' '.join(tweet_nouns)
g = pygoogle(query)
g.pages = 2
print '*Found %s results*'%(g.get_result_count())
retreived_urls=g.get_urls()

data=[]

for i in range(len(retreived_urls)):
    a = Article(retreived_urls[i], language='en')
    a.download()
    a.parse()
    #print a.text
    data.append(a.text)
    
documents=data
# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# I can print out the documents and which is the most probable topics for each doc.
lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=5)
corpus_lda = lda[corpus]

for i in range(0, lda.num_topics-1):
    print lda.print_topic(i)
