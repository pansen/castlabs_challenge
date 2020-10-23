import os

from setuptools import find_namespace_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION')) as f:
    VERSION = f.read().strip()

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'bcrypt',
    'fastapi',
    'uvicorn',
    'passlib',
    'python-dotenv',

    'pyjwt',
    'cryptography',

    # http client stuff
    # see: https://docs.aiohttp.org/en/v2.3.4/
    'aiohttp',
    'cchardet',
    'aiodns',
    # another one
    'httpx',
]

standalone_require = [
]

tests_require = [
    'mypy>=0.760',
    'pytest',
    'requests',
    'vcrpy',
]


setup(name='pansen-castlabs',
      version=VERSION,
      description='castlabs challenge',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Framework :: FastAPI",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: ASGI :: Application"
      ],
      keywords="web services",
      author='pansen',
      author_email='andi@zerotired.com',
      url='',
      packages=find_namespace_packages(include=['pansen.*']),
      include_package_data=True,
      # http://pythonhosted.org/distribute/setuptools.html#namespace-packages
      namespace_packages=['pansen'],
      zip_safe=False,
      extras_require={
          'testing': tests_require + standalone_require,
          'standalone': standalone_require,
      },
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'pansen_castlabs = pansen.castlabs.main:run'
          ],
      },
      )
