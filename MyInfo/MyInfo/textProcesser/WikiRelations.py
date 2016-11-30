import os
import pymorphy2
import datetime
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import numpy
import scipy
import pymystem3
import json

class GetWikiRelation():

    PATH_TO_STOP_WORDS = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt'

    relevant_themes = []
    stopwords = []
    analyzer = pymorphy2.MorphAnalyzer()

    def __init__(self):
        self.relevant_themes = self.readFrom("I:\\keywords.txt")
        self.stopwords = self.readFrom(self.PATH_TO_STOP_WORDS)

    def readFrom(self,path):
        file = open(path, 'r', -1, 'utf-8')
        return file.readlines()
        ##def step_extracting(self):

    def docReader(self, i):
        wikies = []
        directory = "I:\\Folder\\"
        for i in range(3):

            wikitext = []
            wikihead = []
            for dir in (os.listdir(directory)[:100]):
                with open(directory + dir, encoding='utf-8') as f:
                    wiki = json.loads(f.read())
                    wikihead.append(wiki)
                    wikitext.append(wiki['Content'])

            toDocument_relevant = self.GetKeyWordsToEachDoc(wikitext)

            for i in range(len(toDocument_relevant)):
                wikies.append((wikihead[i], toDocument_relevant[i]))

        return wikies

    def Vectorized(self):
        wikies = self.docReader(10)
        docs = []
        for wiki in wikies:
            var = wiki[0].get('Header') + ' '.join(wiki[0].get('Categories'))
            gar = list(wiki[0].get('Links'))
            print(wiki[1])
            sar = ' '.join(list(wiki[0].get('Links'))) + ' '.join(wiki[1])
            keys = wiki[0].get('Header') + ' '.join(wiki[0].get('Categories')) + ' '.join(wiki[0].get('Links'))\
                   + ' '.join(wiki[1])
            docs.append(keys)

        A = CountVectorizer().fit_transform(docs)
        print(A)

        # Дерево википедии


        vector = []

        # from titles and categories

        # from tf-idf support


    # слова в нормальной форме, выжны вхождения
    # не так важно, как вхождения терминов
    def GetKeyWordsToEachDoc(self, documents):
        tfidfTransformer = TfidfVectorizer(stop_words=self.stopwords,use_idf=False)
        tfidfMatrix = scipy.sparse.csc_matrix(tfidfTransformer.fit_transform(documents))
        r, v = tfidfMatrix.shape
        docs_vector = []
        print(r, v)

        words = [(key) for key, value in tfidfTransformer.vocabulary_.items()]
        for i in range(r):
            pairs = []
            for j in range(v):
                pairs.append((tfidfMatrix[i,j],words[j]))
            bests = sorted(pairs, key=lambda item: item[0])

            if v < 100:
                bests = bests[:int(v/2)]
            else:
                bests = bests[:100]
            wordnet = []
            for word in bests:
                tag = self.analyzer.parse(word[1])[0].tag
                if tag.POS == 'NOUN':
                    wordnet.append((word[0], word[1]))
            docs_vector.append(wordnet)
        return docs_vector

GetWikiRelation().Vectorized()