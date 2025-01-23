from setuptools import setup, find_packages
import os
import sys

CURRENT_PY = sys.version_info[:2]
REQ_PY = (3, 10)

if CURRENT_PY < REQ_PY:
    sys.stderr.write(
        f""" 
=============================================
        Unsupported python verion
============================================
Your python version is {CURRENT_PY}, but supported version is {REQ_PY}+
Please install newest version of Python and try again.
"""
    )


def readme():
    with open("README.md",'r') as f:
        return f.read()
    
    
requires = [
    "requests>=2.25.1"
]


classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries"
    ]


setup(
    name="pycheckoapi",
    version="0.2.170125",
    author="io451",
    author_email="prvtangl@gmail.com",
    description="Full implementation of checko.ru API functions in Python",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/io451/pycheckoapi",
    packages=find_packages(),
    install_requires=requires,
    classifiers=classifiers,
    keywords="osint",
    python_requires=">=3.10"
)

