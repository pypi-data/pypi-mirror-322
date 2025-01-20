import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')
os.environ.setdefault('RUN_MAIN', 'true')

application = get_wsgi_application()
