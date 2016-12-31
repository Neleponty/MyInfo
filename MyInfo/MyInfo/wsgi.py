import os, sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/home/MyInfo/MyInfo/MyInfo/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
"""
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
"""
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
