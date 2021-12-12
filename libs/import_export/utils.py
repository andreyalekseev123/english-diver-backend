import html
import operator
import os
import re
import unicodedata
import uuid
from urllib.parse import unquote_plus

from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils.html import strip_tags

import requests
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


def normalize_string_value(value):
    """Normalize string value.

    1. Remove leading and trailing whitespaces.
    2. Replace all space characters (' \t\n\r\x0b\x0c') with the Space char.
    3. Remove Unicode C0 controls to prevent problems with the creation of
    XLS(X) files with `openpyxl` lib.
    4. Normalize Unicode string, using `NFKC` form. See the details:
    https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize

    """
    cleaned = ' '.join(value.strip().split()).strip()
    return remove_illegal_characters(cleaned)


def get_default_file_mime_type():
    """Returns default MIME type"""
    return settings.MIME_TYPES_MAP['.bin']


def get_mime_type_by_file_url(file_url):
    """Retrieve file's mime type by file's url according to
    `MIME_TYPES_MAP` from setting

    If file extension not in `MIME_TYPES_MAP` it returns default mime type
    for binary files
    """
    file_extension = f'.{get_file_extension(file_url)}'
    if file_extension in settings.MIME_TYPES_MAP:
        return settings.MIME_TYPES_MAP[file_extension]

    return get_default_file_mime_type()


def get_class_fullname(klass):
    """Get fully qualified class name of an class in Python.
    """
    return '.'.join([klass.__module__, klass.__name__])


def upload_media_path(model_instance, filename):
    """Function for generation of upload path for Django model instance.

    Generates upload path that contain instance's model app, model name,
    object's ID, salt and file name.
    """
    components = model_instance._meta.label_lower.split('.')
    components.append(str(model_instance.id))
    components.append(str(uuid.uuid4()))
    components.append(filename)

    return os.path.join(*components)


def download_file(external_url):
    """Download file from external resource and return the file object."""
    mime_type = get_mime_type_by_file_url(external_url)
    data = requests.get(external_url)
    file = ContentFile(data.content)
    file.content_type = mime_type
    return file


def get_file_extension(url, lower=True):
    """Method to extract file extension from path/URL.

    Args:
        url (str): Path to the file
        lower (boolean): Extension in lower
    Returns:
        String: extension of the file (lower or not)

    Example:
        'dir/subdir/file.ext' -> 'ext'

    """
    get_index = url.find('?')
    if get_index != -1:
        url = url[:get_index]  # remove GET params from URL
    ext = os.path.splitext(url)[1][1:]
    return ext.lower() if lower else ext


def get_attr(obj, attr_path, **kwargs):
    """Returns attribute of object, defined with in dot-path

    Examples:
        obj = Book(**kwargs)
        get_attr(obj, 'book.author.id', raise_attr_error=True)
        # returns obj.book.author.id

    Args:
        obj (object): object to process
        attr_path (str): path to attribute (Example: 'book.author.id')
        default (object): default value to return if ``raise_attr_error``
            is False
        raise_attr_error (bool): if True AttriubuteError will be raised if
            attribute does not exists

    Returns:
        object: attribute's value
    """
    _getattr = operator.attrgetter(attr_path)

    try:
        return _getattr(obj)
    except AttributeError:
        if 'default' in kwargs:
            return kwargs['default']
        raise


def html_to_plain(text):
    """Convert HTML to plain text with dummy formatting"""
    line_break_regex = r'<\s*?/?\s*?(((b|B)(r|R))|(p|P))\s*?/?\s*?>'

    value = re.sub(line_break_regex, '\n', text)
    value = strip_tags(value)
    value = html.unescape(value)

    return value


def url_to_internal_value(file_url):
    """Convert file url to internal value"""

    file_url = unquote_plus(file_url)
    # manually remove scheme and domain parts, because file name may
    # contain '#' or '?' and they parsed incorrectly
    file_url = file_url.split('://')[-1]
    file_url = file_url.split('/')[1:]
    file_url = '/'.join(file_url)

    if file_url.startswith(settings.MEDIA_URL[1:]):
        # In case of local storing crop the media prefix
        file_url = file_url[len(settings.MEDIA_URL) - 1:]

    elif (getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
            and settings.AWS_STORAGE_BUCKET_NAME in file_url):
        # In case of S3 upload crop S3 bucket name
        file_url = file_url.split(f'{settings.AWS_STORAGE_BUCKET_NAME}/')[-1]

    return file_url


def remove_illegal_characters(value):
    """Remove `illegal` characters from string values.

    1. Remove Unicode C0 controls to prevent problems with the creation of
    XLS(X) files with `openpyxl` lib.
    2. Normalize Unicode string, using `NFKC` form. See the details:
    https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize

    """
    return unicodedata.normalize(
        'NFKC',
        re.sub(ILLEGAL_CHARACTERS_RE, '', value)
    )


def get_clear_q_filter(str_value, attribute_name):
    """Makes clear Q filter for ``str_value``

    For given string we must create regex pattern that isn't
    dependent on word's cases and extra whitespaces.

    First we build regular expression for ``str_value``
        Example:
            if str_value = 'Hello, world' then regex patter for it
            is '^Hello\s+world$'

    Then for regex patter we create Q filter.
        Example:
            If attribute_name is 'title' then Q filter is
            Q(title__iregex='^Hello\s+world$')

    Args:
        str_value: some string
        attribute_name: model's attribute name

    """  # noqa: W605
    q_regex_attr = '{0}__iregex'.format(attribute_name)

    try:
        str_value.encode('ascii')
        esc = re.escape
    except UnicodeEncodeError:
        esc = escape

    words = str_value.split()
    words = map(esc, words)
    pattern = r'\s+'.join(words)
    pattern = r'^{0}$'.format(pattern)

    # build Q filter and append in list
    return Q(**{q_regex_attr: pattern})


def clean_sequence_of_string_values(sequence, ignore_empty=True):
    """Clean sequence of string values.

    Normalize each string value.
    Remove empty items form sequence if `ignore_empty` is True.

    Args:
        sequence: list of strings
        ignore_empty: boolean value which defines should empty strings be
                      removed from sequence or not

    Returns:
        cleared_sequence: list of cleared sequence items

    """
    sequence = (normalize_string_value(item) for item in sequence)
    if ignore_empty:
        return list(filter(None, sequence))

    return list(sequence)


def clear_string(string):
    """Normalize ``string`` and make it lower case.

    Also drop spaces after and before ``:``. It's needed for custom fields
    headers
    """
    string = string.lower()
    string = normalize_string_value(string)
    string = string.replace(': ', ':').replace(' :', ':')
    return string


def clear_seq_items(sequence):
    """Clear sequence items

    Each item of sequence should be a string

    For each string in sequence drop extra whitespaces and
    make it to lower case

    """
    return list(map(clear_string, sequence))


def escape(s):
    """Escapes special characters in unicode string"""
    return re.sub(r'[(){}\[\].*?|^$\\+-]', r'\\\g<0>', s)


def _get_random_path(obj, filename):
    """Get random path.

    Adds prefix like ``app/modelname/id`` and filename from object
    ``filename`` field.
    """
    split_path = obj._meta.label_lower.split('.')
    split_path.append(str(obj.id))

    return os.path.join(*split_path, obj.filename)
