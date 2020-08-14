"""Skynet ls API.
"""


from . import utils


def default_list_files_options():
    """Returns the default list files options."""

    obj = utils.default_options("")
    obj['endpoint_path_list_files_dir'] = "renter/dir"
    obj['endpoint_path_list_files_file'] = "renter/file"

    return obj


def list_files(self, sia_path, custom_opts=None):
    """Returns the list of files and/or directories at the given path."""

    raise NotImplementedError
