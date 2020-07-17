"""Skynet blocklist API.
"""


from . import utils


def default_get_blocklist_options():
    """Returns the default get blocklist options."""

    return __fill_with_default_get_blocklist_options()


def __fill_with_default_get_blocklist_options(opts=None):
    """Fills in missing options with the default get blocklist options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_update_blocklist_options():
    """Returns the default update blocklist options."""

    return __fill_with_default_get_blocklist_options()


def __fill_with_default_update_blocklist_options(opts=None):
    """Fills in missing options with the default update blocklist options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def get_blocklist(opts=None):
    """Returns the list of hashed merkleroots that are blocklisted."""

    raise NotImplementedError


def update_blocklist(additions, removals, opts=None):
    """Updates the list of skylinks that should be blocklisted from Skynet. \
    This function can be used to both add and remove skylinks from the \
    blocklist."""

    raise NotImplementedError
