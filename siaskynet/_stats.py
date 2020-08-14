"""Skynet stats API.
"""


from . import utils


def default_get_stats_options():
    """Returns the default stats options."""

    obj = utils.default_options("/skynet/stats")

    return obj


def get_stats(self, custom_opts=None):
    """Returns statistical information about Skynet, e.g. number of files \
    uploaded."""

    raise NotImplementedError
