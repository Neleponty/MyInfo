from Morphy import *
from WikiRelations import *
from sklearn.naive_bayes import MultinomialNB
import numpy
import math
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2



dp = DataPreparator(analyzer)
X1, Y1, XW_1, YW_1 = dp.GenerateWordsTrain(ngramm = 1, count = 10, window = 2)
X2, Y2, XW_2, YW_2 = dp.GenerateWordsTrain(ngramm = 2, count = 10, window = 2)
X3, Y3, XW_3, YW_3 = dp.GenerateWordsTrain(ngramm = 3, count = 10, window = 2)

# разные window
MB1.fit(numpy.array(X1), numpy.array(Y1))
MB2.fit(numpy.array(X2), numpy.array(Y2))
MB3.fit(numpy.array(X3), numpy.array(Y3))
# разные ngramm
MBWords1.fit(numpy.array(XW_1), numpy.array(YW_1))
MBWords2.fit(numpy.array(XW_2), numpy.array(YW_2))
MBWords3.fit(numpy.array(XW_3), numpy.array(YW_3))

x,x_w = dp.vectorizePredict(0, 3, "Человек но паук который грязным", 2)

# дать на вход сообщение, выход -> множество


print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))
x,x_w = dp.vectorizePredict(0, 1, "Сегодня утром из Барнаула пришло печальное известие — на 60-м году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов", 2)
print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))

x,x_w = dp.vectorizePredict(3, 3, "Сегодня утром из Барнаула пришло печальное известие — на 60-м году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов", 2)
print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))
x,x_w = dp.vectorizePredict(5, 5, "N году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов",2)
print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))
x,x_w = dp.vectorizePredict(6, 9, "N году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов",2)
print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))
x,x_w = dp.vectorizePredict(10, 12, "N году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов",2)
print('PREDICT=======================')
print(MB1.predict(x))
print(MB2.predict(x))
print(MB3.predict(x))
print(MBWords1.predict(x_w))
print(MBWords2.predict(x_w))
print(MBWords3.predict(x_w))

