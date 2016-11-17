import os, sys
# место, где лежит джанго
sys.path.append('./lib/python2.7/site-packages/')
# место, где лежит проект
sys.path.append('/var/www/html/MyInfoEnv/')
# файл конфигурации проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.py'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()