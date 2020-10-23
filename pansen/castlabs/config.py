import os
from dataclasses import dataclass
from logging.config import dictConfig

from dotenv import load_dotenv


@dataclass
class Config:
    JWT_ALGO: str
    JWT_SECRET: str
    JWT_HEADER_NAME: str
    JWT_ISSUER: str
    HTTP_HOST: str
    HTTP_PORT: int


def configure() -> Config:
    """
    Parse the ENV and prepare a `Config` instance according to that.
    """
    load_dotenv(verbose=True)

    dictConfig(log_config())

    # int
    for k in ('HTTP_PORT',
              ):
        locals()[k] = int(os.getenv(k))
    # string
    for k in ('JWT_ALGO',
              'JWT_SECRET',
              'JWT_HEADER_NAME',
              'JWT_ISSUER',
              'HTTP_HOST',
              ):
        locals()[k] = os.getenv(k)
    # Take all local variables to the `Config` constructor, if they start uppercase
    return Config(**{key: value for (key, value) in locals().items() if key.isupper()})


def log_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stderr'
            }
        },
        'loggers': {
            'pansen': {
                'level': 'DEBUG',
                'propagate': False,
                'handlers': ['console'],
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        }
    }
