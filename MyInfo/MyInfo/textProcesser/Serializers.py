from django.core import serializers
serializers.settings.configure()

json_serializer = serializers.get_serializer('json')()


def serializeInto(text_item, path):
    file = open(path, 'ab', -1, 'utf-8')
    json_serializer.serialize(text_item, file)
    file.close()


def printInto(string, path):
    file = open(path, 'ab', -1)
    file.write(string)
    ##def step_reducing(self):


def readFrom(path):
    file = open(path, 'r', -1)
    return file.readlines()
    ##def step_extracting(self):

