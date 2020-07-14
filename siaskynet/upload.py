"""Skynet upload API.
"""

import os

import requests

from . import utils


def default_upload_options():
    """Returns the default upload options."""
    return __fill_with_default_upload_options()


def __fill_with_default_upload_options(opts=None):
    """Fills in missing options with the default upload options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())
    portal_upload_path = \
        getattr(opts, 'portal_upload_path', 'skynet/skyfile')
    portal_file_fieldname = getattr(opts, 'portal_file_fieldname', 'file')
    portal_directory_file_fieldname = \
        getattr(opts, 'portal_directory_file_fieldname', 'files[]')
    custom_filename = getattr(opts, 'custom_filename', '')
    timeout_seconds = getattr(opts, 'timeout_seconds', None)

    return type('obj', (object,), {
        'portal_url': portal_url,
        'portal_upload_path': portal_upload_path,
        'portal_file_fieldname': portal_file_fieldname,
        'portal_directory_file_fieldname': portal_directory_file_fieldname,
        'custom_filename': custom_filename,
        'timeout_seconds': timeout_seconds
    })


def upload_file(path, opts=None):
    """Uploads file at path with the given options."""
    skylink = upload_file_request(path, opts).json()["skylink"]
    return utils.uri_skynet_prefix() + skylink


def upload_file_request(path, opts=None):
    """Posts request to upload file."""

    path = os.path.normpath(path)
    opts = __fill_with_default_upload_options(opts)

    with open(path, 'rb') as fd:
        host = opts.portal_url
        path = opts.portal_upload_path
        url = host+'/'+path
        filename = opts.custom_filename if opts.custom_filename \
            else os.path.basename(fd.name)
        files = {opts.portal_file_fieldname: (filename, fd)}

        try:
            return requests.post(url,
                                 files=files,
                                 timeout=opts.timeout_seconds)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')


def upload_file_request_with_chunks(path, opts=None):
    """Posts request to upload file with chunks."""

    path = os.path.normpath(path)
    opts = __fill_with_default_upload_options(opts)

    filename = opts.custom_filename if opts.custom_filename else path
    url = "%s/%s?filename=%s" % \
        (opts.portal_url, opts.portal_upload_path, filename)
    headers = {'Content-Type': 'application/octet-stream'}

    try:
        return requests.post(url, data=path, headers=headers,
                             timeout=opts.timeout_seconds)
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')


def upload_directory(path, opts=None):
    """Uploads directory at path with the given options."""

    r = upload_directory_request(path, opts)
    sia_url = utils.uri_skynet_prefix() + r.json()["skylink"]
    r.close()
    return sia_url


def upload_directory_request(path, opts=None):
    """Posts request to upload directory."""

    path = os.path.normpath(path)

    if not os.path.isdir(path):
        print("Given path is not a directory")
        return None

    opts = __fill_with_default_upload_options(opts)

    ftuples = []
    basepath = path if path == '/' else path + '/'
    files = list(utils.__walk_directory(path).keys())
    for filepath in files:
        assert filepath.startswith(basepath)
        ftuples.append((opts.portal_directory_file_fieldname,
                        (filepath[len(basepath):], open(filepath, 'rb'))))

    filename = opts.custom_filename if opts.custom_filename else path

    host = opts.portal_url
    path = opts.portal_upload_path
    url = "%s/%s?filename=%s" % (host, path, filename)
    try:
        return requests.post(url, files=ftuples,
                             timeout=opts.timeout_seconds)
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out')
