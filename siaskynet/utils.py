"""Skynet utility functions.
"""

import os

try:
    from urllib import urljoin
except ImportError:  # For Python 3
    from urllib.parse import urljoin


def default_portal_url():
    """Returns the default portal URL."""

    return 'https://siasky.net'


def uri_skynet_prefix():
    """Returns the Skynet URI prefix."""

    return "sia://"


def __default_options(endpoint_path):
    """Returns the default options with the given endpoint path."""

    return {
        'portal_url': default_portal_url(),
        'endpoint_path': endpoint_path,
        # 'custom_user_agent':
        # 'api_key':
    }


def __make_url(portal_url, *arg):
    """Makes a URL from the given portal url and path elements."""

    url = portal_url
    for path_element in arg:
        url = urljoin(portal_url, path_element)

    return url


def __strip_prefix(string):
    """Strips Skynet prefix from input."""

    if string.startswith(uri_skynet_prefix()):
        return string[len(uri_skynet_prefix()):]
    return string


def __walk_directory(path):
    """Walks given directory returning all files recursively."""

    path = os.path.normpath(path)

    files = {}
    for root, subdirs, subfiles in os.walk(path):
        for subdir in subdirs:
            subdir = os.path.join(root, subdir)
            files.update(__walk_directory(subdir))
        for subfile in subfiles:
            fullpath = os.path.join(root, subfile)
            files[fullpath] = True
    return files
