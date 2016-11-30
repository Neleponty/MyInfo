# -*- coding: utf-8 -*-
import unittest
import requests
from ispras import twitter
from ispras import texterra

import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Texterra Tests

class CustomTexterraAPITest(unittest.TestCase):
  def setUp(self):
    TEXTERRA_CUSTOM_HOST = os.getenv("TEXTERRA_CUSTOM_HOST")
    TEXTERRA_CUSTOM_KEY = os.getenv("TEXTERRA_CUSTOM_KEY")
    self.custom_texterra = texterra.API(host=TEXTERRA_CUSTOM_HOST, key=TEXTERRA_CUSTOM_KEY)

  def test_custom_getAttributes(self):
    self.assertIsInstance(self.custom_texterra.getAttributes(12, 'enwiki'), dict)

class TexterraAPITest(unittest.TestCase):
  def setUp(self):
    TEXTERRA_KEY = os.environ.get("TEXTERRA_KEY")
    TEXTERRA_SERVICE_NAME = os.environ.get("TEXTERRA_SERVICE_NAME")
    TEXTERRA_SERVICE_VERSION = os.environ.get("TEXTERRA_SERVICE_VERSION")
    self.texterra = texterra.API(TEXTERRA_KEY, TEXTERRA_SERVICE_NAME, TEXTERRA_SERVICE_VERSION)

    self.en_text = 'Apple today updated iMac to bring numerous high-performance enhancements to the leading all-in-one desktop. iMac now features fourth-generation Intel Core processors, new graphics, and next-generation Wi-Fi. In addition, it now supports PCIe-based flash storage, making its Fusion Drive and all-flash storage options up to 50 percent faster than the previous generation'
    self.ru_text = 'Первые в этом году переговоры министра иностранных дел России Сергея Лаврова и госсекретаря США Джона Керри, длившиеся 1,5 часа, завершились в Мюнхене.'
    self.en_tweet = 'mentioning veterens care which Mccain has voted AGAINST - SUPER GOOOOD point Obama+1 #tweetdebate'
    self.ru_tweet = 'В мастерской готовят пушку и автомобили 1940-х годов, для участия в Параде Победы в Ново-Переделкино.'

  def test_key_concepts(self):
    self.assertIsInstance(self.texterra.keyConcepts(self.en_text), list)
    self.assertIsInstance(self.texterra.keyConcepts(self.ru_text), list)
    self.assertIsInstance(self.texterra.keyConcepts(self.en_tweet), list)
    self.assertIsInstance(self.texterra.keyConcepts(self.ru_tweet), list)

  def test_disambiguation(self):
    self.assertIsInstance(self.texterra.disambiguation(self.en_text), list)
    self.assertIsInstance(self.texterra.disambiguation(self.ru_text), list)

  def test_sentimentAnalysis(self):
    import sys
    self.assertIsInstance(self.texterra.sentimentAnalysis(self.en_text), str if sys.version_info[0] == 3 else basestring)
    self.assertIsInstance(self.texterra.sentimentAnalysis(self.ru_text), str if sys.version_info[0] == 3 else basestring)
    self.assertIsInstance(self.texterra.sentimentAnalysis(self.en_tweet), str if sys.version_info[0] == 3 else basestring)
    self.assertIsInstance(self.texterra.sentimentAnalysis(self.ru_tweet), str if sys.version_info[0] == 3 else basestring)

  def test_domainSentimentAnalysis(self):
    self.assertIsInstance(self.texterra.domainSentimentAnalysis(self.en_text), dict)
    self.assertIsInstance(self.texterra.domainSentimentAnalysis(self.ru_text), dict)
    res = self.texterra.domainSentimentAnalysis(self.en_tweet, 'politics')
    self.assertIsInstance(res, dict)
    self.assertEqual('politics', res['domain'])
    with self.assertRaises(requests.exceptions.HTTPError):
      self.texterra.domainSentimentAnalysis(self.ru_text, 'politics')

  def test_tweetNormalization(self):
    self.assertIsInstance(self.texterra.tweetNormalization(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.tweetNormalization(self.ru_tweet), dict)

  def test_syntaxDetection(self):
    self.assertIsInstance(self.texterra.syntaxDetection(self.ru_text), dict)

  def test_languageDetectionAnnotate(self):
    self.assertIsInstance(self.texterra.languageDetectionAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.languageDetectionAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.languageDetectionAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.languageDetectionAnnotate(self.ru_tweet), dict)

  def test_sentenceDetectionAnnotate(self):
    self.assertIsInstance(self.texterra.sentenceDetectionAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.sentenceDetectionAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.sentenceDetectionAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.sentenceDetectionAnnotate(self.ru_tweet), dict)

  def test_tokenizationAnnotate(self):
    self.assertIsInstance(self.texterra.tokenizationAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.tokenizationAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.tokenizationAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.tokenizationAnnotate(self.ru_tweet), dict)

  def test_lemmatizationAnnotate(self):
    self.assertIsInstance(self.texterra.lemmatizationAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.lemmatizationAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.lemmatizationAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.lemmatizationAnnotate(self.ru_tweet), dict)

  def test_posTaggingAnnotate(self):
    self.assertIsInstance(self.texterra.posTaggingAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.posTaggingAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.posTaggingAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.posTaggingAnnotate(self.ru_tweet), dict)

  def test_namedEntitiesAnnotate(self):
    self.assertIsInstance(self.texterra.namedEntitiesAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.namedEntitiesAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.namedEntitiesAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.namedEntitiesAnnotate(self.ru_tweet), dict)

  def test_subjectivityDetectionAnnotate(self):
    self.assertIsInstance(self.texterra.subjectivityDetectionAnnotate(self.en_text), dict)
    self.assertIsInstance(self.texterra.subjectivityDetectionAnnotate(self.ru_text), dict)
    self.assertIsInstance(self.texterra.subjectivityDetectionAnnotate(self.en_tweet), dict)
    self.assertIsInstance(self.texterra.subjectivityDetectionAnnotate(self.ru_tweet), dict)

  def test_representationTerms(self):
    termCandidates = [
      { 'start': 0, 'end': 5 },
      { 'start': 6, 'end': 11 }
    ]
    featureType = ['commonness', 'info-measure']
    res = self.texterra.representationTerms(self.en_text, termCandidates, featureType)
    self.assertIsInstance(res, dict)
    self.assertEqual(res['text'], self.en_text)
    self.assertIsInstance(res['annotations'], dict)
    self.assertIsInstance(res['annotations']['commonness'], list)
    self.assertIsInstance(res['annotations']['info-measure'], list)

  def test_neignbours(self):
    self.assertIsInstance(self.texterra.neighbours(12, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.neighbours(12, 'enwiki', linkType='RELATED', nodeType='REGULAR', minDepth=1, maxDepth=3), dict)
    self.assertIsInstance(self.texterra.neighbours([12, 713], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.neighbours([12, 713], 'enwiki', linkType='RELATED', nodeType='REGULAR', minDepth=1, maxDepth=3), dict)

  def test_neighboursSize(self):
    self.assertIsInstance(self.texterra.neighboursSize(12, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.neighboursSize(12, 'enwiki', linkType='RELATED', nodeType='REGULAR', minDepth=1, maxDepth=3), dict)
    self.assertIsInstance(self.texterra.neighboursSize([12, 713], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.neighboursSize([12, 713], 'enwiki', linkType='RELATED', nodeType='REGULAR', minDepth=1, maxDepth=3), dict)

  def test_similarityGraph(self):
    self.assertIsInstance(self.texterra.similarityGraph([13137], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarityGraph(13137, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarityGraph([12, 13137, 156327], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarityGraph([12, 13137, 156327], 'enwiki', 'MIN'), dict)

  def test_allPairsSimilarity(self):
    self.assertIsInstance(self.texterra.allPairsSimilarity([12, 13137], [156327, 15942292, 1921431], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.allPairsSimilarity([12, 13137], [156327, 15942292, 1921431], 'enwiki', 'MIN'), dict)

  def test_similarityToVirtualArticle(self):
    self.assertIsInstance(self.texterra.similarityToVirtualArticle([12, 13137], [156327, 15942292, 1921431], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarityToVirtualArticle([12, 13137], [156327, 15942292, 1921431], 'enwiki', 'MIN'), dict)

  def test_similarityBetweenVirtualArticles(self):
    self.assertIsInstance(self.texterra.similarityBetweenVirtualArticles([12, 13137], [156327, 15942292, 1921431], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarityBetweenVirtualArticles([12, 13137], [156327, 15942292, 1921431], 'enwiki', 'MIN'), dict)

  def test_similarOverFirstNeighbours(self):
    self.assertIsInstance(self.texterra.similarOverFirstNeighbours(12, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarOverFirstNeighbours(12, 'enwiki', linkWeight='MIN', offset=1, limit=3), dict)

  def test_similarOverFilteredNeighbours(self):
    self.assertIsInstance(self.texterra.similarOverFilteredNeighbours(12, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.similarOverFilteredNeighbours(12, 'enwiki', linkWeight='MIN', offset=1, limit=3, among='PORTION(0.2)'), dict)

  def test_getAttributes(self):
    self.assertIsInstance(self.texterra.getAttributes(12, 'enwiki'), dict)
    self.assertIsInstance(self.texterra.getAttributes([12, 13137], 'enwiki'), dict)
    self.assertIsInstance(self.texterra.getAttributes(12, 'enwiki', ['url(en)', 'type']), dict)
    self.assertIsInstance(self.texterra.getAttributes([12, 13137], 'enwiki', ['url(en)', 'title']), dict)

# Twitter NLP Tests

class TwitterAPITest(unittest.TestCase):
  def setUp(self):
    DDE_KEY = os.environ.get("DDE_KEY")
    DDE_SERVICE_NAME = os.environ.get("DDE_SERVICE_NAME")
    DDE_SERVICE_VERSION = os.environ.get("DDE_SERVICE_VERSION")
    self.twitter = twitter.API(DDE_KEY, DDE_SERVICE_NAME, DDE_SERVICE_VERSION)

  def test_extract_dde(self):
    self.assertIsInstance(self.twitter.extractDDE('en', 'Ann', 'bob', 'I am Ann from NY', 'Hi there, I am Ann fromNY'), dict)
