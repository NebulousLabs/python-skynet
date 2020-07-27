"""Skynet download API.
"""

import json
import os

import requests

from . import utils


def __default_download_options():
    """Returns the default download options."""

    obj = utils.__default_options("/")
    obj['timeout_seconds'] = None

    return obj


def download_file(path, skylink, custom_opts={}):
    """Downloads file to path from given skylink with the given options."""

    path = os.path.normpath(path)
    r = download_file_request(skylink, custom_opts)
    open(path, 'wb').write(r.content)
    r.close()


def download_file_request(skylink, custom_opts={}, stream=False):
    """Posts request to download file."""

    opts = __default_download_options()
    opts.update(custom_opts)

    skylink = utils.__strip_prefix(skylink)
    url = utils.__make_url(opts['portal_url'], opts['endpoint_path'], skylink)

    try:
        return requests.get(url, allow_redirects=True, stream=stream,
                            timeout=opts['timeout_seconds'])
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')


def metadata(skylink, opts=None):
    """Downloads metadata from given skylink."""

    r = metadata_request(skylink, opts)
    return json.loads(r.headers["skynet-file-metadata"])


def metadata_request(skylink, custom_opts={}, stream=False):
    """Posts request to get metadata from given skylink."""

    opts = __default_download_options()
    opts.update(custom_opts)

    skylink = utils.__strip_prefix(skylink)
    url = utils.__make_url(opts['portal_url'], opts['endpoint_path'], skylink)

    try:
        return requests.head(url, allow_redirects=True, stream=stream,
                             timeout=opts['timeout_seconds'])
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')
