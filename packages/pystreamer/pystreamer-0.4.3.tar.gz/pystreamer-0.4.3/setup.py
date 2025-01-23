from io import open
from os import path

from setuptools import find_packages, setup

VERSION = "0.4.3"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pystreamer",
    version=VERSION,
    description="A lazy evaluating, memory friendly, chainable stream solution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arnoldosmium/pystreamer",
    download_url="https://pypi.org/project/pyStreamer/",
    author="Arnold Y. Lin",
    author_email="contact@arnoldlin.tech",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="stream generator chain",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "test"]),
    install_requires=[],
    extras_require={
        "test": ["pytest"],
    },
)
