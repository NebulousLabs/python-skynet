"""Skynet stats API.
"""


from . import utils


def __default_get_stats_options():
    """Returns the default stats options."""

    obj = utils.__default_options("/skynet/stats")

    return obj


def get_stats(custom_opts={}):
    """Returns statistical information about Skynet, e.g. number of files \
    uploaded."""

    raise NotImplementedError
