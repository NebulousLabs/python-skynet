"""Download API integration tests."""

import sys
import tempfile
import filecmp

import responses

import siaskynet as skynet


@responses.activate
def test_download_file():
    """Test downloading a file."""

    src_file = "./testdata/file1"
    skylink = 'testskylink'

    # download a file

    responses.add(
        responses.GET,
        'https://siasky.net/'+skylink,
        "test\n",
        status=200
    )

    dst_file = tempfile.NamedTemporaryFile().name
    print("Downloading to "+dst_file)
    skynet.download_file(dst_file, skylink)
    if not filecmp.cmp(src_file, dst_file):
        sys.exit("ERROR: Downloaded file at "+dst_file +
                 " did not equal uploaded file "+src_file)

    print("File download successful")

    assert len(responses.calls) == 1
