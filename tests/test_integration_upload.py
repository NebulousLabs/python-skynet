"""Upload API integration tests."""

import sys

import responses

import siaskynet as skynet


SKYLINK = "XABvi7JtJbQSMAcDwnUnmp2FKDPjg8_tTTFP4BwMSxVdEg"
SIALINK = skynet.uri_skynet_prefix() + SKYLINK


@responses.activate
def test_upload_file():
    """Test uploading a file."""

    src_file = "./testdata/file1"

    # upload a file

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': SKYLINK},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file)
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"].startswith("multipart/form-data;")
    assert headers["User-Agent"] == "python-requests/2.24.0"
    assert "Authorization" not in headers

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
    custom_name = 'testname'

    # upload a file with custom filename

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': SKYLINK},
        status=200
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file, {'custom_filename': custom_name})
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
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
def test_upload_file_api_key():
    """Test uploading a file with authorization."""

    src_file = "./testdata/file1"

    # Upload a file with an API password set.

    responses.add(
        responses.POST,
        "https://siasky.net/skynet/skyfile",
        json={"skylink": SKYLINK},
        status=200,
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file, {"api_key": "foobar"})
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Authorization"] == "Basic OmZvb2Jhcg=="

    assert len(responses.calls) == 1


@responses.activate
def test_upload_file_custom_user_agent():
    """Test uploading a file with authorization."""

    src_file = "./testdata/file1"

    # Upload a file with an API password set.

    responses.add(
        responses.POST,
        "https://siasky.net/skynet/skyfile",
        json={"skylink": SKYLINK},
        status=200,
    )

    print("Uploading file "+src_file)
    sialink2 = skynet.upload_file(src_file, {"custom_user_agent": "Sia-Agent"})
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    print(headers)
    assert headers["User-Agent"] == "Sia-Agent"

    assert len(responses.calls) == 1


@responses.activate
def test_upload_directory():
    """Test uploading a directory."""

    src_dir = './testdata'

    # upload a directory

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        json={'skylink': SKYLINK},
        status=200
    )

    print('Uploading dir '+src_dir)
    sialink2 = skynet.upload_directory(src_dir)
    if SIALINK != sialink2:
        sys.exit('ERROR: expected returned sialink '+SIALINK +
                 ', received '+sialink2)
    print('Dir upload successful, sialink: ' + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"].startswith("multipart/form-data;")

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


@responses.activate
def test_upload_directory_custom_dirname():
    """Test uploading a directory with a custom dirname."""

    src_dir = './testdata'
    custom_dirname = "testdir"

    # upload a directory

    responses.add(
        responses.POST,
        'https://siasky.net/skynet/skyfile?filename=testdir',
        match_querystring=True,
        json={'skylink': SKYLINK},
        status=200
    )

    print('Uploading dir '+src_dir)
    sialink2 = skynet.upload_directory(
        src_dir,
        {"custom_dirname": custom_dirname}
    )
    if SIALINK != sialink2:
        sys.exit('ERROR: expected returned sialink '+SIALINK +
                 ', received '+sialink2)
    print('Dir upload successful, sialink: ' + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"].startswith("multipart/form-data;")

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
