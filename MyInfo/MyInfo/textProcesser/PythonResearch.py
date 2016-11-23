from xml.dom import minidom
import pymorphy2
import datetime
from pymystem3 import Mystem


# как-то оптимизировать словарь

# Ядро - Документ, пользователь(отношение пользователь - документ - документ - тема)
# отношение (тема - слово, документ - слово, пользователь - слово) - в коробке
# коробка сама умеет выдавать тему, ключевые слова(поднимает свои словари), но уровень документа - внешний


# LSA - поднимаем 1 раз, при формировании тематик

# 1 - ключевые слова (согласовать с коробкой или взять свои)
# 2 - тематики

class Word:
    itemd = 0


class SimpleDataProcessor:
    TF_IDF_THRESHOLD = 0.2
    analyzer = Mystem()
    docs_items_by_id = []
    words_docs_id = []

    def main(self):
        docs_tems_by_id = MinidomParser().getWordsItems()
        for doc in docs_tems_by_id:
            self.analyzer.lemmatize(doc.text)
            #self.printInto(''.join(self.step_lemmatizing(doc)[1]))
            print('step')
        words_docs_id = self.tokenize(docs_tems_by_id)

    #Обработать
    def tokenize(self, text_items):
        processed_items = []
        for item in text_items:
            doc_words = self.step_lemmatizing(item)
            for word in doc_words:
                if word not in processed_items:
                    processed_items.append(word)
        return processed_items



    def buildMatrix(self, docs_items_by_id):
        return [[token in tokenize(doc_item)] for doc_item in docs_items_by_id]

    #Привести к
    def step_lemmatizing(self, text_item):
        clean_title = self.analyzer.lemmatize(text_item.title)
        self.printInto(''.join(clean_title))
        clean_text = self.analyzer.lemmatize(text_item.text)
        self.printInto(''.join(clean_text))

        return (text_item.id, clean_title, clean_text)


    def printInto(self,string):
        file = open('C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\example.txt', 'a')
        file.write(string)
        ##def step_reducing(self):

    ##def step_extracting(self):

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



class TextItem:
    id = 0
    title = ''
    text = ''
    control_key_words = ''
    # Todo привести к нормальному виду
    date = datetime.datetime.now().time

    def __init__(self, _id, title, text, control_key_words):
        self.id = _id
        self.title = title
        self.text = text
        self.control_key_words = control_key_words

items = SimpleDataProcessor().main()
print(items)
