# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 14:10:03 2014

@author: aastha
"""

import pickle
fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/DocumentCorpus.txt"
with open(fpath, 'rb') as f:
    documents = pickle.load(f)

import re
from nltk.corpus import stopwords
stop = stopwords.words('english')    
stop2=["a","able","about","across","after","all","hr","rt","re","ll","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]
stop3=["website","find","search","exist","ps","click","pin","back","ve","always","oh","unless","one","time","first","year","day","two","even","people","m","work","1","2","please","seems","want","go","want","days","delete","know","see","way","years","show","keep","new","tweet","browser","web","site","javascript","page","available","logged","really","user","com","think","location","twitter","option","history","page","try","doesn","cute","thing","mr","turn","link","info","list","enable","pinterest","love","tweets","switch","gm","account","content","sign","god","email","pin","use","enabled","much","website","click","use","thread","posts","shit","join","login","register","help","app","full","currently","pm","review","blog","exist","provide","currently","url","enter","error","register"]

stoplist= list(set(stop) | set(stop2))
stoplist = list(set(stoplist)|set(stop3))

def tfidf_fs(doc):
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc)
    #print tfidf_matrix.todense()
    
    vocab=tfidf_vectorizer.vocabulary_
    inv_vocab = {v: k for k, v in vocab.iteritems()}

    import itertools
    import numpy as np    
    cx = tfidf_matrix.tocoo()    
    
    vals=[]    
    for v in itertools.izip(cx.data):
        vals.append(v)
    
    val_array = np.array(vals)
    threshold=np.percentile(val_array,99)
    
    final_doc=[]
    for i in range(tfidf_matrix.shape[0]):
        for j in range(tfidf_matrix.shape[1]):
            if(tfidf_matrix[i,j]>threshold):
                key=inv_vocab.get(j)
                final_doc.append(key)
     
    final_doc=' '.join(final_doc)
    return final_doc       

corpus=[]
for i in range(len(documents)):
#for i in range(177,182):
    print i
    doc=documents[i]
    tmp=''.join(doc)
    if(doc==[] or tmp==''):
        continue
    clean_doc=[]
    for d in doc:
        c=' '.join(re.sub("(@[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)"," ",d).split())
        c=c.lower()
        c=[i for i in c.split() if i not in stoplist]
        c=' '.join(c)
        if(c!=''):
            clean_doc.append(c)
    pruned_doc=tfidf_fs(clean_doc)
    corpus.append(pruned_doc)
                
#doc=documents[0]
#from sklearn.feature_extraction.text import TfidfVectorizer
#
#tfidf_vectorizer = TfidfVectorizer()
#tfidf_matrix = tfidf_vectorizer.fit_transform(doc)
#print tfidf_matrix.todense()
#
#vocab=tfidf_vectorizer.vocabulary_
#import itertools
#cx = tfidf_matrix.tocoo()    
#for i,j,v in itertools.izip(cx.row, cx.col, cx.data):
#    (i,j,v)
#
#    final_doc=[]        
#    for i,j,v in itertools.izip(cx.row, cx.col, cx.data):
#        new_d=[]
#        if(v>threshold):
#            new_d.append(inv_vocab.get(j))
#        new_d=' '.join(new_d)
#        final_doc.append(new_d)
#            
#
#for i in np.unique(cx.row):
#    for j,v in itertools.izip(cx.col,cx.data):
#        


#corpus=[]
#for i in range(len(documents)):
#    print i
#    tweetdoc=' '.join(documents[i])
#    tweetdoc=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweetdoc).split())
#    tweetdoc=tweetdoc.lower()
#    tweetdoc=[i for i in tweetdoc.split() if i not in stoplist]
#    tweetdoc=' '.join(tweetdoc)
#    corpus.append(tweetdoc)
#    
fpath="/Users/aastha/Desktop/Semester3/Data Mining/CourseProject/Data/FinalData/TFIDF/CleanedCorpus99(2).txt"
with open(fpath, 'wb') as f:
    pickle.dump(corpus, f)