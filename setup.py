# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name = "staller",
    version = "0.4.5",
    packages = find_packages(),
    install_requires = ['lxml', 'argparse'],
    # metadata for upload to PyPI
    author = "California Digital Library",
    description = ("Small application to find the latest version of a software" 
                   "package, download it, check the PGP signature, check "
                   "the checksums, and install it."),
    license = "BSD",
    keywords = "",
    url = "https://github.com/ucldc/staller",   # project home page, if any
    # download_url = "https://github.com/ucldc/staller/tarball/0.4.0",
    # could also include long_description, download_url, classifiers, etc.
    entry_points = {
        'console_scripts': [
            'shib_it = staller.shib_it:main',
            'solr_it = staller.solr_it:main',
            'jpache = staller.jpache:main',
        ]
    }
)

# Copyright © 2014, Regents of the University of California
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
