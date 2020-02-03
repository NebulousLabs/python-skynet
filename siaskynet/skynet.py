import requests

class Skynet:
    @staticmethod
    def default_upload_options():
        return type('obj', (object,), {
            'portalUrl': 'https://siasky.net',
            'portalUploadPath' : '/api/skyfile',
            'portalFileFieldname' : 'file',
            'customFilename':''
        })

    @staticmethod
    def default_download_options():
        return type('obj', (object,), {
            'portalUrl': 'https://siasky.net',
        })

    @staticmethod
    def UploadFile(path, opts=None):
        if opts is None:
            opts = Skynet.default_upload_options()

        with open(path, 'rb') as f:
            r = requests.post("%s%s" % (opts.portalUrl, opts.portalUploadPath), files={opts.portalFileFieldname: f})
            response = r.json()
            return response["skylink"]

    @staticmethod
    def DownloadFile(path, skylink, opts=None):
        if opts is None:
            opts = Skynet.default_download_options()

        r = requests.get("%s/%s" % (opts.portalUrl, skylink),allow_redirects=True)
        open(path, 'wb').write(r.content)
