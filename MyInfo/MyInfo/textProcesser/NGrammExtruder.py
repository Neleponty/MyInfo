from sklearn.naive_bayes import MultinomialNB
import re
from Backend import MinidomParser, Word, TextItem

import pymorphy2
import math

analyzer = pymorphy2.MorphAnalyzer()
stop = ['', ]
items = MinidomParser(analyzer, stop).getWordsItems(1, tokenize=True)


def extractNgramms(n, words):
    result = []
    start = 0

    while start < len(words):
        result.append(words[start: start + n])
        if start + n > len(words):
            start = len(words)
        start += 1

    return result


def levensteinDistance(therm, therm_to_check):
    difference = math.fabs(len(therm) - len(therm_to_check))
    therm1 = [word.lower() for word in therm_to_check.split()]
    therm2 = [word.lower() for word in therm.split()]

    for i in range(min(len(therm1), len(therm2))):
        # предпологаем наивную конструкцию, вставка всегда хуже,чем изменение
        # O(n)
        for j in range(min(len(therm1[i]), len(therm2[i]))):
            if therm1[i][j] != therm2[i][j]:
                difference += 1

    return float(difference/len(therm_to_check))

def search(text_words, keywords):
    words = []
    threshold = lambda own: own[0] < 0.3
    for i in range(len(keywords)):
        if len(keywords[i].split()) == 1:
            words_distance_word = [(levensteinDistance(text_words[j], keywords[i]), text_words[j]) for j in range(len(text_words))]
            nearest_words = [item[1] for item in filter(lambda own:own[0] < 0.3 , words_distance_word)]
            words.append(nearest_words)

        else:
            window = len(keywords[i].split())
            ngramms = extractNgramms(window, text_words)
            ngramms_distance_index = [(levensteinDistance(' '.join(ngramms[j]), ' '.join(keywords[i])), ngramms[j])
                                      for j in range(len(ngramms))]
            nearest_ngramms = [item[1] for item in filter(threshold, ngramms_distance_index)]
            words.append(nearest_ngramms)

    return words

print('###################')
print(search(items[0].words,items[0].control_key_words))
print('###################')


# 1. научиться находить делители Ngramm
def divideToNgramms():
    print(1)


# 1. научиться находить Ngramm-ы по статистикам (инфа есть => 1 и 2 независимы)


def getStatistics(words):
    result = []
    for word in words:
        morph = analyzer.parse(word)[0]
        # взять у Mystem
        result.append(morph.tag)
    return result


# p(w|w\w\w\w) == p(w)p(w)p(w)
def StudentStatistics(posteriorProb, contained_objects, frequency_objects, objects_count):
    objects_prob = []
    for object in contained_objects:
        objects_prob.append(frequency_objects[object] / objects_count)

    apriorProb = 0
    for prob in objects_prob:
        apriorProb *= prob
    return math.fabs(apriorProb - posteriorProb)


def getCounted(uniques, all_morphs):
    uniques_counted = []
    for unique in uniques:
        count = 0
        for morph in all_morphs:
            if unique == morph:
                count += 1
        uniques_counted.append((unique, count))
    return uniques_counted


#############################3# Распределение NGRAMM по морфологии/ключевым словам
def GetDistribOfTitles(titles):
    result = []
    for title in titles:
        morphology = ''
        for word in title.split():
            morph = analyzer.parse(word)[0]
            # todo посмотреть на probability p(none|w\w\w\w\w)
            # или взять у Mystem
            if morph.tag.POS == None:
                pos = 'None'
            else:
                pos = morph.tag.POS
            if morph.tag.case == None:
                case = 'None'
            else:
                case = morph.tag.case
            morphology += pos + ' ' + case + ' '
        result.append(morphology)

    uniques = list(set(result))
    counted_uniques = getCounted(uniques, result)
    print(counted_uniques)

    count = sum([item[1] for item in counted_uniques])


words = [item.control_key_words for item in items]
inputs = []
for word in words:
    for input in word:
        inputs.append(input)
GetDistribOfTitles(inputs)


# Распределение Студента нужно?
# for morph in uniques:
#    postProb = morph[1]/count
#    StudentStatistics(postProb ,)




##############################################################33
# ВНЕШНИЕ СТАТИСТИКИ КЛЮЧЕВЫХ СЛОВ(Любого размера из любого источника)
##############################################################

# Выделить все статистики в тексте. для каждого keyword - статистики всех вхождений
def morphVector_in_Norm_form(text_keywords, text_words, window):
    text_statistic = []
    # все статистики в тексте
    for keyword in text_keywords:
        for i in range(text_words):
            morph_vector = []
            # выделим границы
            if text_words[i] == keyword:
                if i < window:
                    start = 0
                else:
                    start = i - window
                if (i + window) > len(text_words) - 1:
                    end = len(text_words)
                else:
                    end = i + window
                nearby_words = text_words[start:i] + text_words[i:end]

                # вся статистика по границе
                morph_vector = getStatistics(nearby_words)
            text_statistic.append((keyword, morph_vector))
    return text_statistic


# Все совпадения наборы слов <-> текстов
def KeyWordParamsDistrib(keywords, texts, window):
    assert (len(keywords) == len(texts))
    all_text_statistics = []
    # todo: приведение именных сущностей к нормальной форме
    for i in range(len(texts)):
        # [**text1** [[(keyword1,статистики_nearby_keyword1)], [*****], ], [статистики_nearby_слово2, [*****] ], ]
        one_text_statistic = morphVector_in_Norm_form(keywords[i], texts[i], window)
        all_text_statistics.append(one_text_statistic)
    return all_text_statistics


# F(i)
class Feature:
    prob_distr = {}
    Ni = 0
    smoothing = 0.01

    def __init__(self, class_names):
        self.prob_distr = [(name, 0) for name in class_names]

    def probability(self, class_v):
        ni = self.prob_distr[class_v][1]
        d = len(self.prob_distr)
        likehood = (ni + self.smoothing) / (self.Ni + d * self.smoothing)
        return likehood

    def recalc(self, class_v):
        self.Ni += 1
        self.prob_distr[class_v] += 1


class FeatureVariants:
    feature_values = {}

    def __init__(self, class_names):
        self.class_names = class_names

    def recalc(self, feature_value, class_v):
        if feature_value in self.feature_values.keys():
            self.feature_values[feature_value].recalc(class_v)
        else:
            self.feature_values.update((feature_value, Feature(self.class_names)))

    def precision(self, feature_value, class_v):
        if feature_value in self.feature_values.keys():
            self.feature_values[feature_value].probability(class_v)


# Сформировать статистики из текстов
class BayesanClassifier():
    N = 0
    features = []
    alphas = []

    # window {words, c_word, words}
    def __init__(self, class_names, class_apriors, window, analyzer):
        self.analyzer = analyzer
        self.window = window
        self.class_names = class_names
        self.alphas = class_apriors

    def fit(self, features_values_tuples, class_v):
        self.N += 1
        for i in range(self.window):
            for feature_value in features_values_tuples[i]:
                self.features[i].recalc(feature_value, class_v[i])

    def precision(self, feature_tuple):
        all_prob = []
        for i in range(self.class_names):
            class_prob = 1
            for feature_value in feature_tuple:
                class_prob *= feature_value.precision(feature_value, self.class_names[i])
            all_prob.append((self.class_names[i], class_prob))

        return sorted(all_prob, key=lambda a: a[1])
