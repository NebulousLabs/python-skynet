import os
import string

import requests


class Skynet:

    @staticmethod
    def uri_skynet_prefix():
        return "sia://"

    @staticmethod
    def default_upload_options():
        return type('obj', (object,), {
            'portal_url': 'https://siasky.net',
            'portal_upload_path': 'skynet/skyfile',
            'portal_file_fieldname': 'file',
            'portal_directory_file_fieldname': 'files[]',
            'custom_filename': ''
        })

    @staticmethod
    def default_download_options():
        return type('obj', (object,), {
            'portal_url': 'https://siasky.net',
        })

    @staticmethod
    def strip_prefix(str):
        if str.startswith(Skynet.uri_skynet_prefix()):
            return str[len(Skynet.uri_skynet_prefix()):]
        return str

    @staticmethod
    def upload_file(path, opts=None):
        return Skynet.uri_skynet_prefix() + Skynet.upload_file_request(path, opts).json()["skylink"]

    @staticmethod
    def upload_file_request(path, opts=None):
        if opts is None:
            opts = Skynet.default_upload_options()

        with open(path, 'rb') as f:
            host = opts.portal_url
            path = opts.portal_upload_path
            url = f'{host}/{path}'
            r = requests.post(url, files={opts.portal_file_fieldname: f})
        return r

    @staticmethod
    def upload_file_request_with_chunks(path, opts=None):
        if opts is None:
            opts = Skynet.default_upload_options()

        filename = opts.custom_filename if opts.custom_filename else path

        r = requests.post("%s/%s?filename=%s" % (opts.portal_url, opts.portal_upload_path,
                                                 filename), data=path, headers={'Content-Type': 'application/octet-stream'})
        return r

    @staticmethod
    def upload_directory(path, opts=None):
        r = Skynet.upload_directory_request(path, opts)
        sia_url = Skynet.uri_skynet_prefix() + r.json()["skylink"]
        r.close()
        return sia_url

    @staticmethod
    def upload_directory_request(path, opts=None):
        if os.path.isdir(path) == False:
            print("Given path is not a directory")
            return

        if opts is None:
            opts = Skynet.default_upload_options()

        ftuples = []
        files = list(Skynet.walk_directory(path).keys())
        for file in files:
            ftuples.append((opts.portal_directory_file_fieldname,
                            (file, open(file, 'rb'))))

        filename = opts.custom_filename if opts.custom_filename else path

        host = opts.portal_url
        path = opts.portal_upload_path
        url = f'{host}/{path}?filename={filename}'
        r = requests.post(url, files=ftuples)
        return r

    @staticmethod
    def download_file(path, skylink, opts=None):
        r = Skynet.download_file_request(skylink, opts)
        open(path, 'wb').write(r.content)
        r.close()

    @staticmethod
    def download_file_request(skylink, opts=None, stream=False):
        if opts is None:
            opts = Skynet.default_download_options()

        portal = opts.portal_url
        skylink = Skynet.strip_prefix(skylink)
        url = f'{portal}/{skylink}'
        r = requests.get(url, allow_redirects=True, stream=stream)
        return r

    @staticmethod
    def walk_directory(path):
        files = {}
        for root, subdirs, subfiles in os.walk(path):
            for subdir in subdirs:
                files.update(Skynet.walk_directory(os.path.join(root, subdir)))
            for subfile in subfiles:
                fullpath = os.path.join(root, subfile)
                files[fullpath] = True
        return files