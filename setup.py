#!/usr/bin/env python

"""The setup script."""

import os

from setuptools import find_packages, setup

from pymlb_statsapi import __author__, __email__, __version__


def load_requirements(file_name="requirements.txt"):
    """Load requirements from a requirements.txt file."""
    requirements = []
    if os.path.exists(file_name):
        with open(file_name) as req_file:
            requirements = [
                line.strip()
                for line in req_file.readlines()
                if line.strip() and not line.startswith("#")
            ]
    return requirements


# Use Pipfile for dependencies if available
install_requires = load_requirements("requirements.txt")

setup(
    name="pymlb_statsapi",
    author=__author__,
    author_email=__email__,
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    description="This project generates an endpoint.event interface based on the MLB StatsAPI model",
    install_requires=install_requires,
    license="Apache Software License 2.0",
    include_package_data=True,
    keywords="pymlb_statsapi",
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest>=3", "mock~=4.0.3"],
    url="https://github.com/power-edge/pymlb_statsapi",
    version=__version__,
    zip_safe=False,
    packages=find_packages(),
    # package_data={"configs": [
    #     'configs/statsapi/**',
    #     "configs/endpoint-model.yaml"
    # ]},
    # package_dir={"": "."},
)
