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


def upload(self, upload_data, custom_opts=None):
    """Uploads the given generic data and returns the skylink."""

    response = self.upload_request(upload_data, custom_opts)
    sia_url = utils.uri_skynet_prefix() + response.json()["skylink"]
    response.close()
    return sia_url


def upload_request(self, upload_data, custom_opts=None):
    """Uploads the given generic data and returns the response object."""

    opts = default_upload_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    if len(upload_data) == 1:
        fieldname = opts['portal_file_fieldname']
        # this appears to be missing in go sdk; maybe the server ignores it?
        filename = opts['custom_filename']
    else:
        if not opts['custom_dirname']:
            raise ValueError("custom_dirname must be set when "
                             "uploading multiple files")
        fieldname = opts['portal_directory_file_fieldname']
        filename = opts['custom_dirname']

    params = {
        'filename': filename,
        # 'skykeyname': opts['skykey_name'],
        # 'skykeyid': opts['skyket_id'],
    }

    ftuples = []
    for filename, data in upload_data.items():
        ftuples.append((fieldname,
                        (filename, data)))

    if len(upload_data) == 1:
        data = ftuples[0][1][1]
        if hasattr(data, '__iter__') and (
                not isinstance(data, bytes) and
                not isinstance(data, str) and
                not hasattr(data, 'read')):
            # an iterator for chunked uploading
            return self.execute_request(
                "POST",
                opts,
                data=data,
                headers={'Content-Type': 'application/octet-stream'},
                params=params
            )
    return self.execute_request(
        "POST",
        opts,
        files=ftuples,
        params=params
    )


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
        if not opts['custom_filename']:
            opts['custom_filename'] = os.path.basename(file_h.name)

        upload_data = {opts['custom_filename']: file_h}

        return self.upload_request(upload_data, opts)


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

    upload_data = {}
    basepath = path if path == '/' else path + '/'
    for filepath in utils.walk_directory(path):
        assert filepath.startswith(basepath)
        upload_data[filepath[len(basepath):]] = open(filepath, 'rb')

    if not opts['custom_dirname']:
        opts['custom_dirname'] = path

    return self.upload_request(upload_data, opts)
