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
        return type('obj', (object,), {
            'portal_url': 'https://siasky.net',
            'portal_upload_path': 'skynet/skyfile',
            'portal_file_fieldname': 'file',
            'portal_directory_file_fieldname': 'files[]',
            'timeout_seconds': 35,
            'custom_filename': ''
        })

    @staticmethod
    def default_download_options():
        """Returns the default download options."""
        return type('obj', (object,), {
            'portal_url': 'https://siasky.net',
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
        if opts is None:
            opts = Skynet.default_upload_options()

        with open(path, 'rb') as fd:
            host = opts.portal_url
            path = opts.portal_upload_path
            url = host+'/'+path
            if hasattr(opts, 'timeout_seconds'):
                timeout = opts.timeout_seconds
            else:
                timeout = Skynet.default_upload_options().timeout_seconds
            r = requests.post(url, files={opts.portal_file_fieldname: fd}, timeout=timeout)
        return r

    @staticmethod
    def upload_file_request_with_chunks(path, opts=None):
        """Posts request to upload file with chunks."""
        if opts is None:
            opts = Skynet.default_upload_options()

        filename = opts.custom_filename if opts.custom_filename else path

        url = "%s/%s?filename=%s" % \
            (opts.portal_url, opts.portal_upload_path, filename)
        headers = {'Content-Type': 'application/octet-stream'}
        if hasattr(opts, 'timeout_seconds'):
            timeout = opts.timeout_seconds
        else:
            timeout = Skynet.default_upload_options().timeout_seconds
        r = requests.post(url, data=path, headers=headers, timeout=timeout)
        return r

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
        if not os.path.isdir(path):
            print("Given path is not a directory")
            return None

        if opts is None:
            opts = Skynet.default_upload_options()

        ftuples = []
        files = list(Skynet.__walk_directory(path).keys())
        for filepath in files:
            ftuples.append((opts.portal_directory_file_fieldname,
                            (filepath, open(filepath, 'rb'))))

        filename = opts.custom_filename if opts.custom_filename else path

        host = opts.portal_url
        path = opts.portal_upload_path
        url = "%s/%s?filename=%s" % (host, path, filename)
        if hasattr(opts, 'timeout_seconds'):
            timeout = opts.timeout_seconds
        else:
            timeout = Skynet.default_upload_options().timeout_seconds
        r = requests.post(url, files=ftuples, timeout=timeout)
        return r

    @staticmethod
    def download_file(path, skylink, opts=None):
        """Downloads file to path from given skylink with the given options."""
        r = Skynet.download_file_request(skylink, opts)
        open(path, 'wb').write(r.content)
        r.close()

    @staticmethod
    def download_file_request(skylink, opts=None, stream=False):
        """Posts request to download file."""
        if opts is None:
            opts = Skynet.default_download_options()

        portal = opts.portal_url
        skylink = Skynet.__strip_prefix(skylink)
        url = portal+'/'+skylink
        if hasattr(opts, 'timeout_seconds'):
            timeout = opts.timeout_seconds
        else:
            timeout = Skynet.default_upload_options().timeout_seconds
        r = requests.get(url, allow_redirects=True, stream=stream, timeout=timeout)
        return r

    @staticmethod
    def metadata(skylink, opts=None):
        """Downloads metadata from given skylink."""
        r = Skynet.metadata_request(skylink, opts)
        return json.loads(r.headers["skynet-file-metadata"])

    @staticmethod
    def metadata_request(skylink, opts=None, stream=False):
        """Posts request to get metadata from given skylink."""
        if opts is None:
            opts = Skynet.default_download_options()

        portal = opts.portal_url
        skylink = Skynet.__strip_prefix(skylink)
        url = portal+'/'+skylink
        if hasattr(opts, 'timeout_seconds'):
            timeout = opts.timeout_seconds
        else:
            timeout = Skynet.default_upload_options().timeout_seconds
        r = requests.head(url, allow_redirects=True, stream=stream, timeout=timeout)
        return r

    @staticmethod
    def __walk_directory(path):
        """Walks given directory returning all files recursively."""
        files = {}
        for root, subdirs, subfiles in os.walk(path):
            for subdir in subdirs:
                subdir = os.path.join(root, subdir)
                files.update(Skynet.__walk_directory(subdir))
            for subfile in subfiles:
                fullpath = os.path.join(root, subfile)
                files[fullpath] = True
        return files
