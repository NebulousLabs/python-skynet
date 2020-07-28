"""Skynet convert API.
"""


from . import utils


def __default_convert_options():
    """Returns the default convert options."""

    obj = utils.__default_options("/skynet/skyfile")

    return obj


def convert(src_sia_path, dest_sia_path, custom_opts={}):
    """Converts an existing siafile to a skyfile and skylink."""

    raise NotImplementedError
