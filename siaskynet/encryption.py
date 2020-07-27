"""Skynet encryption API.
"""


from . import utils


def __default_add_skykey_options():
    """Returns the default addskykey options."""

    obj = utils.__default_options("/skynet/addskykey")

    return obj


def __default_create_skykey_options():
    """Returns the default createskykey options."""

    obj = utils.__default_options("/skynet/createskykey")

    return obj


def __default_get_skykey_options():
    """Returns the default getskykey options."""

    obj = utils.__default_options("/skynet/skykey")

    return obj


def __default_get_skykeys_options():
    """Returns the default getskykeys options."""

    obj = utils.__default_options("/skynet/skykeys")

    return obj


def add_skykey(skykey, custom_opts={}):
    """Stores the given base-64 encoded skykey with the skykey manager."""

    raise NotImplementedError


def create_skykey(skykey_name, skykey_type, custom_opts={}):
    """Returns a new skykey created and stored under the given name with \
       the given type. skykeyType can be either "public-id" or \
       "private-id"."""

    raise NotImplementedError


def get_skykey_by_name(skykey_name, custom_opts={}):
    """Returns the given skykey by name."""

    raise NotImplementedError


def get_skykey_by_id(skykey_id, custom_opts={}):
    """Returns the given skykey by id."""

    raise NotImplementedError


def get_skykeys(custom_opts={}):
    """Returns a get of all skykeys."""

    raise NotImplementedError
