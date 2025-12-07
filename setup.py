"""
Package manager for analytics_framework
"""

import os
from setuptools import find_packages, setup

# Read version from environment variable with fallback
#this is for if the workflow fails to pass the version
RELEASE_VERSION = os.getenv("RELEASE_VERSION", "2.0.0")

setup(
    name="analytics_framework",
    version=RELEASE_VERSION,
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
