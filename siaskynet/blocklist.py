"""Skynet blocklist API.
"""


from . import utils


def __default_get_blocklist_options():
    """Returns the default get blocklist options."""

    obj = utils.__default_options("/skynet/blocklist")

    return obj


def __default_update_blocklist_options():
    """Returns the default update blocklist options."""

    obj = utils.__default_options("/skynet/blocklist")

    return obj


def get_blocklist(custom_opts={}):
    """Returns the list of hashed merkleroots that are blocklisted."""

    raise NotImplementedError


def update_blocklist(additions, removals, custom_opts={}):
    """Updates the list of skylinks that should be blocklisted from Skynet. \
    This function can be used to both add and remove skylinks from the \
    blocklist."""

    raise NotImplementedError
