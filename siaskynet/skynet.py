import os
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

        with open(path, 'rb') as f:
            host = opts.portalUrl
            path = opts.portalUploadPath
            url = f'{host}/{path}'
            r = requests.post(url, files={opts.portalFileFieldname: f})
        return r

    @staticmethod
    def UploadFileRequestWithChunks(path, opts=None):
        if opts is None:
            opts = Skynet.default_upload_options()

        filename = opts.customFilename if opts.customFilename else path

        r = requests.post("%s/%s?filename=%s" % (opts.portalUrl, opts.portalUploadPath, filename), data=path, headers={'Content-Type': 'application/octet-stream'})
        return r

    @staticmethod
    def UploadDirectory(path, opts=None):
        r = Skynet.UploadDirectoryRequest(path, opts)
        sia_url = "sia://" + r.json()["skylink"]
        r.close()
        return sia_url

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

        filename = opts.customFilename if opts.customFilename else path

        host = opts.portalUrl
        path = opts.portalUploadPath
        url = f'{host}/{path}?filename={filename}'
        r = requests.post(url, files=ftuples)
        return r

    @staticmethod
    def DownloadFile(path, skylink, opts=None):
        r = Skynet.DownloadFileRequest(skylink, opts)
        open(path, 'wb').write(r.content)
        r.close()

    @staticmethod
    def DownloadFileRequest(skylink, opts=None, stream=False):
        if opts is None:
            opts = Skynet.default_download_options()

        portal = opts.portalUrl
        skylink = Skynet.strip_prefix(skylink)
        url = f'{portal}/{skylink}'
        r = requests.get(url, allow_redirects=True, stream=stream)
        return r

    @staticmethod
    def DownloadFileRequestWithChunks(skylink, opts=None):
        return Skynet.DownloadFileRequest(skylink, opts, True)

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
