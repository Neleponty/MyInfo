import math
from Backend import MinidomParser,Word,TextItem
import pymorphy2
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import numpy
import scipy
import Serializers
from WikiRelations import *
from Usefull import twogrammAnalys

PATH_TO_MORPHY = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\example3.txt'
PATH_TO_OTHER = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\example1.txt'
PATH_TO_STOP_WORDS = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt'


class Word_iter_count:
    doc_id = 0
    count = 0

    def __init__(self, doc_id):
        self.doc_id = doc_id

    def increment(self):
        self.count += 1


def prepareStopwords():
    stopwords = Serializers.readFrom(PATH_TO_STOP_WORDS)[0:-1]
    stopwords_result = []
    for word in stopwords:
        stopwords_result.append(word[:-1])

    return stopwords_result


def loadKeywords():
    keys = open("I:\\keywords.txt", 'r', encoding='utf-8').readlines()
    dict = {}

    for key in keys:
        dict.update([(key, 0),])

    return dict

class SimpleDataProcessor:

    dict_POS = {
        'NOUN': 1,
        'ADJF': 2,
        'ADJS': 3,
        'COMP': 4,
        'VERB': 5,
        'INFN': 6,
        'PRTF': 7,
        'PRTS': 8,
        'GRND': 9,
        'NUMR': 10,
        'ADVB': 11,
        'NPRO': 12,
        'PRED': 13,
        'PREP': 14,
        'CONJ': 15,
        'PRCL': 16,
        'INTJ': 17
    }

    dict_case = {
        'nomn': 1,
        'gent': 2,
        'datv': 3,
        'accs': 4,
        'ablt': 5,
        'loct': 6,
        'voct': 7,
        'gen2': 8,
        'acc2': 9,
        'loc2': 10
    }

    TF_IDF_THRESHOLD = 0.2
    stopwords = []
    word_column_num = {}
    analyzer = []
    parser = None
    keywords = {}

    # ToDo Рутез и википедия
    def __init__(self, stopwords, keywords):
        self.stopwords = stopwords
        self.keywords = keywords
        self.analyzer = pymorphy2.MorphAnalyzer()
        self.parser = MinidomParser(stemmer=self.analyzer, stopwords=self.stopwords)

    def fit(self, documents, Y, posterior):
        # отбор по регрессии
        twogramms = self.twogramm_relevant(documents)
        ngramms = self.ngramm_relevant(documents, 4)
        return twogramms

    #todo то же самое в байесовском алгоритме
    def vectorize(self, ngramm):
        None

    def ngramm_relevant(self, documents):
        counter = CountVectorizer(stop_words=self.stopwords, ngram_range=(1, 3))
        counter.fit_transform(documents)
        ngramms = twogrammAnalys(counter, documents)
        # smth heruistic
        return self.ngrammHeruisticalFilter(ngramms.keys())

    def simpleRelevant(self, text, control_result):

        counter = CountVectorizer(stop_words=self.stopwords, ngram_range=(1, 3))
        counter.fit_transform(text)
        return self.ngrammHeruisticalFilter(counter.vocabulary_.keys())

    def simplePredict(self, text):
        print('vectorize')
        counter = CountVectorizer(stop_words=self.stopwords, ngram_range=(1, 3))
        counter.fit_transform(text)
        print('end')
        return self.ngrammHeruisticalFilter(counter.vocabulary_.keys())


    def predict(self, text):
        return self.algorithm.predict(text)

    def checkStatistics(self, keywords, control_key_words):
        TP = 0
        FP = 0
        len_base = len(control_key_words)

        for thermin in keywords:
            if thermin in control_key_words:
                TP += 1
            else:
                FP += 1

        FN = len_base - TP
        TN = len_base - FN
        Precision = TP / (TP + FP + 1)
        Recall = TP / (TP + FN + 1)
        FMeasure = 2 * (Precision * Recall) / (Precision + Recall + 1)

        return {'Precision': Precision, 'Recall': Recall, 'Fmeasure': FMeasure}

    def getWordTfIdfFrequency (self, normalized_douments):
        tf = TfidfVectorizer()
        result = tf.fit_transform(normalized_douments)
        return tf,result


    #def ngrammStatistics(self):

    def distance(self,vector1,vector2):
        AB = numpy.sum(vector1 + vector2)
        Norm_AB = numpy.sum(numpy.linalg.matrix_power(vector1, 2)) + numpy.sum(numpy.linalg.matrix_power(vector2, 2))
        return AB/Norm_AB

    #Terms From analyzer
    def rangDistance(self, checked_term, control_term):
        getNormalized = lambda words: [item for item in words]
        ct_words = getNormalized(control_term.full_info_words)
        ch_words = getNormalized(checked_term.full_info_words)
        result_range = 0

        temp = 0
        morphs = [word.part_of() for word in ct_words]
        for word in [word.part_of() for word in ch_words]:
            if word in morphs:
               temp += 1

        if temp == 3:
            result_range += 1

        for word in ch_words:
            if word.word in [word.word for word in ct_words]:
                result_range += 1

        return math.log(result_range)

    def getUselessWords(self, text_items , all_words):
        transformer = TfidfVectorizer()
        tfidf = transformer.fit_transform([' '.join(item.words) for item in text_items])
        r,v = tfidf.shape
        result = []
        for i in range(r):
            for j in range(len(all_words)):
                result.append((all_words[j],tfidf[i,j]))
        sort = sorted(result,key = lambda own: own[1] )
        return sort[-1000:-1]

    # todo: Учитывать "Союза Писателей" -> "Союз писателей"
    preferenced_morph_vectors = \
        [('NOUN',),
         ('ADJF','NOUN'),
         ('NOUN','ADJF'),
         ('PRTF','NOUN'),
         ('NOUN','PRTF'),
         ('NOUN', 'NOUN'),
         ('NOUN', 'NOUN', 'NOUN'),
         ('ADJF', 'ADJF', 'NOUN'),
         ('ADJF', 'NOUN', 'ADJF'),
         ('NOUN', 'ADJF', 'ADJF'),
         ('ADJF', 'NOUN', 'NOUN'),
         ('NOUN', 'ADJF', 'NOUN'),
         ('NOUN', 'NOUN', 'ADJF'),
         ]

    def ngrammHeruisticalFilter(self, ngramms):
        result_ngramms = []

        for ngramm in ngramms:
            therm_vector = []
            morph_vector = []
            for word in ngramm.split():
                therm_vector.append(word)
                morph_vector.append(self.analyzer.parse(word)[0].tag.POS)

            # Если в составе имя или геох
            if self.morphVectorVectorizer(morph_vector,therm_vector ,self.preferenced_morph_vectors)[0]:
                result_ngramms.append(therm_vector)

        return result_ngramms

    #todo Все или ничего
    def morphVectorVectorizer(self, morph_vector, word_vector, preferenced_vectors):
        value = 0
    # Нормальный fulltext search needed
#        for word in word_vector:
 #           for keyword in self.keywords:
  #              if word in keyword or self.analyzer.parse(word)[0].normal_form in keyword:
   #                 value += 1

        value /= len(word_vector)
        t = ()
        for word in morph_vector:
            t += (word,)

        if t in preferenced_vectors:
            return True, value
        return False, value

    def main(self):
        text_items = self.parser.getWordsItems(40)
        all_words = self.wordToCleanDictionary(text_items)  # Обработка text and features

    #   r,v = t.shape
    #   res = []
    #   for i in range(v):
    #       res.append(max([(item.toarray(), show[i]) for item in t[:, i]], key=lambda a: a[0]))
    #   print(res)

    def wordToCleanDictionary(self, text_items):
        all_words = []
        for item in text_items:
            for word in item.words:
                n_word = self.analyzer.parse(word)[0].normal_form
                all_words.append(n_word)

        all_words = list(set(all_words))
        return all_words

