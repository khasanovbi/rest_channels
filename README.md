[![PyPI version](https://badge.fury.io/py/rest_channels.svg)](https://badge.fury.io/py/rest_channels) [![Build Status](https://travis-ci.org/KhasanovBI/rest_channels.svg?branch=master)](https://travis-ci.org/KhasanovBI/rest_channels) [![Coverage Status](https://coveralls.io/repos/github/KhasanovBI/rest_channels/badge.svg?branch=master)](https://coveralls.io/github/KhasanovBI/rest_channels?branch=master)

[![Documentation Status](http://readthedocs.org/projects/rest-channels/badge/?version=latest)](http://rest-channels.readthedocs.io/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/l/rest_channels.svg)](https://pypi.python.org/pypi/rest_channels)

# REST channels

`django-channels` with `django-rest-framework` under the same roof.

# Installation
The easiest way to install the latest version is by using `pip/easy_install` to pull it from PyPI:

    pip install rest_channels

Add `'rest_channels'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'rest_channels',
    )

You may also use Git to clone the repository from Github and install it
manually:

    git clone https://github.com/KhasanovBI/rest_channels
    python setup.py install

## License

The BSD License

Contributed by `Bulat Khasanov`
