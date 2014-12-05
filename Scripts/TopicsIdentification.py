# -*- coding: utf-8; -*-
#
# (c) 2014 S. Aguinaga
#
#
# MMC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MMC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
"""

Created on 03Dec14
@author: S. Aguinaga

"""

import nltk
import google
from newspaper import Article
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from itertools import izip
from pprint import pprint
import pickle

""" 
@script         TopicsIdentifcation.py
@description    Read corpus doc from URLs and run LDA
@howthisworks

Twitter User {wsbt/sbtribune} -> crawl timeline -> extract URLs -+
+-> PrepareText ->> sandBox/DocumentCorpus.txt

sandBox/DocumentCorpus.txt >>- Scripts/TopicsIdentification.py -+
+-> Topic Vectors Weighted e.g. {0.100*ads + 0.100*coke + 0.100*milk + 0.100*new +  .... }

"""

in_fpath="sandBox/DocumentCorpus.txt"
with open(in_fpath, 'r') as f:
    documents = pickle.load(f)

print "\nDocument size:",len(documents),type(documents)

# remove common words and tokenize
stoplist = set('for a of the and to in are is with its'.split())
texts = [[word for word in document[0].lower().split() if word not in stoplist]
         for document in documents]
#for document in documents:
#    print document
#    break

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

print lda.num_topics
for i in range(0, lda.num_topics):
    print (lda.print_topic(i))

#print type(lda), type(corpus_lda)
