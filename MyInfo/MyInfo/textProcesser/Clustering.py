from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.covariance import EmpiricalCovariance
from Usefull import twogrammAnalys
from WikiRelations import GetWikiRelation
from Backend import MinidomParser
import matplotlib.pyplot as plt

import re
import pymorphy2

def splitCareful(text):
    return re.findall(r'(?u)\b\w\w+\b', text)


class Clustering:
    support = open("I:\keywords.txt", 'r', encoding='utf-8')
    support_strings = []
    stopwordFile = open("C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt", 'r', encoding='utf-8')
    stopwords = []
    analyzer = pymorphy2.MorphAnalyzer()

    def __init__(self):
        for line in self.support.readlines():
            self.support_strings.append(line)
        for line in self.stopwordFile.readlines():
            self.stopwords.append(line)

    # 1
    def getKeyComponent(self, docs):
        counter, tfMatrix = self.prepareTfIdf(docs)
        return self.pcaDecompose(counter, tfMatrix)

    #1
    def prepareTfIdf(self, docs):
        # todo rutez
        docs_clean = [' '.join([self.analyzer.parse(word)[0].normal_form for word in splitCareful(doc)]) for doc in docs]
        counter = TfidfVectorizer(stop_words=self.stopwords)
        tfMatrix = counter.fit_transform(docs_clean)
        return counter, tfMatrix

    # 2
    def convertToCovariance(self, tfidf):
        EC = EmpiricalCovariance()
        EC.fit(tfidf)
        return EC.covariance_

    #3
    def pcaDecompose(self, tfVectorized, tfMatrix):
        tfMatrix = tfMatrix.toarray()
        pca = PCA(svd_solver='full')
        return pca.fit_transform(tfMatrix)

    #4
    def svdDecomposition(self, tfMatrix, n_components):
        svdDecomposer = TruncatedSVD(n_components=n_components, algorithm='arpack')
        svdDecomposer.fit(tfMatrix)
        return svdDecomposer.components_

    def oneClassVisualise(self, color, X, Y):
        plt.plot(X, Y, color)

    #5
    def clusterizeKMeans(self, docs, n_of_clusters):
        counter, tfidf = self.prepareTfIdf(docs)
        visualizing2 = self.visualize(tfidf)
        print(visualizing2)
        self.svdDecomposition(tfidf, n_of_clusters)
        #self.oneClassVisualise('ro',visualizing2,visualizing2)
        #km = KMeans(8, n_jobs=4)
        #km.fit(tfidf.toarray())

    def visualize(self,tfidf):
        return self.svdDecomposition(tfidf,2)

    def getEssential(self):
        support = open("I:\keywords.txt", 'r', encoding='utf-8')
        support_strings = []
        stopwordFile = open("C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt", 'r',
                            encoding='utf-8')
        stopwords = []
        for line in support.readlines():
            support_strings.append(line)
        for line in stopwordFile.readlines():
            stopwords.append(line)

        return stopwords, support_strings

clust = Clustering()
stopwords = clust.getEssential()[0]
docs = [' '.join(item.words) for item in MinidomParser(stopwords=stopwords, stemmer=pymorphy2.MorphAnalyzer())
    .getWordsItems(10)]

clust.clusterizeKMeans(docs, 8)