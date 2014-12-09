# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 00:28:25 2014

@author: aastha
"""

from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from itertools import izip

documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

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

#lda = ldamodel.LdaModel(corpus, num_topics=100)  # train model

# I can print out the documents and which is the most probable topics for each doc.
lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=5)
corpus_lda = lda[corpus]

for i in range(0, lda.num_topics):
    print lda.print_topic(i)

for doc in corpus_lda:
    print doc
#for t in topics:
#    print lsi.show_topics(t[0])