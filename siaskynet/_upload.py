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

    # Upload as a directory if the dirname is set, even if there is only 1
    # file.
    issinglefile = len(upload_data) == 1 and not opts['custom_dirname']

    filename = ''
    if issinglefile:
        fieldname = opts['portal_file_fieldname']
    else:
        if not opts['custom_dirname']:
            raise ValueError("custom_dirname must be set when "
                             "uploading multiple files")
        fieldname = opts['portal_directory_file_fieldname']
        filename = opts['custom_dirname']

    params = {
        # 'skykeyname': opts['skykey_name'],
        # 'skykeyid': opts['skyket_id'],
    }
    if filename:
        params['filename'] = filename

    ftuples = []
    for filename, data in upload_data.items():
        ftuples.append((fieldname,
                        (filename, data)))

    if issinglefile:
        data = ftuples[0][1][1]
        if hasattr(data, '__iter__') and (
                not isinstance(data, bytes) and
                not isinstance(data, str) and
                not hasattr(data, 'read')):
            # an iterator for chunked uploading
            params['filename'] = ftuples[0][1][0]
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
        filename = os.path.basename(file_h.name)
        if opts['custom_filename']:
            filename = opts['custom_filename']

        upload_data = {filename: file_h}

        return self.upload_request(upload_data, opts)


def upload_file_with_chunks(self, chunks, custom_opts=None):
    """
    Uploads a chunked or streaming file with the given options.
    For more information on chunked uploading, see:
    https://requests.readthedocs.io/en/stable/user/advanced/#chunk-encoded-requests

    :param iter data: An iterator (for chunked encoding) or file-like object
    :param dict custom_opts: Custom options. See upload_file.
    """

    response = self.upload_file_request_with_chunks(chunks, custom_opts)
    sia_url = utils.uri_skynet_prefix() + response.json()["skylink"]
    response.close()
    return sia_url


def upload_file_request_with_chunks(self, chunks, custom_opts=None):
    """
    Posts request for chunked or streaming upload of a single file.
    For more information on chunked uploading, see:
    https://requests.readthedocs.io/en/stable/user/advanced/#chunk-encoded-requests

    :param iter chunks: An iterator (for chunked encoding) or file-like object
    :param dict custom_opts: Custom options. See upload_file.
    :return: the full response
    :rtype: dict
    """

    opts = default_upload_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    if opts['custom_filename']:
        filename = opts['custom_filename']
    else:
        # this is the legacy behavior
        filename = str(chunks)

    upload_data = {filename: chunks}

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
