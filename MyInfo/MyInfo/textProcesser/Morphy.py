import math
from Backend import MinidomParser,Word,TextItem
import pymorphy2
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import numpy
import scipy
import Serializers

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



class SimpleDataProcessor:
    TF_IDF_THRESHOLD = 0.2
    stopwords = []
    word_column_num = {}
    # analyzer_stem = pymystem3.Mystem()
    analyzer = []
    parser = None

    def __init__(self):
        self.stopwords = prepareStopwords()
        self.analyzer = pymorphy2.MorphAnalyzer()
        self.parser = MinidomParser(stemmer=self.analyzer, stopwords=self.stopwords)

    def countFrequencyMatrix(self, text_items):
        A = numpy.zeros((len(text_items), len(self.word_column_num)))
        i = 0
        for item in text_items:  # Подсчет frequency
            for k, v in item.distribution.items():
                n_j = self.word_column_num[k.encode('utf-8').decode('utf-8')]
                A[i, n_j] = v
            i += 1
        return A

    def getWordTfIdfFrequency(self, text_items, all_words, idf=True):

        column_count = 0
        for word in all_words:
            self.word_column_num.update([(word, column_count), ])
            column_count += 1

        A = self.countFrequencyMatrix(text_items)
        scipy.sparse.csc_matrix(A)  # обработка разреженности
        result = scipy.sparse.csc_matrix(TfidfTransformer(use_idf=idf).fit_transform(A))
        return A, result  # log ( n / df(d, t) ) + 1


    # может оценивать вероятность того, что (key|w1,w2,w3)
    #
    def equalAnalyse(self, ngramm, ngramm2):
        for i in ngramm:
            if i not in ngramm2:
                return False
        return True

    def equal(self, ngramm, ngramm2):

        for i in ngramm:
            if i not in ngramm2:
                return False
        return True



    def isNamed(self, text_item):
        return 'NOUN' in text_item.morphology()

    def isNamedEntity(self, term):
        return False

    def checkInFile(self, file, termin):
        result = 0

        with file:
            for line in file:
                # Аккумулируем совпадения
                result =+ self.rangDistance(termin,line)
        return result/len(termin.split())


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

    # расстояние левенштейна - > the same as normal_form
    # def levenstainDistance(self,term,term2):
    # если {W} - попарно независимы,то p(w|wi) = p(w)*p(wi)
    # если {W} - совместно независимы,то p(w|W) = p(w1)*p(w2)....p(wn)
    def twogrammAnalys(self, ngramm_counter, text_items):
        counted = CountVectorizer()
        garbage = counted.fit_transform([' '.join(item.words) for item in text_items])
        diction = ngramm_counter.vocabulary_
        words_twoplix = diction.keys()
        probability = {}

        # Частотный метод
        for wordset in words_twoplix:

            count_of_set = diction[wordset]
            words_prob = []
            posterior_distrib = count_of_set/sum(diction.values())
            # p(w)
            for word in wordset.split():
                # Есть совпадение
                word_count = counted.vocabulary_.get(word)
                word_probability = word_count/(numpy.sum(garbage))
                words_prob.append(word_probability)
            apriorDistrib = 0

            for item in words_prob:
                apriorDistrib *= item
            #
            #Student's t-statistic
        #    t_stat_dividor = math.sqrt(1/len(words_twoplix))
            t_stat = math.fabs(apriorDistrib - posterior_distrib)
            probability.update([(wordset,t_stat),])
        # Word_probability

        return probability


    def ngrammHeruisticalFilter(self, ngramm_counter, ngramm_count):
        #todo: Учитывать "Союза Писателей" -> "Союз писателей"
        preferenced_morph_vectors = \
            [[('ADJF','nomn'), ('NOUN','nomn')],
             [('PRTF','nomn'), ('NOUN','nomn')],
             [('NOUN','nomn'), ('NOUN','gent')],# gent падеж
             [('NOUN','nomn'), ('NOUN','ablt')]]# ablt падеж

        diction = ngramm_counter.vocabulary_
        ngramms = diction.keys()
        result_ngramms = []
        for ngramm in ngramms:
            therm_vector = []
            for word in ngramm.split():
                therm_vector.append(word)

            if self.morphVectorValidate(therm_vector, preferenced_morph_vectors, ngramm_count):
                result_ngramms.append(therm_vector)

        return result_ngramms

    #todo Все или ничего
    def morphVectorValidate(self, word_vectors, preferenced_vectors, gramm_count):
        # error = 0
        #

        for i in range(len(word_vectors)):
            morph = self.analyzer.parse(word_vectors[i])
            # проверяем каждую строку preferences
            for pr_vector in preferenced_vectors:
                if morph[0].tag.POS == pr_vector[i][0] or morph[0].tag.case == pr_vector[i][1]:
                    return True
        return False

    def keyWords(self, text_items):
        theMain = []
        # ToDo: Фильтровать через словарь

        for item in text_items:
            for_one = []
            for word in item.words:
                if 'NOUN' in self.analyzer.parse(word)[0].tag:
                    for_one.append(word)
            theMain.append(for_one)

        features = [' '.join(words) for words in theMain]
        helper = CountVectorizer(stop_words=self.stopwords)
        tfidfReslt = scipy.sparse.csc_matrix(helper.fit_transform(features))
        bagWords = []
        for item in helper.vocabulary_:
            bagWords.append(item)

        most_relevant = []
        r, v = tfidfReslt.shape
        for i in range(r):
            result = []
            for j in range(v):
                result.append((bagWords[j], tfidfReslt[i, j]))
            # print(sorted(result, key=lambda one: one[1])[-10:-1])
            most_relevant.append(sorted(result, key=lambda one: one[1])[-10:-1])

        # Todo: поставить в именительный

        return most_relevant

    def main(self):
        text_items = self.parser.getWordsItems(40)
        all_words = self.wordToCleanDictionary(text_items)  # Обработка text and features

        print(self.getUselessWords(text_items, all_words))
        print('###################################STOP#####################################')

        most_relevant_each = self.keyWords(text_items)
        for i in range(len(most_relevant_each)):
            print(most_relevant_each)
            print(text_items[i].checkStatistics(self.analyzer,most_relevant_each[i]))


        counter = CountVectorizer(stop_words=self.stopwords, ngram_range=(2,2))
        ngramms = counter.fit_transform([' '.join(item.words) for item in text_items])

        THRESHOLD = 0.1
        twogramm_relevant1 = self.twogrammAnalys(counter, text_items)
        twogramm_relevant2 = self.ngrammHeruisticalFilter(counter, 2)

        print(sorted(twogramm_relevant1, key = lambda one: one[1])[:-10])

        # todo УЖАСНО НЕОК        print(len(twogramm_relevant2))


        # todo: именную форму и согласование file = open("I:/keywords.txt",'r',encoding='utf-8')


        #  Анализ заголовков
        #  1. Расширить на n-граммы
        #  2. Привести к согласованному описанию


    def wordToCleanDictionary(self, text_items):
        all_words = []
        for item in text_items:
            for word in item.words:
                all_words.append(word)

        all_words = list(set(all_words))
        return all_words


# idea
#    def buildMatrix(self, docs_items_by_id):
#    return [[token in tokenize(doc_item)] for doc_item in docs_items_by_id]


processor = SimpleDataProcessor()
processor.main()
