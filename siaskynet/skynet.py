import os
import random
import string

import requests


class Skynet:
    @staticmethod
    def default_upload_options():
        return type('obj', (object,), {
            'portalUrl': 'https://siasky.net',
            'portalUploadPath': 'skynet/skyfile',
            'portalFileFieldname': 'file',
            'portalDirectoryFileFieldname': 'files[]',
            'customFilename': ''
        })

    @staticmethod
    def default_download_options():
        return type('obj', (object,), {
            'portalUrl': 'https://siasky.net',
        })

    @staticmethod
    def strip_prefix(str):
        if str.startswith("sia://"):
            return str[len("sia://"):]
        return str

    @staticmethod
    def UploadFile(path, opts=None):
        return "sia://" + Skynet.UploadFileRequest(path, opts).json()["skylink"]

    @staticmethod
    def UploadFileRequest(path, opts=None):
        if opts is None:
            opts = Skynet.default_upload_options()

        charset = string.ascii_lowercase
        uuid = ''.join(random.choice(charset) for i in range(16))

        with open(path, 'rb') as f:
            host = opts.portalUrl
            path = opts.portalUploadPath
            url = f'{host}/{path}/{uuid}'
            r = requests.post(url, files={opts.portalFileFieldname: f})
        return r

    @staticmethod
    def UploadDirectory(path, opts=None):
        return "sia://" + Skynet.UploadDirectoryRequest(path, opts).json()["skylink"]

    @staticmethod
    def UploadDirectoryRequest(path, opts=None):
        if os.path.isdir(path) == False:
            print("Given path is not a directory")
            return

        if opts is None:
            opts = Skynet.default_upload_options()

        ftuples = []
        files = list(Skynet.walkDirectory(path).keys())
        for file in files:
            ftuples.append((opts.portalDirectoryFileFieldname,
                            (file, open(file, 'rb'))))

        charset = string.ascii_lowercase
        uuid = ''.join(random.choice(charset) for i in range(16))

        filename = opts.customFilename if opts.customFilename else path

        host = opts.portalUrl
        path = opts.portalUploadPath
        url = f'{host}/{path}/{uuid}?filename={filename}'
        r = requests.post(url, files=ftuples)
        return r

    @staticmethod
    def DownloadFile(path, skylink, opts=None):
        r = Skynet.DownloadFileRequest(skylink, opts)
        open(path, 'wb').write(r.content)

    @staticmethod
    def DownloadFileRequest(skylink, opts=None):
        if opts is None:
            opts = Skynet.default_download_options()

        portal = opts.portalUrl
        skylink = Skynet.strip_prefix(skylink)
        url = f'{portal}/{skylink}'
        r = requests.get(url, allow_redirects=True)
        return r

    @staticmethod
    def walkDirectory(path):
        files = {}
        for root, subdirs, subfiles in os.walk(path):
            for subdir in subdirs:
                files.update(Skynet.walkDirectory(os.path.join(root, subdir)))
            for subfile in subfiles:
                fullpath = os.path.join(root, subfile)
                files[fullpath] = True
        return files