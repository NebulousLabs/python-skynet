"""Skynet portals API.
"""


from . import utils


def __default_get_portals_options():
    """Returns the default get portals options."""

    obj = utils.__default_options("/skynet/portals")

    return obj


def __default_update_portals_options():
    """Returns the default update portals options."""

    obj = utils.__default_options("/skynet/portals")

    return obj


def get_portals(custom_opts={}):
    """Returns the list of hashed merkleroots that are portalsed."""

    raise NotImplementedError


def update_portals(additions, removals, custom_opts={}):
    """Updates the list of skylinks that should be portalsed from Skynet. \
    This endpoint can be used to both add and remove skylinks from the \
    portals."""

    raise NotImplementedError
