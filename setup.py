import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rest_channels',
    version=get_version('rest_channels'),
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Class Based Views for Django Channels with Django Rest Framework',
    setup_requires=['setuptools-markdown'],
    install_requires=[
        'django>=1.8',
        'djangorestframework>=3.0.0',
        'channels>=0.11.0',
        'ujson>=1.35',
        'six>=1.10.0',
    ],
    long_description_markdown_filename='README.md',
    author='Khasanov Bulat',
    author_email='afti@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    url='https://github.com/KhasanovBI/rest_channels'
)
