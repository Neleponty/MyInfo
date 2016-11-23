from xml.dom import minidom
import pymorphy2
import datetime
from django.core import serializers
import Serializers
import json
from sklearn.feature_extraction import text as sk

PATH_TO_MORPHY = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\example3.txt'
PATH_TO_OTHER = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\example1.txt'
PATH_TO_STOP_WORDS = 'C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\stopwords.txt'


class Word:
    itemd = 0




def prepareStopwords():
    stopwords = Serializers.readFrom(PATH_TO_STOP_WORDS)[1:-1]
    stopwords_result = []
    for word in stopwords:
        stopwords_result.append(word[:-1])
    return stopwords_result


class SimpleDataProcessor:
    TF_IDF_THRESHOLD = 0.2
    analyzer = pymorphy2.MorphAnalyzer()
    docs_items_by_id = []
    words_docs_id = []
    stopwords = prepareStopwords()

    def main(self):
        text_items = MinidomParser().getWordsItems()[:2]
        text_items = self.tokenize(text_items)
        vactorizer = sk.CountVectorizer()
        corpus = []
        for item in text_items:
            for word in item.clean_text.encode('utf-8'):
                corpus.append(word)
        print(corpus)

    #    for item in text_items:
     #       Serializers.printInto(','.join(item.clean_text) + "\n", PATH_TO_MORPHY)

   #     text_items = self.stopProcess(text_items)

#        print('wordsStopPreproc')
 #       for item in text_items:
  #          Serializers.printInto(','.join(item.clean_text) + "\n", PATH_TO_MORPHY)

        # Serializators().serializeInto(text_items, PATH_TO_MORPHY)

        # for item in text_items:
        # return self.serializeInto(item)

    def splitAndReturn(self, text):
        values = []
        for text in text.split():
            values.append(self.analyzer.parse(text)[0].normal_form)
        return values

    # ============================= hardware

    # Обработать
    def tokenize(self, text_items):
        result = []
        for item in text_items:
            print('oneMore')
            result.append(item.init_clean(item,
                                          self.splitAndReturn(item.title),
                                          self.splitAndReturn(item.text)))
        return result

    def stopProcess(self, text_items):
        result = []
        for item in text_items:
            result.append(item.init_clean(item,
                                          self.stopProcedure(item.clean_title),
                                          self.stopProcedure(item.clean_text)))
        return result

    def stopProcedure(self, divided_words):
        result_list = []
        for word in divided_words:
            if word not in self.stopwords :
                result_list.append(word)
            else:
                print(word.encode('utf-8'))
        return result_list


# idea
#    def buildMatrix(self, docs_items_by_id):
#    return [[token in tokenize(doc_item)] for doc_item in docs_items_by_id]

class MinidomParser:
    def getWordsItems(self):
        dom = minidom.parse('C:\\Users\\Nikita\\Downloads\\xmlWikiOrderByDate.xml')
        items_array = dom.getElementsByTagName('page')
        list_of_items = []
        for item in items_array:
            parsed_item = self.initTextItem(item)
            if parsed_item is not None:
                list_of_items.append(parsed_item)
        return list_of_items

    def initTextItem(self, item):
        id = item.getElementsByTagName('id')[0].firstChild
        title = item.getElementsByTagName('title')[0].firstChild
        text = item.getElementsByTagName('text')[0].firstChild
        categories = self.get_all_categories(item)

        if title is not None and text is not None and id is not None:
            id = int(id.nodeValue)
            return TextItem(id, title.nodeValue, text.nodeValue, categories)
        else:
            return None

    def get_all_categories(self, item):
        elements = item.getElementsByTagName('category')
        result = []
        for element in elements:
            result.append(element.firstChild.nodeValue)
        return result


class Serializators:
    def serializeInto(self, text_items, path):
        # json_serializer = serializers.get_serializer('json')
        # json_serializer = json_serializer()
        file = open(path, 'w', -1, 'utf-8')
        for item in text_items: item.serialize(file)
        file.close()


class TextItem():
    id = 0
    title = ''
    text = ''
    control_key_words = ''
    clean_title = []
    clean_text = []
    # Todo привести к нормальному виду
    date = datetime.datetime.now().time

    def __init__(self, _id, title, text, control_key_words):
        self.id = _id
        self.title = title
        self.text = text
        self.control_key_words = control_key_words

    def init_clean(self, item, clean_title, clean_text):
        result = TextItem(
            item.id,
            item.title,
            item.text,
            item.control_key_words)
        result.clean_text = clean_text
        result.clean_title = clean_title
        return result

    def serialize(self, stream):
        result = {}
        result['clean_title'] = self.clean_title
        result['clean_text'] = self.clean_text
        json.dumps(result, stream, ensure_ascii=False)


# class TextitemSerializer(serializers.Serializers):

SimpleDataProcessor().main()
