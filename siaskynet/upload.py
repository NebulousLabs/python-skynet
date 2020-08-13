"""Skynet upload API.
"""

import os

from . import utils


def __default_upload_options():
    """Returns the default upload options."""

    obj = utils.__default_options("/skynet/skyfile")
    obj['portal_file_fieldname'] = 'file'
    obj['portal_directory_file_fieldname'] = 'files[]'
    obj['custom_filename'] = ''
    obj['custom_dirname'] = ''

    return obj


def upload_file(path, custom_opts={}):
    """Uploads file at path with the given options."""

    r = upload_file_request(path, custom_opts)
    sia_url = utils.uri_skynet_prefix() + r.json()["skylink"]
    r.close()
    return sia_url


def upload_file_request(path, custom_opts={}):
    """
    Posts request to upload file.

    :param str path: The local path of the file to upload.
    :param dict custom_opts: Custom options. See upload_file.
    :return: the full response
    :rtype: dict
    """

    opts = __default_upload_options()
    opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isfile(path):
        print("Given path is not a file")
        return None

    with open(path, 'rb') as fd:
        url = utils.__make_url(opts['portal_url'], opts['endpoint_path'])
        filename = opts['custom_filename'] if opts['custom_filename'] \
            else os.path.basename(fd.name)
        files = {opts['portal_file_fieldname']: (filename, fd)}

        return utils.__execute_request(
            "POST",
            url,
            opts,
            files=files,
        )


def upload_file_request_with_chunks(path, custom_opts={}):
    """Posts request to upload file with chunks."""

    opts = __default_upload_options()
    opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isfile(path):
        print("Given path is not a file")
        return None

    url = utils.__make_url(opts['portal_url'], opts['endpoint_path'])
    filename = opts['custom_filename'] if opts['custom_filename'] else path
    params = {filename: filename}
    headers = {'Content-Type': 'application/octet-stream'}

    return utils.__execute_request(
        "POST",
        url,
        opts,
        data=path,
        headers=headers,
        params=params,
    )


def upload_directory(path, custom_opts={}):
    """Uploads directory at path with the given options."""

    r = upload_directory_request(path, custom_opts)
    sia_url = utils.uri_skynet_prefix() + r.json()["skylink"]
    r.close()
    return sia_url


def upload_directory_request(path, custom_opts={}):
    """Posts request to upload directory."""

    opts = __default_upload_options()
    opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isdir(path):
        print("Given path is not a directory")
        return None

    ftuples = []
    basepath = path if path == '/' else path + '/'
    files = list(utils.__walk_directory(path).keys())
    for filepath in files:
        assert filepath.startswith(basepath)
        ftuples.append((opts['portal_directory_file_fieldname'],
                        (filepath[len(basepath):], open(filepath, 'rb'))))

    dirname = opts['custom_dirname'] if opts['custom_dirname'] else path

    url = utils.__make_url(opts['portal_url'], opts['endpoint_path'])
    params = {"filename": dirname}

    return utils.__execute_request(
        "POST",
        url,
        opts,
        files=ftuples,
        params=params,
    )
