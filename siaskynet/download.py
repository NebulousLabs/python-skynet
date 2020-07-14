"""Skynet download API.
"""

import json
import os

import requests

from . import utils


def default_download_options():
    """Returns the default download options."""
    return __fill_with_default_download_options()


def __fill_with_default_download_options(opts=None):
    """Fills in missing options with the default download options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())
    timeout_seconds = getattr(opts, 'timeout_seconds', None)

    return type('obj', (object,), {
        'portal_url': portal_url,
        'timeout_seconds': timeout_seconds
    })


def download_file(path, skylink, opts=None):
    """Downloads file to path from given skylink with the given options."""

    path = os.path.normpath(path)
    r = download_file_request(skylink, opts)
    open(path, 'wb').write(r.content)
    r.close()


def download_file_request(skylink, opts=None, stream=False):
    """Posts request to download file."""

    opts = __fill_with_default_download_options(opts)

    portal = opts.portal_url
    skylink = utils.__strip_prefix(skylink)
    url = portal+'/'+skylink

    try:
        return requests.get(url, allow_redirects=True, stream=stream,
                            timeout=opts.timeout_seconds)
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')


def metadata(skylink, opts=None):
    """Downloads metadata from given skylink."""
    r = metadata_request(skylink, opts)
    return json.loads(r.headers["skynet-file-metadata"])


def metadata_request(skylink, opts=None, stream=False):
    """Posts request to get metadata from given skylink."""
    opts = __fill_with_default_download_options(opts)

    portal = opts.portal_url
    skylink = utils.__strip_prefix(skylink)
    url = portal+'/'+skylink

    try:
        return requests.head(url, allow_redirects=True, stream=stream,
                             timeout=opts.timeout_seconds)
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')
