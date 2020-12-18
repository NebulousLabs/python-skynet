"""Skynet SDK tests."""

import os

from . import utils


PORTAL_URL = utils.default_portal_url()
SKYLINK = "XABvi7JtJbQSMAcDwnUnmp2FKDPjg8_tTTFP4BwMSxVdEg"


def test_make_url():
    """Test make_url."""

    assert utils.make_url(PORTAL_URL, "/") == PORTAL_URL+"/"
    assert utils.make_url(PORTAL_URL, "/skynet") == PORTAL_URL+"/skynet"
    assert utils.make_url(PORTAL_URL, "/skynet/") == PORTAL_URL+"/skynet/"

    assert utils.make_url(PORTAL_URL, "/", SKYLINK) == PORTAL_URL+"/"+SKYLINK
    assert utils.make_url(PORTAL_URL, "/skynet", SKYLINK) == \
        PORTAL_URL+"/skynet/"+SKYLINK
    assert utils.make_url(PORTAL_URL, "//skynet/", SKYLINK) == \
        PORTAL_URL+"/skynet/"+SKYLINK


def test_walk_directory():
    """Test walk_directory."""

    path = "./testdata/"

    # Quick test that normalizing removes the final slash.
    assert os.path.normpath(path) == "testdata"

    files = utils.walk_directory(path)
    expected_files = [
        "testdata/file1",
        "testdata/dir1/file2",
        "testdata/file3"
    ]
    assert len(expected_files) == len(files)
    for expected_file in expected_files:
        assert expected_file in files
