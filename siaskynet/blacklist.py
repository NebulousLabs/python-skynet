"""Skynet blacklist API.
"""


from . import utils


def default_get_blacklist_options():
    """Returns the default get blacklist options."""

    return __fill_with_default_get_blacklist_options()


def __fill_with_default_get_blacklist_options(opts=None):
    """Fills in missing options with the default get blacklist options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_update_blacklist_options():
    """Returns the default update blacklist options."""

    return __fill_with_default_get_blacklist_options()


def __fill_with_default_update_blacklist_options(opts=None):
    """Fills in missing options with the default update blacklist options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def get_blacklist(opts=None):
    """Returns the list of hashed merkleroots that are blacklisted."""

    raise NotImplementedError


def update_blacklist(additions, removals, opts=None):
    """Updates the list of skylinks that should be blacklisted from Skynet. \
    This endpoint can be used to both add and remove skylinks from the \
    blacklist."""

    raise NotImplementedError
