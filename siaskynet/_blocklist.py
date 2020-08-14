"""Skynet blocklist API.
"""


from . import utils


def default_get_blocklist_options():
    """Returns the default get blocklist options."""

    obj = utils.default_options("/skynet/blocklist")

    return obj


def default_update_blocklist_options():
    """Returns the default update blocklist options."""

    obj = utils.default_options("/skynet/blocklist")

    return obj


def get_blocklist(self, custom_opts=None):
    """Returns the list of hashed merkleroots that are blocklisted."""

    raise NotImplementedError


def update_blocklist(self, additions, removals, custom_opts=None):
    """Updates the list of skylinks that should be blocklisted from Skynet. \
    This function can be used to both add and remove skylinks from the \
    blocklist."""

    raise NotImplementedError
