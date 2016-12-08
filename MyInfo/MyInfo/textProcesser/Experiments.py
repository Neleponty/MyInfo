# coding=utf-8
# -*- coding: utf-8 -*-,
from Morphy import *
from WikiRelations import *
from sklearn.naive_bayes import MultinomialNB
import numpy
import math
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2

PATH_TO_STOP_WORDS = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt'
stopwords = open(PATH_TO_STOP_WORDS, 'r', encoding='utf-8').readlines()
keywords = open("I:\\keywords.txt", 'r', encoding='utf-8').readlines()
SDP = SimpleDataProcessor(stopwords, keywords)
result = SDP.simplePredict([" Сегодня утром из Барнаула пришло печальное известие — на 60-м году жизни скончался выдающийся поэт, член Союза Писателей Росссии Владимир Мефодьевич Башунов. В последние годы поэт тяжело болел, у него была острая сердечная недостаточность, а в 2002 году его настиг инфаркт миокарда.",])
print(result)

dp = DataPreparator(analyzer)

dict1 = {}
dict1.update([(u"Жордан",1),])
dict2 = {}
dict2.update([(u"Корень",1),])
dict3 = {}
dict4 = {}
dict3.update([(u"Юпитер",1),])
dict4.update([(u"Астроном",1),])
dict5 = {}
dict5.update([(u"Легенда",1),])
dict6 = {}
dict6.update([(u"Марсианин",1),])
dict7 = {}
dict7.update([(u"Сложный случай",1),])

X, Y = dp.Split_Vectorize([u"Жордан был очень слаб", u"Корень был мудрым", u"Юпитер был юношей",
                           u"Астроном, который не легионер", u"Легенда это вымысел", u"Что поделать, Марсианин",
                           "Сложный случай"],
                          [dict1,dict2,dict3,dict4,dict5,dict6,dict7],2,1)
t = MB.fit(numpy.array(X), numpy.array(Y))
# pos_start, pos_end, alltext, window
# Человек но паук - объект, который - окружение
x = dp.vectorizePredict(0, 3, "Человек но паук который грязным",1)

print('PREDICT=======================')
print(MB.predict(x))
