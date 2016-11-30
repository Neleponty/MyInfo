# -*- coding: utf-8 -*-
from . import ispras
class API(ispras.API):
  """This class provides methods to work with Twitter NLP REST via OpenAPI"""

  # Default Twitter NLP path
  twitterName = 'twitter-nlp'
  twitterVersion = '1.0'

  specs = {
    'path': 'extract',
    'params': {}
  }

  def __init__(self, key='', name=None, ver=None, host=None):
    """Provide only apikey to use default Twitter NLP service name and version."""
    if host == None:
      if name == None: name = API.twitterName
      if ver == None: ver = API.twitterVersion
      ispras.API.__init__(self, key, name, ver)
    else:
      ispras.API.__init__(self, host=host, key=key)

  def extractDDE(self, lang, username, screenname, description, tweets):
    """Extracts demographic attributes from provided Twitter info. All info is required, but can be empty"""
    if isinstance(tweets, list):
      tweets = ' '.join(tweets)
    form = {
        'lang': lang,
        'username': username,
        'screenname': screenname,
        'description': description,
        'tweet': tweets
    }
    return self.POST('extract', {}, form)

  def customQuery(self, path, query, form=None):
    """Invoke custom request to Twitter NLP"""
    if form:
      return self.POST(path, query, form)
    else:
      return self.GET(path, query)
