"""Skynet download API.
"""

import json
import os

from . import utils


def default_download_options():
    """Returns the default download options."""

    obj = utils.default_options("/")

    return obj


def download_file(self, path, skylink, custom_opts=None):
    """Downloads file to path from given skylink with the given options."""

    path = os.path.normpath(path)
    response = self.download_file_request(skylink, custom_opts)
    open(path, 'wb').write(response.content)
    response.close()


def download_file_request(self, skylink, custom_opts=None, stream=False):
    """Posts request to download file."""

    opts = default_download_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    skylink = utils.strip_prefix(skylink)
    opts["extra_path"] = skylink

    return self.execute_request(
        "GET",
        opts,
        allow_redirects=True,
        stream=stream,
    )


def get_metadata(self, skylink, custom_opts=None):
    """Downloads metadata from given skylink."""

    response = self.get_metadata_request(skylink, custom_opts)
    return json.loads(response.headers["skynet-file-metadata"])


def get_metadata_request(self, skylink, custom_opts=None, stream=False):
    """Posts request to get metadata from given skylink."""

    opts = default_download_options()
    opts.update(self.custom_opts)
    if custom_opts is not None:
        opts.update(custom_opts)

    skylink = utils.strip_prefix(skylink)

    return self.execute_request(
        "HEAD",
        opts,
        allow_redirects=True,
        stream=stream,
    )
