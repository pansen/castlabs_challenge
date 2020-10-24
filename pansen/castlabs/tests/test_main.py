import os

import jwt
import pytest
from jwt import InvalidAlgorithmError, InvalidSignatureError
from starlette.testclient import TestClient
from vcr.request import Request

from pansen.castlabs.config import Config, configure
from pansen.castlabs.conftest import cast_vcr
from pansen.castlabs.lib.http import _token
from pansen.castlabs.main import app


def test_get_status(test_client: TestClient):
    res = test_client.get('/status')
    assert 200 == res.status_code
    assert {'status': 'OK'} == res.json()


# @pytest.mark.skip('Only for testing locally, not part of the requirements')
@cast_vcr.use_cassette
def test_get_response(test_client: TestClient, config: Config):
    res = test_client.get('http://httpbin.org/get?a=1&b=3')
    assert 200 == res.status_code
    assert 'x-pansen-processed' in res.headers


@cast_vcr.use_cassette
def test_post_response(test_client: TestClient, config: Config):
    url = 'http://httpbin.org/post?a=1&b=2'
    post_data = b'abc'

    res = test_client.post(url, data=post_data)
    assert 200 == res.status_code
    assert 'x-pansen-processed' in res.headers


def test_post_subrequest(test_client: TestClient, config: Config):
    url = 'http://httpbin.org/post?a=1&b=2'
    post_data = b'abc'

    with cast_vcr.use_cassette('test_post_subrequest.yaml') as cassette:
        res = test_client.post(url, data=post_data)

        request: Request = cassette.requests[0]
        assert config.JWT_HEADER_NAME in request.headers
        assert 'httpbin.org' in request.headers['host']
        assert url == request.url
        assert post_data == request.body


def test_token_success():
    os.environ['JWT_HEADER_NAME'] = 'x-foo'
    os.environ['JWT_ISSUER'] = 'testing-issuer'
    os.environ['JWT_SECRET'] = 'abc'
    c = configure(app)
    token = _token(c)
    decoded = jwt.decode(token, c.JWT_SECRET, algorithms=[c.JWT_ALGO, ])
    assert decoded['jti'].startswith(f"{c.JWT_ISSUER}:")
    assert c.JWT_ISSUER == decoded['iss']
    assert all([k in decoded['payload'] for k in ('user', 'date',)])


def test_token_fail():
    os.environ['JWT_HEADER_NAME'] = 'x-foo'
    os.environ['JWT_ISSUER'] = 'testing-issuer'
    os.environ['JWT_SECRET'] = 'abc'
    c = configure(app)
    token = _token(c)

    try:
        jwt.decode(token, 'wrong', algorithms=[c.JWT_ALGO, ])
    except Exception as e:
        assert isinstance(e, InvalidSignatureError)

    try:
        decoded = jwt.decode(token, c.JWT_SECRET, algorithms=['None', ])
    except Exception as e:
        assert isinstance(e, InvalidAlgorithmError)
