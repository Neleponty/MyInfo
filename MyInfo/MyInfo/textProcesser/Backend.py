from xml.dom import minidom
import re
import subprocess
import datetime
import json


class MinidomParser:
    stemmer = None
    stopwords = None

    def __init__(self, stemmer, stopwords):
        self.stemmer = stemmer
        self.stopwords = stopwords

    def getWordsItems(self, howMatch, tokenize=True):
        file = open('C:\\Users\\Nikita\\myenv\\MyInfo\\MyInfo\\textProcesser\\xmlWikiOrderByDate.xml', encoding='utf-8')
        dom = minidom.parse(file)
        items_array = dom.getElementsByTagName('page')
        list_of_items = []

        if howMatch > len(items_array):
            howMatch = len(items_array)

        for i in range(howMatch):
            parsed_item = self.textItemTemplate(items_array[i])
            if parsed_item is not None:
                if tokenize:
                    list_of_items.append(self.tokenize(parsed_item[1], parsed_item[1] + parsed_item[2], parsed_item[3]))
                else:
                    list_of_items.append(parsed_item[2])
        return list_of_items

    def tokenize(self,title, string, key_words):
        words = self.splitAndReturn(string, 1)
        return TextItem(title, words, key_words)

    #######################################################333
    def splitAndReturn(self, text, weight):
        values = []
        for text in re.findall(r'(?u)\b\w\w+\b', text):
            analysed = self.stemmer.parse(text)
            values.append(Word(analysed, weight))

        return values

    # ============================= hardware


    def stopProcedure(self, divided_words):
        result_list = []
        for word in divided_words:
            if word not in self.stopwords:
                result_list.append(word)

        return result_list

    def textItemTemplate(self, item):
        id = item.getElementsByTagName('id')[0].firstChild
        title = item.getElementsByTagName('title')[0].firstChild
        text = item.getElementsByTagName('text')[0].firstChild
        categories = self.get_all_categories(item)

        if title is not None and text is not None and id is not None:
            id = int(id.nodeValue)
            return id, title.nodeValue, text.nodeValue, categories
        else:
            return None

    def get_all_categories(self, item):
        for element in item.getElementsByTagName('category'):
            yield element.firstChild.nodeValue



class TextItem:
    control_key_words = []
    count = 0
    words = []
    title = ''
    # Todo привести к нормальному виду
    date = datetime.datetime.now().time
    full_info_words = []

    def __init__(self, title, words, control_key_words):
        self.title = title
        self.words = [word.word for word in words]
        self.full_info_words = [word for word in words]
        self.control_key_words = [word for word in control_key_words]
        self.distribution = self.calcDistrib()

    def calcDistrib(self):
        distrib = {}
        for word in self.words:
            if word in distrib.keys():
                value = distrib.pop(word)
                distrib.update([(word, (value + 1)), ])
            else:
                distrib.update([(word, 1), ])

        return distrib

class Word():
    word = ''
    weight = 0.0
    allInfo = []

    def __init__(self, word, weight):
        self.word = word[0].word
        self.weight = weight
        self.allInfo = word

    def morphology(self):
        return self.allInfo[0].tag

    def part_of(self):
        return self.allInfo[0].tag.POS
