"""An SDK for integrating Skynet into Python applications.
"""

import json
import os

import requests


class Skynet:
    """Contains static methods making up the Skynet API."""

    @staticmethod
    def uri_skynet_prefix():
        """Returns the Skynet URI prefix."""
        return "sia://"

    @staticmethod
    def default_upload_options():
        """Returns the default upload options."""
        return Skynet.__fill_with_default_upload_options()

    @staticmethod
    def __fill_with_default_upload_options(opts=None):
        """Fills in missing options with the default upload options."""
        portal_url = getattr(opts, 'portal_url', 'https://siasky.net')
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

    @staticmethod
    def default_download_options():
        """Returns the default download options."""
        return Skynet.__fill_with_default_download_options()

    @staticmethod
    def __fill_with_default_download_options(opts=None):
        """Fills in missing options with the default download options."""
        portal_url = getattr(opts, 'portal_url', 'https://siasky.net')
        timeout_seconds = getattr(opts, 'timeout_seconds', None)

        return type('obj', (object,), {
            'portal_url': portal_url,
            'timeout_seconds': timeout_seconds
        })

    @staticmethod
    def __strip_prefix(string):
        """Strips Skynet prefix from input."""
        if string.startswith(Skynet.uri_skynet_prefix()):
            return string[len(Skynet.uri_skynet_prefix()):]
        return string

    @staticmethod
    def upload_file(path, opts=None):
        """Uploads file at path with the given options."""
        skylink = Skynet.upload_file_request(path, opts).json()["skylink"]
        return Skynet.uri_skynet_prefix() + skylink

    @staticmethod
    def upload_file_request(path, opts=None):
        """Posts request to upload file."""

        path = os.path.normpath(path)
        opts = Skynet.__fill_with_default_upload_options(opts)

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

    @staticmethod
    def upload_file_request_with_chunks(path, opts=None):
        """Posts request to upload file with chunks."""

        path = os.path.normpath(path)
        opts = Skynet.__fill_with_default_upload_options(opts)

        filename = opts.custom_filename if opts.custom_filename else path
        url = "%s/%s?filename=%s" % \
            (opts.portal_url, opts.portal_upload_path, filename)
        headers = {'Content-Type': 'application/octet-stream'}

        try:
            return requests.post(url, data=path, headers=headers,
                                 timeout=opts.timeout_seconds)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

    @staticmethod
    def upload_directory(path, opts=None):
        """Uploads directory at path with the given options."""

        r = Skynet.upload_directory_request(path, opts)
        sia_url = Skynet.uri_skynet_prefix() + r.json()["skylink"]
        r.close()
        return sia_url

    @staticmethod
    def upload_directory_request(path, opts=None):
        """Posts request to upload directory."""

        path = os.path.normpath(path)

        if not os.path.isdir(path):
            print("Given path is not a directory")
            return None

        opts = Skynet.__fill_with_default_upload_options(opts)

        ftuples = []
        basepath = path if path == '/' else path + '/'
        files = list(Skynet.__walk_directory(path).keys())
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

    @staticmethod
    def download_file(path, skylink, opts=None):
        """Downloads file to path from given skylink with the given options."""

        path = os.path.normpath(path)
        r = Skynet.download_file_request(skylink, opts)
        open(path, 'wb').write(r.content)
        r.close()

    @staticmethod
    def download_file_request(skylink, opts=None, stream=False):
        """Posts request to download file."""

        opts = Skynet.__fill_with_default_download_options(opts)

        portal = opts.portal_url
        skylink = Skynet.__strip_prefix(skylink)
        url = portal+'/'+skylink

        try:
            return requests.get(url, allow_redirects=True, stream=stream,
                                timeout=opts.timeout_seconds)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

    @staticmethod
    def metadata(skylink, opts=None):
        """Downloads metadata from given skylink."""
        r = Skynet.metadata_request(skylink, opts)
        return json.loads(r.headers["skynet-file-metadata"])

    @staticmethod
    def metadata_request(skylink, opts=None, stream=False):
        """Posts request to get metadata from given skylink."""
        opts = Skynet.__fill_with_default_download_options(opts)

        portal = opts.portal_url
        skylink = Skynet.__strip_prefix(skylink)
        url = portal+'/'+skylink

        try:
            return requests.head(url, allow_redirects=True, stream=stream,
                                 timeout=opts.timeout_seconds)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

    @staticmethod
    def __walk_directory(path):
        """Walks given directory returning all files recursively."""

        path = os.path.normpath(path)

        files = {}
        for root, subdirs, subfiles in os.walk(path):
            for subdir in subdirs:
                subdir = os.path.join(root, subdir)
                files.update(Skynet.__walk_directory(subdir))
            for subfile in subfiles:
                fullpath = os.path.join(root, subfile)
                files[fullpath] = True
        return files
