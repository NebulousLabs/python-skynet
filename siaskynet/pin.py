"""Skynet pin API.
"""


from . import utils


def __default_pin_options():
    """Returns the default pin options."""

    obj = utils.__default_options("/skynet/pin")

    return obj


def __default_unpin_options():
    """Returns the default unpin options."""

    obj = utils.__default_options("")
    obj['endpoint_path_unpin_dir'] = "/renter/dir"
    obj['endpoint_path_unpin_file'] = "/renter/delete"

    return obj


def pin(skylink, dest_sia_path, custom_opts={}):
    """Pins the file associated with this skylink by re-uploading an exact \
    copy."""

    raise NotImplementedError


def unpin(sia_path, custom_opts={}):
    """Unpins the pinned skyfile or directory at the given siapath."""

    raise NotImplementedError
