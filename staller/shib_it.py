#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os
import argparse
from pprint import pprint as pp
import tempfile
# import gnupg
import subprocess
import shutil
from staller import scraper, key_import
import errno
import re
from collections import defaultdict


def main(argv=None):
    # https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPLinuxSourceBuild
    packages = [
        ( 'https://curl.haxx.se/download.html',
          'curl',
          './configure --disable-static --with-openssl={openssl} --prefix={prefix}',
        ),
        ( 'https://shibboleth.net/downloads/log4shib/latest/', 
          'log4shib', 
          './configure --disable-static --disable-doxygen --prefix={prefix}',
        ),
        ( 'https://xerces.apache.org/xerces-c/download.cgi', 
          'xerces-c',
          './configure --prefix={prefix} --disable-netaccessor-curl --disable-transcoder-gnuiconv --with-curl={prefix}',
        ),
        ( 'https://santuario.apache.org/download.html', 
          'xml-security-c',
          './configure --without-xalan --disable-static --prefix={prefix} --with-xerces={prefix} --with-openssl={openssl}',
        ),
        ( 'https://shibboleth.net/downloads/c++-opensaml/latest/', 
          'xmltooling',
          './configure --with-log4shib={prefix} --prefix={prefix} -C --with-boost={boost} --with-curl={prefix}'
        ),
        ( 'https://shibboleth.net/downloads/c++-opensaml/latest/', 
          'opensaml',
          './configure --with-log4shib={prefix} --prefix={prefix} -C --with-boost={boost}'
        ),
        ( 'https://shibboleth.net/downloads/service-provider/latest/', 
          'shibboleth-sp',
          './configure --with-log4shib={prefix} --enable-apache-24 --with-apxs24={apxs} --prefix={prefix} --with-openssl={openssl} --with-boost={boost}'
        ),
    ]
    parser = argparse.ArgumentParser( )
    parser.add_argument('-p', '--prefix', required=True)
    parser.add_argument('--boost', required=True)
    parser.add_argument('--openssl', required=True)
    parser.add_argument('--apxs', help='full path to apxs', required=True)

    parser.add_argument('-t', '--tempdir', required=False)
    parser.add_argument('-f', '--force', action='store_true', required=False)

    if argv is None:
        argv = parser.parse_args()

    with_opts = {
        'prefix': argv.prefix,
        'boost': argv.boost,
        'openssl': argv.openssl,
        'apxs': argv.apxs,
    }

    shibd_path = os.path.join(argv.prefix,'sbin','shibd')

    if os.path.isfile(shibd_path) and not argv.force:
        print "been done? use -f/--force to force rebuild"
        exit(0)

    keys = [ 
        'https://www.apache.org/dist/santuario/KEYS', 
        'https://www.apache.org/dist/xerces/c/KEYS',
        'https://daniel.haxx.se/mykey.asc'
    ]

    if argv.tempdir:
        mkdir_p(argv.tempdir)
        tempfile.tempdir = argv.tempdir

    for (url, package, configure) in packages:
        config_command = configure.format(**with_opts)
        print config_command

    tmp = tempfile.mkdtemp(prefix="shib_builder_")
    key_import(keys, tmp)
    os.chdir(tmp)
    pp(tmp)

    os.environ['CFLAGS'] = os.environ['CPPFLAGS'] = "-g -I {0}/include".format(argv.prefix)
    os.environ['LDFLAGS'] = "-L{0}/lib".format(argv.prefix)
    resetldpath(argv.prefix)
    #resetldpath(argv.prefix, argv.other_prefix)

    for (url, package, configure) in packages:
        config_command = configure.format(**with_opts)
        print config_command
        # scraper looks at the "latest download" web page, finds the newest .tar.gz, 
        # verfies MD5 checksum and and the pgp signature
        # downloads verified package to `tmp` and returns the path to the .tar.gz
        archive = scraper(url, package, tmp)
        os.chdir(tmp)
        print subprocess.check_output(['tar', 'zxf', archive])
        src_dir = archive[:-7] # strip off '.tar.gz'
        print src_dir
        os.chdir(src_dir)
        # --with-boost=/registry/pkg/include
        subprocess.check_output(config_command.split())
        subprocess.check_output(['make'])
        subprocess.check_output(['make', 'install'])

    # test the shib command when we are done
    subprocess.check_output([shibd_path, '-t'])
    sanity_check_ldd(shibd_path)

    # ## somehow check the shibd for bad links

    # save config.logs from source building tree before deleting?
    shutil.rmtree(tmp)


def sanity_check_ldd(path):
    parse_ldd = re.compile('^\t(.*?)\\.')  # parse ldd outout
    d = defaultdict(bool)
    # look for duplicate libraries
    try:  # ldd might not exist (as on OS X)
        for line in subprocess.check_output(['ldd', path]).split('\n'):
            if line == '':
                break
            lib = parse_ldd.search(line).group(0)
            # http://youtu.be/SckD99B51IA?t=22s
            assert not(lib in d), "dubious binary, ldd finds more than one {0}".format(lib)
            d[lib] = True
    except OSError:
        # is this OSX? try running `otool`?
        pass


def resetldpath(addition):
    ldd_path = ""
    path = []
    if os.environ.get('LD_LIBRARY_PATH'):
        ldd_path = os.environ['LD_LIBRARY_PATH']
        path = ldd_path.split(':')
    
    path.insert(0, "{0}/lib".format(addition))
    
    if len(path) > 1:
        ldd_path = ":".join(path)
    else:
        ldd_path = path[0]

    os.environ['LD_LIBRARY_PATH'] = ldd_path


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# main() idiom for importing into REPL for debugging 
if __name__ == "__main__":
    sys.exit(main())

"""
Copyright © 2014, Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, 
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, 
  this list of conditions and the following disclaimer in the documentation 
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this 
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""
