"""Skynet SDK tests."""

import os

from . import utils


portal_url = utils.default_portal_url()
skylink = "XABvi7JtJbQSMAcDwnUnmp2FKDPjg8_tTTFP4BwMSxVdEg"


def test_make_url():
    """Test make_url."""

    assert utils.__make_url(portal_url, "/") == portal_url+"/"
    assert utils.__make_url(portal_url, "/skynet") == portal_url+"/skynet"
    assert utils.__make_url(portal_url, "/skynet/") == portal_url+"/skynet/"

    assert utils.__make_url(portal_url, "/", skylink) == portal_url+"/"+skylink
    assert utils.__make_url(portal_url, "/skynet", skylink) == \
        portal_url+"/skynet/"+skylink
    assert utils.__make_url(portal_url, "//skynet/", skylink) == \
        portal_url+"/skynet/"+skylink


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
