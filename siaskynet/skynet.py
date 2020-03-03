import random
import string

import requests


class Skynet:
    @staticmethod
    def default_upload_options():
        return type('obj', (object,), {
            'portalUrl': 'https://siasky.net',
            'portalUploadPath' : 'skynet/skyfile',
            'portalFileFieldname' : 'file',
            'customFilename':''
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
            r = requests.post("%s/%s/%s" % (opts.portalUrl, opts.portalUploadPath, uuid), files={opts.portalFileFieldname: f})
            return r

    @staticmethod
    def DownloadFile(path, skylink, opts=None):
        r = Skynet.DownloadFileRequest(skylink, opts)
        open(path, 'wb').write(r.content)

    @staticmethod
    def DownloadFileRequest(skylink, opts=None):
        if opts is None:
            opts = Skynet.default_download_options()

        r = requests.get("%s/%s" % (opts.portalUrl, Skynet.strip_prefix(skylink)),allow_redirects=True)
        return r
