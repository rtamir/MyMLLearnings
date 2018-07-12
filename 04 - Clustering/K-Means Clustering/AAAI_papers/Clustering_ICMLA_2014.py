"""
Created on Wed Feb 28 15:57:20 2018

@author: Ravikiran.Tamiri
NOT USEFUL
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.corpus import stopwords

import string
import math

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

dataset = pd.read_csv("ICMLA_2014.csv",encoding='latin-1')
#print(dataset['Title'])
#print(dataset['Abstract'][149])

#stop_words = set(stopwords.words('english'))
#stop_words.update([]) # remove it if you need punctuation 


X = dataset['abstract']

def text_process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    filtered_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return ' '.join(filtered_words)
    #return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    #return [stemmer.stem(t) for t in filtered_words]

for i in range(0,len(X)):
    X[i] = text_process(X[i])

# =============================================================================
# Y = dataset['session']
# 
# # Splitting the dataset into the Training set and Test set
# from sklearn.cross_validation import train_test_split
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 0)
# 
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.linear_model import SGDClassifier
# text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
#                          ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42))])
# 
# text_clf_svm = text_clf_svm.fit(X_train, Y_train)
# predicted_svm = text_clf_svm.predict(X_test)
# np.mean(predicted_svm == Y_test)
# 
# =============================================================================

from sklearn.feature_extraction.text import TfidfVectorizer
tfidvectorizer = TfidfVectorizer()
#tfidvectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,min_df=0.2,use_idf=True, tokenizer=text_process, ngram_range=(1,3))
tfidf_matrix = tfidvectorizer.fit_transform(X)

print(tfidf_matrix.shape)

terms = tfidvectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

#KMeans 

from sklearn.cluster import KMeans
wcss = []
for i in range(1, 105):
    kmeans = KMeans(n_clusters = i, init = 'k-means++')
    kmeans.fit(tfidf_matrix)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,105), wcss,'.')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()





