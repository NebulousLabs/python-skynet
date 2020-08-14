"""Skynet ls API.
"""


from . import utils


def default_ls_options():
    """Returns the default ls options."""

    obj = utils.default_options("")
    obj['endpoint_path_ls_dir'] = "renter/dir"
    obj['endpoint_path_ls_file'] = "renter/file"

    return obj


def list_files(self, sia_path, custom_opts=None):
    """Returns the list of files and/or directories at the given path."""

    raise NotImplementedError
