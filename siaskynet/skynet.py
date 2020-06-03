import json
import os
import string

import requests


class Skynet:

    @staticmethod
    def uri_skynet_prefix():
        return "sia://"

    @staticmethod
    def fill_with_default_options(opts):
        try:
            portal_url = opts.portal_url
        except:
            portal_url = 'https://siasky.net'
            
        try:
            portal_upload_path = opts.portal_upload_path
        except:
            portal_upload_path = 'skynet/skyfile'
            
        try:
            portal_file_fieldname = opts.portal_file_fieldname
        except:
            portal_file_fieldname = 'file'
            
        try:
            portal_directory_file_fieldname = opts.portal_directory_file_fieldname
        except:
            portal_directory_file_fieldname = 'files[]'
            
        try:
            custom_filename = opts.custom_filename
        except:
            custom_filename = ''
            
        try:
            timeout = opts.timeout
        except:
            timeout = None
            
        return type('obj', (object,), {
            'portal_url': portal_url,
            'portal_upload_path': portal_upload_path,
            'portal_file_fieldname': portal_file_fieldname,
            'portal_directory_file_fieldname': portal_directory_file_fieldname,
            'custom_filename': custom_filename,
            'timeout': timeout
        })

    @staticmethod
    def fill_with_default_download_options(opts):
        try:
            portal_url = opts.portal_url
        except:
            portal_url = 'https://siasky.net'

        return type('obj', (object,), {
            'portal_url': portal_url,
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
        opts = Skynet.fill_with_default_options(opts)

        with open(path, 'rb') as f:
            host = opts.portal_url
            path = opts.portal_upload_path
            url = f'{host}/{path}'
            try:
                return requests.post(url, files={opts.portal_file_fieldname: f}, timeout=opts.timeout)
            except requests.exceptions.Timeout:
                raise TimeoutError('Request timed out')

    @staticmethod
    def upload_file_request_with_chunks(path, opts=None):
        opts = Skynet.fill_with_default_options(opts)

        filename = opts.custom_filename if opts.custom_filename else path
        try:
            return requests.post("%s/%s?filename=%s" % (opts.portal_url, opts.portal_upload_path, filename),
                                     data=path, headers={'Content-Type': 'application/octet-stream'}, timeout=opts.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

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

        opts = Skynet.fill_with_default_options(opts)

        ftuples = []
        files = list(Skynet.walk_directory(path).keys())
        for file in files:
            ftuples.append((opts.portal_directory_file_fieldname,
                            (file, open(file, 'rb'))))

        filename = opts.custom_filename if opts.custom_filename else path

        host = opts.portal_url
        path = opts.portal_upload_path
        url = f'{host}/{path}?filename={filename}'
        try:
            return requests.post(url, files=ftuples, timeout=opts.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

    @staticmethod
    def download_file(path, skylink, opts=None):
        r = Skynet.download_file_request(skylink, opts)
        open(path, 'wb').write(r.content)
        r.close()

    @staticmethod
    def download_file_request(skylink, opts=None, stream=False):
        opts = Skynet.fill_with_default_download_options(opts)

        portal = opts.portal_url
        skylink = Skynet.strip_prefix(skylink)
        url = f'{portal}/{skylink}'
        try:
            return requests.get(url, allow_redirects=True, stream=stream, timeout=opts.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

    @staticmethod
    def metadata(skylink, opts=None):
        r = Skynet.metadata_request(skylink, opts)
        return json.loads(r.headers["skynet-file-metadata"])

    @staticmethod
    def metadata_request(skylink, opts=None, stream=False):
        opts = Skynet.fill_with_default_download_options(opts)

        portal = opts.portal_url
        skylink = Skynet.strip_prefix(skylink)
        url = f'{portal}/{skylink}'
        
        try:
            return requests.head(url, allow_redirects=True, stream=stream, timeout=opts.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutError('Request timed out')

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
