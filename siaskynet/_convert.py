"""Skynet convert API.
"""


from . import utils


def default_convert_options():
    """Returns the default convert options."""

    obj = utils.default_options("/skynet/skyfile")

    return obj


def convert(self, src_sia_path, dest_sia_path, custom_opts=None):
    """Converts an existing siafile to a skyfile and skylink."""

    raise NotImplementedError
