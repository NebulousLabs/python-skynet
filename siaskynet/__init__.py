"""An SDK for integrating Skynet into Python applications.
"""


import requests

from . import utils
from .utils import default_portal_url, uri_skynet_prefix


# pylint: disable=too-few-public-methods
class SkynetClient():
    """The Skynet Client which can be used to access Skynet."""

    # Imported methods

    # pylint: disable=import-outside-toplevel
    from ._download import (
        download_file, download_file_request, get_metadata,
        get_metadata_request
    )
    from ._encryption import (
        add_skykey, create_skykey, get_skykey_by_id, get_skykey_by_name,
        get_skykeys
    )
    from ._upload import (
        upload, upload_request,
        upload_file, upload_file_request,
        upload_file_with_chunks, upload_file_request_with_chunks,
        upload_directory, upload_directory_request
    )
    # pylint: enable=import-outside-toplevel

    def __init__(self, portal_url="", custom_opts=None):
        if portal_url == "":
            portal_url = utils.default_portal_url()
        self.portal_url = portal_url
        if custom_opts is None:
            custom_opts = {}
        self.custom_opts = custom_opts

    def execute_request(self, method, opts, **kwargs):
        """Makes and executes a request with the given options."""

        url = utils.make_url(
            self.portal_url,
            opts["endpoint_path"],
            opts.get("extra_path", "")
        )

        if opts["api_key"] is not None:
            kwargs["auth"] = ("", opts["api_key"])

        if opts["custom_user_agent"] is not None:
            headers = kwargs.get("headers", {})
            headers["User-Agent"] = opts["custom_user_agent"]
            kwargs["headers"] = headers

        if opts["timeout_seconds"] is not None:
            kwargs["timeout"] = opts["timeout_seconds"]

        try:
            return requests.request(method, url, **kwargs)
        except requests.exceptions.Timeout as err:
            raise TimeoutError("Request timed out") from err

# pylint: enable=too-few-public-methods
