"""
Package manager for analytics_framework
"""
# -*- coding: utf-8 -*-
# patch fix (needs a proper fix)

from setuptools import find_packages, setup

setup(
    name="analytics_framework",
    version="2.0.0",
    author="sayantikabanik",
    description="Design first open source data management toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DataJourneyHQ/DataJourney",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
    license="Apache-2.0"
)
