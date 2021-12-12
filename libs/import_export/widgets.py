from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.core.files import File
from django.core.files.storage import default_storage

from import_export.widgets import CharWidget

from libs.import_export.utils import (
    download_file,
    get_file_extension,
    url_to_internal_value,
)


class FileWidget(CharWidget):
    """Widget for working with File fields"""

    def __init__(self, filename):
        """
        Args:
            filename (str): Filename to save file
        """
        self.filename = filename

    def render(self, value, obj=None):
        """Convert DB value to URL to file"""
        if value:
            if (
                    settings.DEFAULT_FILE_STORAGE
                    == 'django.core.files.storage.FileSystemStorage'
            ):
                return f'http://localhost:8000{value.url}'
            return value.url

    def clean(self, value, *args, **kwargs):
        """Get the file and check for exists."""
        if not value:
            return

        internal_url = url_to_internal_value(urlparse(value).path)

        try:
            if default_storage.exists(internal_url):
                return internal_url
        except SuspiciousFileOperation:
            pass

        return self._get_file(value)

    def _get_file(self, url):
        """Download file from the external resource."""
        ext = get_file_extension(url)
        file = download_file(url)
        return File(file, f'{self.filename}.{ext}')
