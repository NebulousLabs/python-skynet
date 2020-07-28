"""Skynet SDK tests."""

import os

from . import utils


def test_walk_directory():
    """Test walk_directory."""

    path = "./testdata/"

    # Quick test that normalizing removes the final slash.
    assert os.path.normpath(path) == "testdata"

    files = utils.__walk_directory(path)
    expected_files = ["testdata/file1",
                      "testdata/dir1/file2",
                      "testdata/file3"]
    assert len(expected_files) == len(files)
    for expected_file in expected_files:
        assert expected_file in files
