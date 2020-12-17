"""Download API integration tests."""

import filecmp
import os
import platform
import sys
import tempfile

import responses

import siaskynet as skynet


SKYLINK = "XABvi7JtJbQSMAcDwnUnmp2FKDPjg8_tTTFP4BwMSxVdEg"

client = skynet.SkynetClient()


@responses.activate
def test_download_file():
    """Test downloading a file to a temporary location."""

    # This test fails on CI for Windows so skip it.
    if platform.system() == "Windows" and 'CI' in os.environ:
        return

    src_file = "./testdata/file1"

    # download a file

    responses.add(
        responses.GET,
        'https://siasky.net/'+SKYLINK,
        "test\n",
        status=200
    )

    dst_file = tempfile.NamedTemporaryFile().name
    print("Downloading to "+dst_file)
    client.download_file(dst_file, SKYLINK)
    if not filecmp.cmp(src_file, dst_file):
        sys.exit("ERROR: Downloaded file at "+dst_file +
                 " did not equal uploaded file "+src_file)

    print("File download successful")

    assert len(responses.calls) == 1
