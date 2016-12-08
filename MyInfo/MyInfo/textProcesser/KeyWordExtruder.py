from Clustering import *
from WikiRelations import *
from Backend import *

def wikies():
    wikies = GetWikiRelation().docReader(10)
    return [' '.join(wiki.words) for wiki in wikies]

def docs():
    return [' '.join(item.words) for item in MinidomParser().getWordsItems(10)]


clusterManager = Clustering()
counter, tfidf = clusterManager.prepareTfIdf(wikies())
vocabulary = counter.vocabulary_
#covariance_matrix = clusterManager.convertToCovariance(tfidf)
r,c = tfidf.shape
named_array = []

for row in range(r):
    for column in range(c):
        row_vector = tfidf[row:]


sorted = [[column for column in covariance_matrix[row:]] for row in range(r)]

