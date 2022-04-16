
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cb_dj_weather_app.settings')

application = get_asgi_application()
