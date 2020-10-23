import logging
from datetime import datetime
from urllib import parse
from uuid import uuid4

import async_timeout
import jwt
from aiohttp import ClientResponse, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST
from starlette.requests import Request

from pansen.castlabs.config import Config

HTTP_SUBREQUEST_TIMEOUT = 10
HTTP_ALLOWED_METHODS = (METH_POST, METH_GET,)

log = logging.getLogger(__name__)


async def fetch_with_jwt_token(method: str, request: Request, url_to_proxy: str) -> (
ClientResponse, bytes):
    """
    Async HTTP *x* a url.
    """
    if not method in HTTP_ALLOWED_METHODS:
        raise NotImplementedError(f"Method {method} is not allowed.")
    log.debug('%s %s', method.upper(), url_to_proxy)
    c: Config = request.app.extra['config']

    if method == METH_POST:
        # It looks like there is no way to pass a stream directly
        # `aiohttp.client_reqrep.ClientRequest.update_body_from_data`
        # TODO andi: there IS a streamable HTTP client:
        #  https://gist.github.com/tomchristie/5765e10a90a41c7e57470e2dc700f9db#file-proxy-py-L14-L25
        body = b''
        async for chunk in request.stream():
            body += chunk
    else:
        body = None

    if request.query_params:
        url_to_proxy = f"{url_to_proxy}?{str(request.query_params)}"

    parsed_url = parse.urlparse(url_to_proxy)
    jwt_token = _token(c)

    async with ClientSession() as session:
        with async_timeout.timeout(HTTP_SUBREQUEST_TIMEOUT):
            if method == METH_POST:
                func = session.post
            elif method == METH_GET:
                func = session.get

            async with func(url_to_proxy, data=body, headers={
                **request.headers,
                **{
                    c.JWT_HEADER_NAME: f"Bearer {jwt_token}",
                    'host': parsed_url.netloc,
                },
            }) as response:
                _body = await response.read()
                return response, _body


def _token(c: Config):
    utcnow = datetime.utcnow()
    return jwt.encode({
        'iat': utcnow,
        'iss': c.JWT_ISSUER,
        'jti': f"{c.JWT_ISSUER}:{uuid4()}",
        'payload': {
            'user': 'ronny',
            'date': utcnow.strftime('%Y-%m-%d')
        },
    },
        c.JWT_SECRET,
        algorithm=c.JWT_ALGO
    ).decode('utf-8')
