# -*- coding: utf-8 -*-
######################################################
#     _____                  _____      _     _      #
#    (____ \       _        |  ___)    (_)   | |     #
#     _   \ \ ____| |_  ____| | ___ ___ _  _ | |     #
#    | |  | )/ _  |  _)/ _  | |(_  / __) |/ || |     #
#    | |__/ ( ( | | | ( ( | | |__| | | | ( (_| |     #
#    |_____/ \_||_|___)\_||_|_____/|_| |_|\____|     #
#                                                    #
#    Copyright (c) 2023 Kangas Development Team      #
#    All rights reserved                             #
######################################################
"""
datagrid setup
"""
import io
import os

import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(file, name="__version__"):
    """
    Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


__version__ = get_version(os.path.join(HERE, "datagrid/_version.py"))

with io.open(os.path.join(HERE, "README.md"), encoding="utf8") as fh:
    long_description = fh.read()

setup_args = dict(
    name="datagrid",
    version=__version__,
    url="https://github.com/dsblank/datagrid",
    author="DataGrid Development Team",
    description="Tool for exploring columnar data, including multimedia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "Pillow",
        "astor",
        "marko",
        "matplotlib",
        "numpy",
        "requests",
        "scikit-learn",
        "scipy",
    ],
    packages=[
        "datagrid",
        "datagrid.server",
        "datagrid._datatypes",
    ],
    python_requires=">=3.7",
    license="MIT License",
    platforms="Linux, Mac OS X, Windows",
    keywords=["data science", "python", "machine learning"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
