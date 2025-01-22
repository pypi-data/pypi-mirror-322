#!/usr/bin/env python

import io
import os
from typing import Dict

from setuptools import setup, find_packages

current_dir = os.path.abspath(os.path.dirname(__file__))
about = {}  # type: Dict[str, str]

with open(os.path.join(current_dir, "pytiqs", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    download_url=about["__download_url__"],
    license=about["__license__"],
    packages=["pytiqs"],
    install_requires=[
        "service_identity>=18.1.0",
        "requests>=2.18.4",
        "python-dateutil>=2.6.1",
        "six>=1.11.0",
        "pyOpenSSL>=17.5.0",
        "python-dateutil>=2.6.1",
        "autobahn[twisted]==19.11.2"
    ],
    tests_require=["pytest", "responses", "pytest-cov", "mock", "flake8"],
    test_suite="tests",
    setup_requires=["pytest-runner"]
)
