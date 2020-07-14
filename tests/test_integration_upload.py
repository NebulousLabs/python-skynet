"""Upload API integration tests."""

import sys

import responses

import siaskynet as skynet


@responses.activate
def test_upload_file():
    """Test uploading a file."""

    src_file = "./testdata/file1"
    skylink = 'testskylink'
    sialink = skynet.uri_skynet_prefix() + skylink

    # upload a file

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file)
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

    assert len(responses.calls) == 1


@responses.activate
def test_upload_file_custom_filename():
    """Test uploading a file with a custom filename."""

    src_file = './testdata/file1'
    skylink = 'testskylinkcustomname'
    sialink = skynet.uri_skynet_prefix() + skylink

    custom_name = 'testname'
    opts = skynet.default_upload_options()
    opts.custom_filename = custom_name

    # upload a file with custom filename

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file, opts)
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
    sialink = skynet.uri_skynet_prefix() + skylink

    # upload a directory

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': skylink},
        status=200
    )

    print('Uploading dir '+src_dir)
    sialink2 = skynet.upload_directory(src_dir)
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
