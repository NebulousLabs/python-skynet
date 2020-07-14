"""Skynet portals API.
"""


from . import utils


def default_get_portals_options():
    """Returns the default get portals options."""

    return __fill_with_default_get_portals_options()


def __fill_with_default_get_portals_options(opts=None):
    """Fills in missing options with the default get portals options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_update_portals_options():
    """Returns the default update portals options."""

    return __fill_with_default_get_portals_options()


def __fill_with_default_update_portals_options(opts=None):
    """Fills in missing options with the default update portals options."""

    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def get_portals(opts=None):
    """Returns the list of hashed merkleroots that are portalsed."""

    raise NotImplementedError


def update_portals(additions, removals, opts=None):
    """Updates the list of skylinks that should be portalsed from Skynet. \
    This endpoint can be used to both add and remove skylinks from the \
    portals."""

    raise NotImplementedError
