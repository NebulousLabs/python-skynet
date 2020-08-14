"""Skynet portals API.
"""


from . import utils


def default_get_portals_options():
    """Returns the default get portals options."""

    obj = utils.default_options("/skynet/portals")

    return obj


def default_update_portals_options():
    """Returns the default update portals options."""

    obj = utils.default_options("/skynet/portals")

    return obj


def get_portals(self, custom_opts=None):
    """Returns the list of known Skynet portals."""

    raise NotImplementedError


def update_portals(self, additions, removals, custom_opts=None):
    """Updates the list of known portals. This function can be used to both \
    add and remove portals from the list. Removals are provided in the form \
    of addresses."""

    raise NotImplementedError