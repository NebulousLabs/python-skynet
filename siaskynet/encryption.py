"""Skynet encryption API.
"""


from . import utils


def default_add_skykey_options():
    """Returns the default addskykey options."""
    return __fill_with_default_add_skykey_options()


def __fill_with_default_add_skykey_options(opts=None):
    """Fills in missing options with the default addskykey options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_create_skykey_options():
    """Returns the default createskykey options."""
    return __fill_with_default_create_skykey_options()


def __fill_with_default_create_skykey_options(opts=None):
    """Fills in missing options with the default createskykey options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_get_skykey_options():
    """Returns the default getskykey options."""
    return __fill_with_default_get_skykey_options()


def __fill_with_default_get_skykey_options(opts=None):
    """Fills in missing options with the default getskykey options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def default_list_skykeys_options():
    """Returns the default listskykeys options."""
    return __fill_with_default_list_skykeys_options()


def __fill_with_default_list_skykeys_options(opts=None):
    """Fills in missing options with the default listskykeys options."""
    portal_url = getattr(opts, 'portal_url', utils.default_portal_url())

    return type('obj', (object,), {
        'portal_url': portal_url,
    })


def add_skykey(skykey, opts=None):
    """Stores the given base-64 encoded skykey with the skykey manager."""

    raise NotImplementedError


def create_skykey(skykey_name, skykey_type, opts=None):
    """Returns a new skykey created and stored under the given name with \
       the given type. skykeyType can be either "public-id" or \
       "private-id"."""

    raise NotImplementedError


def get_skykey(skykey_name, skykey_id, opts=None):
    """Returns the given skykey. One of either name or id must be provided \
       -- the one that is not provided should be left blank."""

    raise NotImplementedError


def list_skykeys(opts=None):
    """Returns a list of all skykeys."""

    raise NotImplementedError
