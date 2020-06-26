"""API integration tests."""

import filecmp
import sys
import tempfile

import responses

from siaskynet import Skynet

SRC_FILE = "./testdata/file1"
SRC_DIR = "./testdata"


@responses.activate
def test_upload_and_download_file():
    """Test uploading and download a file."""
    # upload a file

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': 'testskylink'},
        status=200
    )

    print("Uploading file "+SRC_FILE)
    skylink = Skynet.upload_file(SRC_FILE)
    print("File upload successful, skylink: " + skylink)

    # download a file

    responses.add(
        responses.GET,
        'https://siasky.net/testskylink',
        "test\n",
        status=200
    )

    dst_file = tempfile.NamedTemporaryFile().name
    print("Downloading to "+dst_file)
    skylink = skylink[len(Skynet.uri_skynet_prefix()):]
    Skynet.download_file(dst_file, skylink)
    if not filecmp.cmp(SRC_FILE, dst_file):
        sys.exit("ERROR: Downloaded file at "+dst_file +
                 " did not equal uploaded file "+SRC_FILE)

    print("File download successful")


@responses.activate
def test_upload_directory():
    """Test uploading a directory."""
    # upload a directory

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': 'testskylink'},
        status=200
    )

    print("Uploading dir "+SRC_DIR)
    skylink = Skynet.upload_directory(SRC_DIR)
    print("Dir upload successful, skylink: " + skylink)
