"""Upload API integration tests."""

import sys

import responses

import siaskynet as skynet


SKYLINK = "XABvi7JtJbQSMAcDwnUnmp2FKDPjg8_tTTFP4BwMSxVdEg"
SIALINK = skynet.uri_skynet_prefix() + SKYLINK

client = skynet.SkynetClient()


def response_callback(request):
    """Called by responses for HTTP requests.
       This function can perform any processing of
       requests needed for tests.
    """

    # process body content
    if hasattr(request.body, 'read'):
        # upload is a file object
        # read the file and store its content for test to compare
        request.body = request.body.read()
    elif not isinstance(request.body, (str, bytes)):
        # upload is a chunked iterator
        # convert it into the iterated content
        chunks = [*request.body]
        if len(chunks) > 0 and isinstance(chunks[0], str):
            request.body = ''.join(chunks)
        else:
            request.body = b''.join(chunks)

    # return the status code and headers for
    # the responses module to provide
    return (
        200,
        {'Content-Type': 'application/json'},
        '{"skylink": "' + SKYLINK + '"}'
    )


@responses.activate
def test_upload_file():
    """Test uploading a file."""

    src_file = "./testdata/file1"

    # upload a file

    responses.add_callback(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        callback=response_callback
    )

    print("Uploading file "+src_file)
    sialink2 = client.upload_file(src_file)
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"]
    assert headers["User-Agent"].startswith("python-requests")
    assert "Authorization" not in headers

    params = responses.calls[0].request.params
    assert params["filename"] == "file1"

    body = responses.calls[0].request.body
    with open(src_file, 'rb') as file_h:
        contents = file_h.read()
        assert contents == body

    assert len(responses.calls) == 1


@responses.activate
def test_upload_file_custom_filename():
    """Test uploading a file with a custom filename."""

    src_file = './testdata/file1'
    custom_name = 'testname'

    # upload a file with custom filename

    responses.add_callback(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        callback=response_callback
    )

    print("Uploading file "+src_file)
    sialink2 = client.upload_file(src_file, {'custom_filename': custom_name})
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    body = responses.calls[0].request.body
    with open(src_file, 'rb') as file_h:
        contents = file_h.read()
        assert body == contents

    params = responses.calls[0].request.params
    assert params["filename"] == custom_name

    assert len(responses.calls) == 1


@responses.activate
def test_upload_file_api_key():
    """Test uploading a file with authorization."""

    src_file = "./testdata/file1"

    # Upload a file with an API password set.

    responses.add_callback(
        responses.POST,
        "https://siasky.net/skynet/skyfile",
        callback=response_callback
    )

    print("Uploading file "+src_file)
    sialink2 = client.upload_file(src_file, {"api_key": "foobar"})
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
    client2 = skynet.SkynetClient(
        "https://testportal.net",
        {"custom_user_agent": "Sia-Agent"}
    )

    # Upload a file using the client's user agent.

    responses.add_callback(
        responses.POST,
        "https://testportal.net/skynet/skyfile",
        callback=response_callback
    )

    print("Uploading file "+src_file)
    sialink2 = client2.upload_file(src_file)
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["User-Agent"] == "Sia-Agent"

    # Upload a file with a new user agent set.

    responses.add_callback(
        responses.POST,
        "https://testportal.net/skynet/skyfile",
        callback=response_callback
    )

    print("Uploading file "+src_file)
    sialink2 = client2.upload_file(
        src_file,
        {"custom_user_agent": "Sia-Agent-2"}
    )
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[1].request.headers
    assert headers["User-Agent"] == "Sia-Agent-2"

    assert len(responses.calls) == 2


@responses.activate
def test_upload_directory():
    """Test uploading a directory."""

    src_dir = './testdata'

    # upload a directory

    responses.add_callback(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        callback=response_callback
    )

    print('Uploading dir '+src_dir)
    sialink2 = client.upload_directory(src_dir)
    if SIALINK != sialink2:
        sys.exit('ERROR: expected returned sialink '+SIALINK +
                 ', received '+sialink2)
    print('Dir upload successful, sialink: ' + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"].startswith("multipart/form-data;")

    params = responses.calls[0].request.params
    assert params["filename"] == "testdata"

    body = str(responses.calls[0].request.body)
    print(body)
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file1"') != -1
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file3"') != -1
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="dir1/file2"') != -1
    # Check a file that shouldn't be there.
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file0"') == -1

    assert len(responses.calls) == 1


@responses.activate
def test_upload_directory_custom_dirname():
    """Test uploading a directory with a custom dirname."""

    src_dir = './testdata'
    custom_dirname = "testdir"

    # upload a directory

    responses.add_callback(
        responses.POST,
        'https://siasky.net/skynet/skyfile?filename=testdir',
        match_querystring=True,
        callback=response_callback
    )

    print('Uploading dir '+src_dir)
    sialink2 = client.upload_directory(
        src_dir,
        {"custom_dirname": custom_dirname}
    )
    if SIALINK != sialink2:
        sys.exit('ERROR: expected returned sialink '+SIALINK +
                 ', received '+sialink2)
    print('Dir upload successful, sialink: ' + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"].startswith("multipart/form-data;")

    params = responses.calls[0].request.params
    assert params["filename"] == custom_dirname

    body = str(responses.calls[0].request.body)
    print(body)
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file1"') != -1
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file3"') != -1
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="dir1/file2"') != -1
    # Check a file that shouldn't be there.
    assert body.find('Content-Disposition: form-data; name="files[]"; \
filename="file0"') == -1

    assert len(responses.calls) == 1


@responses.activate
def test_upload_file_chunks():
    """Test uploading a file with chunks."""

    src_file = "./testdata/file1"

    # upload a file

    responses.add_callback(
        responses.POST,
        'https://siasky.net/skynet/skyfile',
        callback=response_callback
    )

    print("Uploading file "+src_file)

    def chunker(filename):
        with open(filename, 'rb') as file:
            while True:
                data = file.read(3)
                if not data:
                    break
                yield data
    chunks = chunker(src_file)
    sialink2 = client.upload_file_with_chunks(chunks,
                                              {'custom_filename': src_file})
    if SIALINK != sialink2:
        sys.exit("ERROR: expected returned sialink "+SIALINK +
                 ", received "+sialink2)
    print("File upload successful, sialink: " + sialink2)

    headers = responses.calls[0].request.headers
    assert headers["Content-Type"]
    assert headers["Transfer-Encoding"] == "chunked"
    assert headers["User-Agent"].startswith("python-requests")
    assert "Authorization" not in headers

    params = responses.calls[0].request.params
    assert params["filename"] == src_file

    body = responses.calls[0].request.body
    with open(src_file, 'rb') as file_h:
        contents = file_h.read()
        assert contents == body

    assert len(responses.calls) == 1
