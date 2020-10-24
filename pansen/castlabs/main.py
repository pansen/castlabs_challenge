import logging

from aiohttp.hdrs import METH_GET, METH_POST
from fastapi import FastAPI
from starlette.requests import Request

from pansen.castlabs.config import configure, log_config
from pansen.castlabs.lib.fastapi import as_starlette_response
from pansen.castlabs.lib.http import fetch_with_jwt_token

app = FastAPI()
log = logging.getLogger(__name__)


@app.middleware("http")
async def align_possible_testclient(request: Request, call_next):
    """
    TODO andi: testclient and real clients behave differnet in headers and `path` processing.
     We do some alignment here, to have a consistent processing down the line.
    """
    if not request.scope.get('raw_path', None) \
            and request.headers.get('user-agent', None) == 'testclient' \
            and request.scope['path'] not in [r.path for r in request.app.router.routes]:
        # this will become the `full_path` parameter later
        request.scope['path'] = f"{request.url.components.scheme}://" \
                                f"{request.url.components.netloc}{request.url.components.path}"

    return await call_next(request)


@app.middleware("http")
async def add_x_headers(request: Request, call_next):
    """
    Add some response headers to indicate our own processing.
    """
    response = await call_next(request)
    response.headers['x-pansen-processed'] = '1'
    return response


@app.get("/status")
async def root_get():
    """
    A status endpoint, to validate the service is running.
    """
    return {'status': 'OK'}


@app.get("{full_path:path}")
async def catch_all_get(request: Request, full_path: str,  # type: ignore
                        ):
    """
    The HTTP GET proxy handler to fetch a url, enriched with a JWT token.
    """
    # TODO andi: `str(request.url)` contains a double domain for some reason. Ignore for now.
    return as_starlette_response(*(await fetch_with_jwt_token(METH_GET, request, full_path)))


@app.post("{full_path:path}")
async def catch_all_post(request: Request, full_path: str,  # type: ignore
                         ):
    """
    The HTTP POST proxy handler to fetch a url, enriched with a JWT token.
    """
    # TODO andi: `str(request.url)` contains a double domain for some reason. Ignore for now.
    return as_starlette_response(*(await fetch_with_jwt_token(METH_POST, request, full_path)))


def run():
    """
    Entry-point to have the ability to perform some application start logic.
    """
    c = configure(app)
    app.extra['config'] = c

    from uvicorn.main import run

    return run('pansen.castlabs.main:app', host=c.HTTP_HOST, port=c.HTTP_PORT, log_config=log_config())
