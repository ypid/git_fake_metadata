#!/usr/bin/env python3

import re
from setuptools import setup, find_packages

__version__ = None
__license__ = None
__author__ = None
exec(open('git_fake_metadata/_meta.py').read())
author = re.search(r'^(?P<name>[^<]+) <(?P<email>.*)>$', __author__)

# https://docs.python.org/3/distutils/apiref.html#distutils.core.setup
# https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(
    name='git_fake_metadata',
    version=__version__,
    description='Machine readable metadata about the DebOps Project',
    long_description=open('README.rst').read(),
    author=author.group('name'),
    author_email=author.group('email'),
    # Basically redundant but when not specified `./setup.py --maintainer` will
    # return "UNKNOWN".
    maintainer=author.group('name'),
    maintainer_email=author.group('email'),
    license=__license__,
    keywords="git fake metadata privacy",
    url='https://github.com/ypid/git_fake_metadata',
    packages=find_packages(),
    package_data={'git_fake_metadata': ['data/*']},
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: DFSG approved'
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Version Control',
    ),
)
