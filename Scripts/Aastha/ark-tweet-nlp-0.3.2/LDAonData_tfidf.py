# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 14:46:35 2014

@author: aastha
"""

import pickle
fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/CleanedCorpus2.txt"
with open(fpath, 'rb') as f:
    documents = pickle.load(f)

print "read data"

documents=documents[0:10]

print "tokenizing"
#tokenize
texts = [[word for word in document.lower().split()] for document in documents]

print "removing words that occur once"
# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

from gensim import corpora
from gensim.models import ldamodel, TdidfModel

print "dictionary"
dictionary = corpora.Dictionary(texts)
#fpath='/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/LDA/Train880/Dictionary.txt'
#dictionary.save_as_text(fpath)

print "mapping text"
corpus = [dictionary.doc2bow(text) for text in texts]
#fpath='/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/LDA/Train880/Corpus.txt'
#with open(fpath, 'wb') as f:
#    pickle.dump(corpus, f)

tfidf = TfidfModel(corpus)
#print "training"
#lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10)
#corpus_lda = lda[corpus]
#
#for i in range(0, lda.num_topics):
#    print lda.print_topic(i)

#f = open('/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/LDA/Train880/LdaTopic.txt', 'w')
#for i in range(0, lda.num_topics):
#    f.write(lda.print_topic(i))
#    f.write("\n")
##    print lda.print_topic(i)
#    
#f.flush()
#f.close()    
#
#f = open('/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/LDA/Train880/LdaTweetTopic.txt', 'w')
#for doc in corpus_lda:
#    f.write(''.join(str(doc)))
#    f.write("\n")    
#    print doc
#
#f.flush()
#f.close()