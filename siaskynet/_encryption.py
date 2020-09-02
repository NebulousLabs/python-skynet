"""Skynet encryption API.
"""


from . import utils


def default_add_skykey_options():
    """Returns the default addskykey options."""

    obj = utils.default_options("/skynet/addskykey")

    return obj


def default_create_skykey_options():
    """Returns the default createskykey options."""

    obj = utils.default_options("/skynet/createskykey")

    return obj


def default_get_skykey_options():
    """Returns the default getskykey options."""

    obj = utils.default_options("/skynet/skykey")

    return obj


def default_get_skykeys_options():
    """Returns the default getskykeys options."""

    obj = utils.default_options("/skynet/skykeys")

    return obj


def add_skykey(self, skykey, custom_opts=None):
    """Stores the given base-64 encoded skykey with the skykey manager."""

    raise NotImplementedError


def create_skykey(self, skykey_name, skykey_type, custom_opts=None):
    """Returns a new skykey created and stored under the given name with \
       the given type. skykeyType can be either "public-id" or \
       "private-id"."""

    raise NotImplementedError


def get_skykey_by_name(self, skykey_name, custom_opts=None):
    """Returns the given skykey by name."""

    raise NotImplementedError


def get_skykey_by_id(self, skykey_id, custom_opts=None):
    """Returns the given skykey by id."""

    raise NotImplementedError


def get_skykeys(self, custom_opts=None):
    """Returns a get of all skykeys."""

    raise NotImplementedError
