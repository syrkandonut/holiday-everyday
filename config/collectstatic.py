import os

from django.conf.urls.static import static

from config import settings

STATICFILES = []

for url, dir in settings.STATIC_CONFIG.items():
    STATICFILES += static(url, document_root=os.path.join(settings.BASE_DIR, dir))
