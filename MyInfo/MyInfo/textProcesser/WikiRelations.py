import multiprocessing
import os
import pymorphy2
import datetime
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import random
import re
import numpy
import scipy
import pymystem3
import json
import networkx as nx
import math


support = open("I:\keywords.txt", 'r', encoding='utf-8')
support_strings = []

for line in support:
    support_strings.append(line)


def createWikiTree(wikies):
    G = nx.Graph()
    for wiki in wikies:
        if wiki.getHeader() in support_strings:
            G.add_node(wiki.getHeader())


############################################### FEATURE EXTRACTURE #########################################################
def splitCareful(text):
    return re.findall(r'(?u)\b\w\w+\b', text)


def extractNgramms(n, words):
    if n == 0: return []
    result = []
    start = 0

    while start + n <= len(words):
        result.append((words[start: start + n], (start, start + n - 1)))
        if start + n > len(words):
            start = len(words)

        start += 1


    return result
def attachContext(s_words, word_position, window):
    right_bound = window + word_position[1] + 1
    left_bound = word_position[0] - window
    l_error = 0
    r_error = 0

    if right_bound > len(s_words):
        r_error = int(math.fabs(right_bound - len(s_words)))
    if left_bound < 0:
        l_error = int(math.fabs(left_bound))
        left_bound = 0

    ## выравнивание
    result = []
    for shift in range(l_error):
        result.append(None)
    result += s_words[left_bound:word_position[0]] + s_words[word_position[1] + 1: right_bound]
    for shift in range(r_error):
        result.append(None)
    return result


class Wiki:
    dict = {}
    # строгие
    key_terms = []
    # like text
    keywords = {}
    words = []
    regexp = '\[\[[\w, ,\.,-,\,|,]+]]'

    def __init__(self, dict):
        self.dict = dict
        self.key_terms = self.extract()
        self.keywords = self.getKeyWords()
        self.words = splitCareful(self.getContent())

    # [[термин|употребление]]
    def extract(self):
        content = self.getContent()
        reg = self.getMatches(content)
        return [word[1].split('|')[0] for word in reg]

    def getMatches(self, text):
        # matches = re.findall('\[\[[\w, ,\.,-,\,|,]+]]', text)
        # if len(matches) > 0:
        return [(term, term[2:-2]) for term in re.findall(self.regexp, text)]
        # else :
        #    return []

    def getHeader(self):
        return self.dict['Header']

    def getContent(self):
        return self.dict['Content']

    def getKeyWords(self):
        content = self.getContent()
        matches = self.getMatches(content)

        key_words = {}
        for word in matches:
            ex = word[1].split('|')
            # ex[1] - в правильной форме в предложении
            if len(ex) > 1:
                if len(splitCareful(ex[1])) > 0:
                    key_words.update([(' '.join(splitCareful(ex[1])), 0), ])
                else:
                    key_words.update([(ex[1], 0), ])
            else:
                sk = splitCareful(ex[0])
                if len(sk) > 0:
                    key_words.update([(' '.join(sk), 0), ])
                else:
                    key_words.update([(ex[0], 0), ])
        return key_words


    def getLinks(self):
        if 'Links' in self.dict.keys():
            return self.dict['Links']

    def getCategories(self):
        if 'Links' in self.dict.keys():
            return self.dict['Categories']


class GetWikiRelation:
    PATH_TO_STOP_WORDS = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt'
    relevant_themes = []
    stopwords = []
    analyzer = pymorphy2.MorphAnalyzer()

    def __init__(self):
        self.relevant_themes = open("I:\\keywords.txt", 'r', encoding='utf-8').readlines()
        self.stopwords = self.readFrom(self.PATH_TO_STOP_WORDS)

    def readFrom(self, path):
        file = open(path, 'r', -1, 'utf-8')
        return file.readlines()

    def docReader(self, i):
        wikies = []
        directory = "I:\\Folder\\"

        dirs = os.listdir(directory)
        for i in range(i):
            j = random.randint(0, len(dirs) - 1)
            dir = dirs[j]
            dirs.pop(j)

            with open(directory + dir, encoding='utf-8') as f:
                try:
                    content = json.loads(f.read())
                    wikies.append(Wiki(content))
                except:
                    None

        return wikies

    # слова в нормальной форме, важны вхождения
    # не так важно, как вхождения терминов
    def GetKeyWordsToEachDoc(self, documents):
        tfidfTransformer = TfidfVectorizer(stop_words=self.stopwords, use_idf=False)
        tfidfMatrix = scipy.sparse.csc_matrix(tfidfTransformer.fit_transform(documents))
        r, v = tfidfMatrix.shape
        docs_vector = []

        words = [key for key, value in tfidfTransformer.vocabulary_.items()]
        for i in range(r):
            pairs = []
            for j in range(v):
                pairs.append((tfidfMatrix[i, j], words[j]))
            bests = sorted(pairs, key=lambda item: item[0])

            if v < 100:
                bests = bests[-int(v / 2):-1]
            else:
                bests = bests[-100:-1]
            wordnet = []
            for word in bests:
                tag = self.analyzer.parse(word[1])[0].tag
                if tag.POS == 'NOUN':
                    wordnet.append((word[0], word[1]))
            docs_vector.append(wordnet)
        return docs_vector


# feature = [gramm ____ true/false]


class DataPreparator:
    analyzer = None
    #processPool = multiprocessing.Pool()
    #manager = multiprocessing.Manager()
    #parsed_words = manager.dict()
    #self_d = manager

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
    all_saved_words = {}
    inc = 1

    def __init__(self, analyzer):
        self.analyzer = analyzer


    # all_ngramm = <(list_ngramm,anytoken), allNgramms>
    def vectorizePredict(self, pos_start, pos_end, alltext, window):
        all_words = splitCareful(alltext)
        ngramm = [([(0, (pos_start, pos_end), 0), ], all_words), ]
        X, Y = self.vectorizeContext(ngramm, window)
        return X

    # Подход - тренировать каждую n_count по отдельности
    def vectorizeWords(self, all_ngramms, n_g):
        X = []
        Y = []
        for ngramm_pos_set, s_words in all_ngramms:
            for ngramm, position, isKey in ngramm_pos_set:
                T = []
                for word in ngramm:
                    T += self.vectorizeSingleWord(word)
                X += T
                if isKey:
                    Y.append(1)
                else:
                    Y.append(0)

        X = numpy.reshape(numpy.array(X), (-1, n_g * 4))

        return X,Y

    def vectorizeTerm(self, ngramm):
        t =[]
        for gramm in ngramm:
            t.append(self.vectorizeSingleWord(gramm))

        return t

    # one n_g every time
    def vectorizeSingleWord(self, word):
        Geox = 0
        Name = 0
        parsed = self.analyzer.parse(word)[0].tag

        # all features!
        if 'Geox' in parsed:
            Geox = 1

        if 'Name' in parsed:
            Name = 1

        if parsed.POS is not None:
            POS = self.dict_POS[parsed.POS]
        else:
            POS = 100

        if parsed.case is not None:
            case = self.dict_case[parsed.case]
        else:
            case = 100

        return [Geox, Name, POS, case]
    #def all_ngramms(self,ngramm,i):
    #    yield ngramm[i]
    #    i+=1

    # Возвращает контекст длины указанного окна, all_ngramm = [<(ngramm, isTrue), allwords>,]
    def vectorizeContext(self, all_ngramm, window):
        result = []
        print('ContextExtracting... ')
        # Заполнить для производительности
        #self.processPool.map(func = self.forEachNgramm,iterable = [(word, self) for word in all_ngramm])
        for ngramm in all_ngramm:
            words = ngramm[1]
            for word in words:
                alreadyExistWord = self.all_saved_words.get(word)
                if alreadyExistWord is None:
                    # сохранение абсолютно всех слов
                    self.inc += 1
                    self.all_saved_words.update([(word, (self.analyzer.parse(word)[0].tag,self.inc)), ])

        for i in range(len(all_ngramm)):
            words = all_ngramm[i][0]
            wiki_all_words = all_ngramm[i][1]
            print(i)

            # todo слова попадают в нормальной форме и из РуТез, перед этим берется морфологический анализ
            for word, position, isKey in words:

                context = attachContext(wiki_all_words, position, window)
                vector_tag = []
                for item in context:
                    if item is not None:
                        vector_tag.append(self.all_saved_words[item])
                    else:
                        vector_tag.append(None)
                result.append((context, vector_tag, isKey))

        print('Vectorizing..')
        return self.VectorsToCount(result, window)

    # Только контекст, само слово - другой параметр
    def VectorsToCount(self, vectors, window):
        Y = []
        X = []
        for vector in vectors:
            tags = vector[1]
            key = vector[2]
            print('oneVector')

            for i in range(len(tags)):
                # (tag,word_id)
                tag = tags[i]
                if tag is not None:
                    pos = tag[0].POS
                    case = tag[0].case
                    if pos is not None and case is not None:
                        word_id = tag[1]
                        pos_value = self.dict_POS[pos]
                        case_value = self.dict_case[case]
                    else:
                        word_id = 100
                        pos_value = 100
                        case_value = 100

                    X.append(word_id)
                    X.append(pos_value)
                    X.append(case_value)
                else:
                    X.append(0)
                    X.append(0)
                    X.append(0)

            if key:
                Y.append(1)
            else:
                Y.append(0)


        X = numpy.reshape(numpy.array(X), (-1, 2 * window * 3))
        return X, Y
        # Возвращает все features и все ngramms
        # Каждая feature считается за отдельный терм и объединяется в строку

    def prepareTextFeatures(self, n_g, text, keyTherms_dict):
        s_words = splitCareful(text)
        return self.prepareWordsFeatures(n_g, s_words, keyTherms_dict)

    # Собирает N - граммы всех размеров, N-gramm - объект
    # У разных n-gramm - разные контексты , каждой n_gramm - свой NB
    # Результат всех n_gramm классификаторов NB и KeyWords NB вычисляется по линейной функции
    def prepareWordsFeatures(self, n_g, all_words, keyTherms_dict):
        print('Preparing...')
        words = []
        s_words = all_words
        positional_array = extractNgramms(n_g, s_words)
        print('extracted')

        for ngramm in positional_array:
            joined = ' '.join(ngramm[0])
            match = keyTherms_dict.get(joined)

            if match is not None:
                words.append((ngramm[0], ngramm[1], True))
            else:
                words.append((ngramm[0], ngramm[1], False))
        print('checked')
        return words, s_words

    # todo отбор признаков
    def Generate(self, ngramm = 2, count = 10, window = 2):
        wikies = GetWikiRelation().docReader(count)
        all_ngramm_wikies = [self.prepareWordsFeatures(ngramm, wiki.words, wiki.keywords) for wiki in wikies]
        return self.vectorizeContext(all_ngramm_wikies, window)

    # Собираем X,Y ,а X-w Yw в отдельный
    #=====================================================================All=========================================
    def GenerateWordsToDoc(self, doc_words, ngramm=2, window=2):
        all_ngramm_wikies = self.prepareWordsFeatures(ngramm, doc_words, {})
        X, Y = self.vectorizeContext(all_ngramm_wikies, window)
        X_w, Y_w = self.vectorizeWords(all_ngramm_wikies, ngramm)
        return X, X_w

    def GenerateWordsTrain(self, ngramm = 2, count = 10, window = 2):
        wikies = GetWikiRelation().docReader(count)
        all_ngramm_wikies = [self.prepareWordsFeatures(ngramm, wiki.words, wiki.keywords) for wiki in wikies]
        X, Y = self.vectorizeContext(all_ngramm_wikies, window)
        X_w, Y_w = self.vectorizeWords(all_ngramm_wikies, ngramm)
        return X,Y, X_w, Y_w
    #=================================================================================================================

    def Split_Vectorize(self, texts, keywordsEach, n_gramm, window):
        allPreparedVectors = []
        for i in range(len(texts)):
            allPreparedVectors.append(self.prepareTextFeatures(n_gramm, texts[i], keywordsEach[i]))

        X,Y =  self.vectorizeContext(allPreparedVectors, window)
        X_w,Y_w = self.vectorizeWords(allPreparedVectors, n_gramm)
        return X,Y,X_w,Y_w