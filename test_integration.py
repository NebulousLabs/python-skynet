"""API integration tests."""

import filecmp
import sys
import tempfile

import responses

from siaskynet import Skynet


@responses.activate
def test_upload_and_download_file():
    """Test uploading and download a file."""
    src_file = "./testdata/file1"

    # upload a file

    skylink = Skynet.uri_skynet_prefix() + 'testskylink'

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': 'testskylink'},
        status=200
    )

    print("Uploading file "+src_file)
    skylink2 = Skynet.upload_file(src_file)
    if skylink != skylink2:
        sys.exit("ERROR: expected returned skylink "+skylink +
                 ", received "+skylink2)
    print("File upload successful, skylink: " + skylink2)

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
    if not filecmp.cmp(src_file, dst_file):
        sys.exit("ERROR: Downloaded file at "+dst_file +
                 " did not equal uploaded file "+src_file)

    print("File download successful")


@responses.activate
def test_upload_directory():
    """Test uploading a directory."""
    src_dir = "./testdata"

    # upload a directory

    skylink = Skynet.uri_skynet_prefix() + 'testskylink'

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': 'testskylink'},
        status=200
    )

    print("Uploading dir "+src_dir)
    skylink2 = Skynet.upload_directory(src_dir)
    if skylink != skylink2:
        sys.exit("ERROR: expected returned skylink "+skylink +
                 ", received "+skylink2)
    print("Dir upload successful, skylink: " + skylink)
