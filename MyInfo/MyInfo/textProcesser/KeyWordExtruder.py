from Backend import MinidomParser,Word,TextItem
import pymorphy2
import math
import numpy
from ispras import texterra
import matplotlib

from sklearn.naive_bayes import MultinomialNB



t = texterra.API('b1c2d3f2250ac8e43a5e7633d83817b18f6ee84e')
