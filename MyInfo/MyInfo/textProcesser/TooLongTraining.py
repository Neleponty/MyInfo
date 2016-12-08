from WikiRelations import *
from Morphy import *
from sklearn.naive_bayes import MultinomialNB
import numpy
import math
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2


MB1 = MultinomialNB(alpha=0.01)
MB2 = MultinomialNB(alpha=0.01)
MB3 = MultinomialNB(alpha=0.01)
MBWords1 = MultinomialNB(alpha=0.01)
MBWords2 = MultinomialNB(alpha=0.01)
MBWords3 = MultinomialNB(alpha=0.01)

analyzer = pymorphy2.MorphAnalyzer()
#где 3 - длина, которую стоит учитывать для термина
#окружение - длина не важна
dp = DataPreparator(analyzer)

class BaseMN:
    support = open("I:\keywords.txt", 'r', encoding='utf-8')
    support_strings = []
    stopwordFile = open("C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt", 'r', encoding='utf-8')
    stopwords = []
    SDP = None

    MB1 = MultinomialNB(alpha=0.01)
    MB2 = MultinomialNB(alpha=0.01)
    MB3 = MultinomialNB(alpha=0.01)

    def __init__(self):
        for line in self.support.readlines():
            self.support_strings.append(line)
        for line in self.stopwordFile.readlines():
            self.stopwords.append(line)
        self.SDP = SimpleDataProcessor(self.stopwords, self.support_strings)


        #    MBWords1 = MultinomialNB(alpha=0.01)
#    MBWords2 = MultinomialNB(alpha=0.01)
#    MBWords3 = MultinomialNB(alpha=0.01)

    #X1 == X_w1 == Y1
    def fit(self, X1, X_w1, X2, X_w2, X3, X_w3, Y1, Y2, Y3):
        # разные window
#          MBWords1.fit(X_w1, Y1)
           MB1.fit(X1, Y1)

           MB2.fit(X2, Y2)
#          MBWords2.fit(X_w2, Y2)
# разные ngramm
           MB3.fit(X3, Y3)
#          MBWords3.fit(X_w3, Y3)

    def getKeywordsWithTemplates(self,doc):
        print('start')
        keywords = self.SDP.simplePredict([doc,])
        return keywords

    def getKeywords(self,doc):
        heruisticKeywords = self.getKeywordsWithTemplates(doc)

        nOne = dp.prepareWordsFeatures(1, splitCareful(doc),{})
        nTwo= dp.prepareWordsFeatures(2, splitCareful(doc),{})
        nThree = dp.prepareWordsFeatures(3, splitCareful(doc),{})

        X1,Y1 = dp.vectorizeContext([nOne,], 2)
        X2,Y2 = dp.vectorizeContext([nTwo,], 2)
        X3,Y3 = dp.vectorizeContext([nThree,], 2)

#         X1_w, Y1 = dp.vectorizeWords([nOne,], 1)
#         X2_w, Y2 = dp.vectorizeWords([nTwo,], 2)
#         X3_w, Y3 = dp.vectorizeWords([nThree,], 3)

        X_predicted1 = [(MB1.predict(X1[i]), MB1.predict_proba(X1[i]), nOne[0][i][0]) for i in range(len(X1))]
        X_predicted2 = [(MB2.predict(X2[i]), MB2.predict_proba(X2[i]), nTwo[0][i][0]) for i in range(len(X2))]
        X_predicted3 = [(MB3.predict(X3[i]), MB3.predict_proba(X3[i]), nThree[0][i][0]) for i in range(len(X3))]

#            X_Wpredicted1 = [(MBWords1.predict(X1_w[i]), MBWords1.predict_proba(X1_w[i]), nOne[0][i]) for i in range(len(X1_w))]
#           X_Wpredicted2 = [(MBWords2.predict(X2_w[i]), MBWords2.predict_proba(X2_w[i]), nTwo[0][i]) for i in range(len(X2_w))]
#          X_Wpredicted3 = [(MBWords3.predict(X3_w[i]), MBWords3.predict_proba(X3_w[i]), nThree[0][i]) for i in range(len(X3_w))]

        X_sure1 = []
        X_sure2 = []
        X_sure3 = []

        # Todo Positions
        for i in range(len(X_predicted1)):
            if X_predicted1[i][0] == 1 and X_predicted1[i][2] in heruisticKeywords:
                print(X_predicted1[i][2])
#                if  X_predicted1[i][0] == 1 and X_Wpredicted1[i][0] == 1:
#                   X_sure1.append((X_predicted1[i][1], X_Wpredicted1[i][1], nOne[0][i]))

        for i in range(len(X_predicted2)):
            if X_predicted2[i][0] == 1 and X_predicted2[i][2] in heruisticKeywords:
                print(X_predicted2[i][2])
                #
#              if X_predicted2[i][0] == 1 and X_Wpredicted2[i][0] == 1:
#                 X_sure2.append((X_predicted2[i][1], X_Wpredicted2[i][1], nTwo[0][i]))

        for i in range(len(X_predicted3)):
            if X_predicted3[i][0] == 1 and X_predicted3[i][2] in heruisticKeywords:
                print(X_predicted3[i][2])
#            if X_predicted3[i][0] == 1 and X_Wpredicted3[i][0] == 1:
 #               X_sure3.append((X_predicted3[i][1], X_Wpredicted3[i][1], nThree[0][i]))


        print('========================================================')
        print(str(X_predicted1) + "|" + str(X_predicted1))
        #print(str(X_Wpredicted1) + "|" + str(X_Wpredicted1))
        print('========================================================')

        print(str(X_predicted2) + "|" + str(X_predicted2))
        #print(str(X_Wpredicted2) + "|" + str(X_Wpredicted2))
        print('========================================================')

        print(str(X_predicted3) + "|" + str(X_predicted3))
        #print(str(X_Wpredicted3) + "|" + str(X_Wpredicted3))
        print('========================================================')

#            print(X_sure1)
#            print(X_sure2)
#            print(X_sure3)


X1,Y1, X_w1,Y_w1 = dp.GenerateWordsTrain(ngramm=1,count=1000, window=2)
X2,Y2, X_w2,Y_w2 = dp.GenerateWordsTrain(ngramm=2,count=1000, window=2)
X3,Y3, X_w3,Y_w3 = dp.GenerateWordsTrain(ngramm=3,count=1000, window=2)

baseMN = BaseMN()
baseMN.fit(X1, X_w1, X2, X_w2, X3, X_w3, Y1, Y2, Y3)
baseMN.getKeywords(u"Сегодня утром из Барнаула пришло печальное известие — на 60-м году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов. В последние годы поэт тяжело болел, у него была острая сердечная недостаточность, а в 2002 году его настиг инфаркт миокарда.")

print('Finished')


