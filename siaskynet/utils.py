"""Skynet utility functions.
"""

import os


def default_options(endpoint_path):
    """Returns the default options with the given endpoint path."""

    return {
        'endpoint_path': endpoint_path,

        'api_key': None,
        'custom_user_agent': None,
        "timeout_seconds": None,
    }


def default_portal_url():
    """DefaultPortalURL intelligently selects a default portal."""

    # TODO: This will be smarter. See
    # https://github.com/NebulousLabs/skynet-docs/issues/21.

    return default_skynet_portal_url()


def default_skynet_portal_url():
    """Returns the default Skynet portal URL."""

    return 'https://siasky.net'


def make_url(portal_url, *arg):
    """Makes a URL from the given portal url and path elements."""

    url = portal_url
    for path_element in arg:
        if path_element == "":
            continue
        while url.endswith("/"):
            url = url[:-1]
        while path_element.startswith("/"):
            path_element = path_element[1:]
        url = url+"/"+path_element

    return url


def strip_prefix(string):
    """Strips Skynet prefix from input."""

    if string.startswith(uri_skynet_prefix()):
        return string[len(uri_skynet_prefix()):]
    return string


def uri_skynet_prefix():
    """Returns the Skynet URI prefix."""

    return "sia://"


def walk_directory(path):
    """Walks given directory returning all files recursively."""

    path = os.path.normpath(path)

    files = {}
    for root, subdirs, subfiles in os.walk(path):
        for subdir in subdirs:
            subdir = os.path.join(root, subdir)
            files.update(walk_directory(subdir))
        for subfile in subfiles:
            fullpath = os.path.join(root, subfile)
            files[fullpath] = True
    return files
