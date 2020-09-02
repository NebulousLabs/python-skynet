"""Skynet upload API.
"""

import os

from . import utils


def default_upload_options():
    """Returns the default upload options."""

    obj = utils.default_options("/skynet/skyfile")
    obj['portal_file_fieldname'] = 'file'
    obj['portal_directory_file_fieldname'] = 'files[]'
    obj['custom_filename'] = ''
    obj['custom_dirname'] = ''

    return obj


def upload_file(self, path, custom_opts=None):
    """Uploads file at path with the given options."""

    response = self.upload_file_request(path, custom_opts)
    sia_url = utils.uri_skynet_prefix() + response.json()["skylink"]
    response.close()
    return sia_url


def upload_file_request(self, path, custom_opts=None):
    """
    Posts request to upload file.

    :param str path: The local path of the file to upload.
    :param dict custom_opts: Custom options. See upload_file.
    :return: the full response
    :rtype: dict
    """

    opts = default_upload_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isfile(path):
        print("Given path is not a file")
        return None

    with open(path, 'rb') as file_h:
        filename = opts['custom_filename'] if opts['custom_filename'] \
            else os.path.basename(file_h.name)
        files = {opts['portal_file_fieldname']: (filename, file_h)}

        return self.execute_request(
            "POST",
            opts,
            files=files,
        )


def upload_file_request_with_chunks(self, path, custom_opts=None):
    """Posts request to upload file with chunks."""

    opts = default_upload_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isfile(path):
        print("Given path is not a file")
        return None

    filename = opts['custom_filename'] if opts['custom_filename'] else path
    params = {filename: filename}
    headers = {'Content-Type': 'application/octet-stream'}

    return self.execute_request(
        "POST",
        opts,
        data=path,
        headers=headers,
        params=params,
    )


def upload_directory(self, path, custom_opts=None):
    """Uploads directory at path with the given options."""

    response = self.upload_directory_request(path, custom_opts)
    sia_url = utils.uri_skynet_prefix() + response.json()["skylink"]
    response.close()
    return sia_url


def upload_directory_request(self, path, custom_opts=None):
    """Posts request to upload directory."""

    opts = default_upload_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    path = os.path.normpath(path)
    if not os.path.isdir(path):
        print("Given path is not a directory")
        return None

    ftuples = []
    basepath = path if path == '/' else path + '/'
    files = list(utils.walk_directory(path).keys())
    for filepath in files:
        assert filepath.startswith(basepath)
        ftuples.append((opts['portal_directory_file_fieldname'],
                        (filepath[len(basepath):], open(filepath, 'rb'))))

    dirname = opts['custom_dirname'] if opts['custom_dirname'] else path

    params = {"filename": dirname}

    return self.execute_request(
        "POST",
        opts,
        files=ftuples,
        params=params,
    )
