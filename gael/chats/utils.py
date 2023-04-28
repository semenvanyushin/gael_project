import os
from django.core.files.storage import FileSystemStorage
from gael import settings
from urllib.parse import urljoin


class CkeditorCustomStorage(FileSystemStorage):
    '''Кастомное расположение для медиа файлов редактора'''
    location = os.path.join(settings.MEDIA_ROOT, 'uploads/images/')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/images/')
