import os, sys
# �����, ��� ����� ������
sys.path.append('./lib/python2.7/site-packages/')
# �����, ��� ����� ������
sys.path.append('/var/www/html/MyInfoEnv/')
# ���� ������������ �������
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.py'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()