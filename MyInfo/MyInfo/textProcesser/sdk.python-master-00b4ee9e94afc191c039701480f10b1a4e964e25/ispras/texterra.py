# -*- coding: utf-8 -*-
import requests
import json
import os
from . import ispras

class API(ispras.API):
  """This class provides methods to work with Texterra REST via OpenAPI, including NLP and EKB methods and custom queriesю
    Note that NLP methods return annotations only"""

  # Default Texterra path
  texterraName = 'texterra'
  texterraVersion = 'v3.1'

  # Path and parameters for preset NLP queries
  NLPSpecs = {
    'languageDetection': {
        'path': 'nlp/language',
        'params': {
          'class': 'language',
          'filtering': 'KEEPING'
        }
    },
    'sentenceDetection': {
        'path': 'nlp/sentence',
        'params': {
          'class': 'sentence',
          'filtering': 'KEEPING'
        }
    },
    'tokenization': {
        'path': 'nlp/token',
        'params': {
          'class': 'token',
          'filtering': 'KEEPING'
        }
    },
    'lemmatization': {
        'path': 'nlp/lemma',
        'params': {
          'class': 'lemma',
          'filtering': 'KEEPING'
        }
    },
    'posTagging': {
        'path': 'nlp/pos',
        'params': {
          'class': 'pos-token',
          'filtering': 'KEEPING'
        }
    },
    'spellingCorrection': {
        'path': 'nlp/spellingcorrection',
        'params': {
          'class': 'spelling-correction-token',
          'filtering': 'KEEPING'
        }
    },
    'namedEntities': {
        'path': 'nlp/namedentity',
        'params': {
          'class': 'named-entity',
          'filtering': 'KEEPING'
        }
    },
    'termDetection': {
        'path': 'nlp/term',
        'params': {
          'class': 'frame',
          'filtering': 'KEEPING'
        }
    },
    'disambiguation': {
        'path': 'nlp/disambiguation',
        'params': {
          'class': 'disambiguated-phrase',
          'filtering': 'KEEPING'
        }

    },
    'keyConcepts': {
        'path': 'nlp/keyconcepts',
        'params': {
          'class': 'keyconcepts',
          'filtering': 'KEEPING'
        }

    },
    'domainDetection': {
        'path': 'nlp/domain',
        'params': {
          'class': 'domain',
          'filtering': 'KEEPING'
        }

    },
    'subjectivityDetection': {
        'path': 'nlp/subjectivity',
        'params': {
          'class': 'subjectivity',
          'filtering': 'KEEPING'
        }

    },
    'polarityDetection': {
        'path': 'nlp/polarity',
        'params': {
          'class': 'polarity',
          'filtering': 'KEEPING'
        }

    },
    'domainPolarityDetection': {
        'path': 'nlp/domainpolarity{}',
        'params': {
          'class': [
            'domain',
            'polarity'
          ],
          'filtering': 'KEEPING'
        }

    },
    'tweetNormalization': {
        'path': 'nlp/twitterdetection',
        'params':
        {
          'class': [
            'sentence',
            'language',
            'token'
          ],
          'filtering': 'REMOVING'
        }

    },
    'syntaxDetection': {
        'path': 'nlp/syntax',
        'params': {
          'class': 'syntax-relation',
          'filtering': 'KEEPING'
        }
    }
  }

  # Path and parameters for preset KBM queries
  KBMSpecs = {
    'representationTerms': {
      'path': 'representation/terms',
      'params': {}
    },
    'neighbours': {
      'path': 'walker/{0}/neighbours{1}',
      'params': {}
    },
    'similarityGraph': {
      'path': 'similarity/{0}/graph',
      'params': {}
    },
    'allPairsSimilarity': {
      'path': 'similarity/{0}/summed/{1}',
      'params': {}
    },
    'similarityToVirtualArticle': {
      'path': 'similarity/{0}/toVirtualArticle/{1}',
      'params': {}
    },
    'similarityBetweenVirtualArticles': {
      'path': 'similarity/{0}/betweenVirtualArticles/{1}',
      'params': {}
    },
    'similarOverFirstNeighbours': {
      'path': 'similarity/{0}/similar/neighbours',
      'params': {}
    },
    'similarOverFilteredNeighbours': {
      'path': 'similarity/{0}/similar/all',
      'params': {}
    }
  }


  def __init__(self, key=os.getenv('TEXTERRA_CUSTOM_KEY', False), name=None, ver=None, host=os.getenv('TEXTERRA_CUSTOM_HOST', None)):
    """Provide only apikey to use default Texterra service name and version."""
    if host == None:
      if name == None: name = API.texterraName
      if ver == None: ver = API.texterraVersion
      ispras.API.__init__(self, key, name, ver)
    else:
      ispras.API.__init__(self, host=host, key=key)

  # Section of NLP methods
  # NLP basic helper methods
  def keyConcepts(self, text):
    """Key concepts are the concepts providing short (conceptual) and informative text description.
    This service extracts a set of key concepts for a given text.
      Note: this method returns list of weighted key concepts"""
    return self.keyConceptsAnnotate(text)['annotations']['keyconcepts'][0]['value']

  def sentimentAnalysis(self, text):
    """Detects whether the given text has positive, negative or no sentiment."""
    try:
      return self.polarityDetectionAnnotate(text)['annotations']['polarity'][0]['value']
    except:
      return 'NEUTRAL'

  def domainSentimentAnalysis(self, text, domain=''):
    """Detects whether the given text has positive, negative, or no sentiment, with respect to domain.
      If domain isn't provided, Domain detection is applied, this way method tries to achieve best results.
      If no domain is detected general domain algorithm is applied."""
    annotations = self.domainPolarityDetectionAnnotate(text, domain)['annotations']
    try:
      usedDomain = 'general'
      sentiment = 'NEUTRAL'
      usedDomain = annotations['domain'][0]['value']
      sentiment = annotations['polarity'][0]['value']
    except KeyError:
      pass
    return { 'domain' :usedDomain, 'polarity': sentiment }

  def disambiguation(self, text):
    """Detects the most appropriate meanings (concepts) for terms occurred in a given text.
      Note: this method returns Texterra annotations"""
    return self.disambiguationAnnotate(text)['annotations']['disambiguated-phrase']

  # NLP annotating methods
  def languageDetectionAnnotate(self, text):
    """Detects language of given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('languageDetection', text)

  def sentenceDetectionAnnotate(self, text):
    """Detects boundaries of sentences in a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('sentenceDetection', text)

  def tokenizationAnnotate(self, text):
    """Detects all tokens (minimal significant text parts) in a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('tokenization', text)

  def lemmatizationAnnotate(self, text):
    """Detects lemma of each word of a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('lemmatization', text)

  def posTaggingAnnotate(self, text):
    """Detects part of speech tag for each word of a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('posTagging', text)

  def spellingCorrectionAnnotate(self, text):
    """Tries to correct disprints and other spelling errors in a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('spellingCorrection', text)

  def namedEntitiesAnnotate(self, text):
    """Finds all named entities occurences in a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('namedEntities', text)

  def termDetectionAnnotate(self, text):
    """Extracts not overlapping terms within a given text; term is a textual representation for some concept of the real world.
      Note: this method returns Texterra document"""
    return self.__presetNLP('termDetection', text)

  def disambiguationAnnotate(self, text):
    """Detects the most appropriate meanings (concepts) for terms occurred in a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('disambiguation', text)

  def keyConceptsAnnotate(self, text):
    """Key concepts are the concepts providing short (conceptual) and informative text description.
    This service extracts a set of key concepts for a given text.
      Note: this method returns Texterra document"""
    return self.__presetNLP('keyConcepts', text)

  def domainDetectionAnnotate(self, text):
    """Detects the most appropriate domain for the given text.
      Currently only 2 specific domains are supported: 'movie' and 'politics'
      If no domain from this list has been detected, the text is assumed to be no domain, or general domain.
        Note: this method returns Texterra document"""
    return self.__presetNLP('domainDetection', text)

  def subjectivityDetectionAnnotate(self, text):
    """Detects whether the given text is subjective or not.
      Note: this method returns Texterra document"""
    return self.__presetNLP('subjectivityDetection', text)

  def polarityDetectionAnnotate(self, text):
    """Detects whether the given text has positive, negative or no sentiment.
      Note: this method returns Texterra document"""
    return self.__presetNLP('polarityDetection', text)

  def domainPolarityDetectionAnnotate(self, text, domain=''):
    """Detects whether the given text has positive, negative, or no sentiment, with respect to domain.
      If domain isn't provided, Domain detection is applied, this way method tries to achieve best results.
      If no domain is detected general domain algorithm is applied.
        Note: this method returns Texterra document"""
    specs = API.NLPSpecs['domainPolarityDetection']
    if domain != '':
      domain = '({})'.format(domain)

    result = self.POST(specs['path'].format(domain), specs['params'], {'text': text}, 'json')
    annotations = result['annotations']
    import sys
    it = annotations.items() if sys.version_info[0] == 3 else annotations.iteritems()
    for k,v in it:
        for an in v:
          an['text'] = text[an['start']:an['end']]
          an['annotated-text'] = text
    return result

  def tweetNormalization(self, text):
    """Detects Twitter-specific entities: Hashtags, User names, Emoticons, URLs.
      And also: Stop-words, Misspellings, Spelling suggestions, Spelling corrections."""
    return self.__presetNLP('tweetNormalization', text)

  def syntaxDetection(self, text):
    """Detects syntax relations """
    result = self.__presetNLP('syntaxDetection', text)
    for an in result['annotations']['syntax-relation']:
      if 'parent-token' in an['value']:
        start = int(an['value']['parent-token']['start'])
        end = int(an['value']['parent-token']['end'])
        an['value']['parent-token']['text'] = text[start:end]
        an['value']['parent-token']['annotated-text'] = text
    return result

  # Section of KBM methods
  def __wrapConcepts(self, concepts, kbname):
    """Utility wrapper for matrix parameters"""
    if isinstance(concepts, list):
      return ''.join(['id={0}:{1};'.format(concept, kbname) for concept in concepts])
    else:
      return 'id={0}:{1};'.format(concepts, kbname)

  def representationTerms(self, text, termCandidates, featureType=['commonness', 'info-measure']):
    """Determines if Knowledge base contains the specified terms and computes features of the specified types for them."""
    specs = API.KBMSpecs['representationTerms']
    queryParam = specs['params']
    queryParam['featureType'] = featureType
    url = self.url + specs['path']
    if self.apikey: queryParam['apikey'] = self.apikey
    payload = {
      'text': text,
      'annotations': {
        'term-candidate': termCandidates
      }
    }
    page = requests.post(url, params=queryParam, json=payload, timeout=60)
    if page.status_code == 200:
      return page.json()
    else:
      page.raise_for_status()

  def neighbours(self, concepts, kbname, linkType=None, nodeType=None, minDepth=None, maxDepth=None):
    """Return neighbour concepts for the given concepts(list or single concept, each concept is {id}, {kbname} is separate parameter).
      If at least one traverse parameter(check REST Documentation for values) is specified, all other parameters should also be specified """
    concept = self.__wrapConcepts(concepts, kbname)
    traverse = ''
    if linkType:
      traverse += ';linkType=' + linkType
    if nodeType:
      traverse += ';nodeType=' + nodeType
    if minDepth:
      traverse += ';minDepth=' + str(minDepth)
    if maxDepth:
      traverse += ';maxDepth=' + str(maxDepth)
    return self.__presetKBM('neighbours', [concept, traverse])

  def neighboursSize(self, concepts, kbname, linkType=None, nodeType=None, minDepth=None, maxDepth=None):
    """Return neighbour concepts size for the given concepts(list or single concept, each concept is {id}, {kbname} is separate parameter).
      If at least one traverse parameter(check REST Documentation for values) is specified, all other parameters should also be specified """
    concept = self.__wrapConcepts(concepts, kbname)
    traverse = ''
    if linkType:
      traverse += ';linkType=' + linkType
    if nodeType:
      traverse += ';nodeType=' + nodeType
    if minDepth:
      traverse += ';minDepth=' + str(minDepth)
    if maxDepth:
      traverse += ';maxDepth=' + str(maxDepth)
    traverse+='/size'
    return self.__presetKBM('neighbours', [concept, traverse])

  def __transformGraph(self, concepts, simGraph):
    concept2id = dict()
    for concept in simGraph['concept-2-position']['entry']:
      idConcept =int(concept['concept']['id'])
      concept2id[idConcept] = int(concept['integer'])

    fullMatrix = dict()
    for pos1, item in enumerate(simGraph['similarity']['double']):
      if not pos1 in fullMatrix:
        fullMatrix[pos1] = dict()
      for add, val in enumerate(item['#text'].split(", ")):
        pos2 = pos1 + add + 1
        if not pos2 in fullMatrix:
          fullMatrix[pos2] = dict()
        fullMatrix[pos1][pos2] = float(val)
        fullMatrix[pos2][pos1] = fullMatrix[pos1][pos2]

    result = dict()
    for concept1 in concepts:
      result[concept1] = dict()
      for concept2 in concepts:
        id1, id2 = concept2id[concept1], concept2id[concept2]
        result[concept1][concept2] = fullMatrix[id1][id2] if id1 != id2 else 1.0

    return result

  def similarityGraph(self, concepts, kbname, linkWeight='MAX'):
    """Compute similarity for each pair of concepts(list or single concept, each concept is {id}, kbname is separated).
      linkWeight specifies method for computation of link weight in case of multiple link types - check REST Documentation for values"""
    if isinstance(concepts, int):
      return {concepts: 1.0}
    if len(concepts) == 0:
      return {}
    if len(concepts) == 1:
      return {concepts[0]: 1.0}
    param = self.__wrapConcepts(concepts, kbname)
    param += 'linkWeight=' + linkWeight
    return self.__transformGraph(concepts, self.__presetKBM('similarityGraph', param)['full-similarity-graph'])

  def allPairsSimilarity(self, firstConcepts, secondConcepts, kbname, linkWeight='MAX'):
    """Computes sum of similarities from each concepts(list or single concept, each concept is {id}, {kbname} is separate parameter) from the first list to all concepts(list or single concept, each concept is {id}, {kbname} is separate parameter) from the second one.
      linkWeight specifies method for computation of link weight in case of multiple link types - check REST Documentation for values"""
    first = self.__wrapConcepts(firstConcepts, kbname)
    first += 'linkWeight={};'.format(linkWeight)
    second = self.__wrapConcepts(secondConcepts, kbname)
    return self.__presetKBM('allPairsSimilarity', [first, second])

  def similarityToVirtualArticle(self, concepts, virtualAricle, kbname, linkWeight='MAX'):
    """Compute similarity from each concept from the first list to all concepts(list or single concept, each concept is {id}, {kbname} is separate parameter) from the second list as a whole.
      Links of second list concepts(each concept is {id}, {kbname} is separate parameter) are collected together, thus forming a "virtual" article, similarity to which is computed.
      linkWeight specifies method for computation of link weight in case of multiple link types - check REST Documentation for values"""
    first = self.__wrapConcepts(concepts, kbname)
    first += 'linkWeight={};'.format(linkWeight)
    second = self.__wrapConcepts(virtualAricle, kbname)
    return self.__presetKBM('similarityToVirtualArticle', [first, second])

  def similarityBetweenVirtualArticles(self, firstVirtualAricle, secondVirtualArticle, kbname, linkWeight='MAX'):
    """Compute similarity between two sets of concepts(list or single concept, each concept is {id}, {kbname} is separate parameter) as between "virtual" articles from these sets.
      The links of each virtual article are composed of links of the collection of concepts.
      linkWeight specifies method for computation of link weight in case of multiple link types - check REST Documentation for values"""
    first = self.__wrapConcepts(firstVirtualAricle, kbname)
    first += 'linkWeight={};'.format(linkWeight)
    second = self.__wrapConcepts(secondVirtualArticle, kbname)
    return self.__presetKBM('similarityBetweenVirtualArticles', [first, second])

  def similarOverFirstNeighbours(self, concepts, kbname, linkWeight='MAX', offset=None, limit=None):
    """Search for similar concepts among the first neighbours of the given ones(list or single concept, each concept is {id}, {kbname} is separate parameter).
      linkWeight specifies method for computation of link weight in case of multiple link types.
      offset provides a possibility to skip several concepts from the start of the result.
      limit provides a possibility to limit size of result.
      check REST Documentation for values"""
    path = '{0};linkWeight={1}'.format(self.__wrapConcepts(concepts, kbname), linkWeight)
    query = {}
    if offset:
      query.update({'offset': offset})
    if limit:
      query.update({'limit': limit})
    return self.__presetKBM('similarOverFirstNeighbours', path, query)

  def similarOverFilteredNeighbours(self, concepts, kbname, linkWeight='MAX', offset=None, limit=None, among=None):
    """Search for similar concepts over filtered set of the first and the second neighbours of the given ones(list or single concept, each concept is {id}, {kbname} is separate parameter).
      linkWeight specifies method for computation of link weight in case of multiple link types.
      offset provides a possibility to skip several concepts from the start of the result.
      limit provides a possibility to limit size of result.
      check REST Documentation for values"""
    path = '{0};linkWeight={1}'.format(self.__wrapConcepts(concepts, kbname), linkWeight)
    query = {'among': ''}
    if offset:
      query.update({'offset': offset})
    if limit:
      query.update({'limit': limit})
    if among:
      query.update({'among': among})
    return self.__presetKBM('similarOverFilteredNeighbours', path, query)

  def getAttributes(self, concepts, kbname, atrList=[]):
    """Get attributes for concepts(list or single concept, each concept is {id}, {kbname} is separate parameter).
      Supported attributes:
        coordinates - GPS coordinates
        definition - brief concept definition
        url(<language>) - URL to page with description of the given concept on the specified language
        <language> - language code, like: en, de, fr, ko, ru, ...
        synonym - different textual representations of the concept
        title - concept title
        translation(<language>) textual representation of the concept on the specified language
        <language> - language code, like: en, de, fr, ko, ru, ...
        type - concept type"""
    params = {'attribute': atrList}
    return self.customQuery('walker/{}'.format(self.__wrapConcepts(concepts, kbname)), params)


  def customQuery(self, path, query, form=None):
    """Invoke custom request to Texterra."""
    if form:
      return self.POST(path, query, form)
    else:
      return self.GET(path, query)

  def __presetNLP(self, methodName, text):
    """Utility NLP part method"""
    import sys

    specs = API.NLPSpecs[methodName]
    result = self.POST(specs['path'], specs['params'], {'text': text}, 'json')
    annotations = result['annotations']
    it = annotations.items() if sys.version_info[0] == 3 else annotations.iteritems()
    for k,v in it:
        for an in v:
          an['text'] = text[an['start']:an['end']]
          an['annotated-text'] = text
    return result

  def __presetKBM(self, methodName, pathParam, queryParam={}):
    """Utility EKB part method"""
    specs = API.KBMSpecs[methodName]
    queryParam.update(specs['params'])
    if isinstance(pathParam, list):
      result = self.customQuery(specs['path'].format(*pathParam), queryParam)
    else:
      result = self.customQuery(specs['path'].format(pathParam), queryParam)

    return result
