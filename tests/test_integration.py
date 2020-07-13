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
    skylink = 'testskylink'
    sialink = Skynet.uri_skynet_prefix() + skylink

    # upload a file

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = Skynet.upload_file(src_file)
    if sialink != sialink2:
        sys.exit("ERROR: expected returned sialink "+sialink +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    body = responses.calls[0].request.body
    assert str(body).find('Content-Disposition: form-data; name="file"; \
filename="file1"') != -1
    with open(src_file, 'r') as fd:
        contents = fd.read().strip()
        assert str(body).find(contents) != -1

    # download a file

    responses.add(
        responses.GET,
        'https://siasky.net/'+skylink,
        "test\n",
        status=200
    )

    dst_file = tempfile.NamedTemporaryFile().name
    print("Downloading to "+dst_file)
    Skynet.download_file(dst_file, skylink)
    if not filecmp.cmp(src_file, dst_file):
        sys.exit("ERROR: Downloaded file at "+dst_file +
                 " did not equal uploaded file "+src_file)

    print("File download successful")

    assert len(responses.calls) == 2


@responses.activate
def test_upload_file_custom_filename():
    """Test uploading a file with a custom filename."""

    src_file = './testdata/file1'
    skylink = 'testskylinkcustomname'
    sialink = Skynet.uri_skynet_prefix() + skylink

    custom_name = 'testname'
    opts = Skynet.default_upload_options()
    opts.custom_filename = custom_name

    # upload a file with custom filename

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = Skynet.upload_file(src_file, opts)
    if sialink != sialink2:
        sys.exit("ERROR: expected returned sialink "+sialink +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    body = responses.calls[0].request.body
    assert str(body).find('Content-Disposition: form-data; name="file"; \
filename="'+custom_name+'"') != -1
    with open(src_file, 'r') as fd:
        contents = fd.read().strip()
        assert str(body).find(contents) != -1

    assert len(responses.calls) == 1


@responses.activate
def test_upload_directory():
    """Test uploading a directory."""

    src_dir = './testdata'
    skylink = 'testskylink'
    sialink = Skynet.uri_skynet_prefix() + skylink

    # upload a directory

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print('Uploading dir '+src_dir)
    sialink2 = Skynet.upload_directory(src_dir)
    if sialink != sialink2:
        sys.exit('ERROR: expected returned sialink '+sialink +
                 ', received '+sialink2)
    print('Dir upload successful, sialink: ' + sialink)

    body = responses.calls[0].request.body
    assert str(body).find('Content-Disposition: form-data; name="files[]"; \
filename="file1"') != -1
    assert str(body).find('Content-Disposition: form-data; name="files[]"; \
filename="file3"') != -1
    assert str(body).find('Content-Disposition: form-data; name="files[]"; \
filename="dir1/file2"') != -1
    # Check a file that shouldn't be there.
    assert str(body).find('Content-Disposition: form-data; name="files[]"; \
filename="file0"') == -1

    assert len(responses.calls) == 1
