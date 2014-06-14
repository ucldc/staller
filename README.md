# Staller

Automates the tasks of installing software.  Core library takes care of

 1. checking a URL for a link to the latest version of a software package
 2. downloading the package
 3. checking the PGP signature
 4. checking the MD5 checksums

Requires `gpg` on the command path.

## `shib_it`

Automate the steps do build shibboleth SP based on 
[NativeSPLinuxSourceBuild](https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPLinuxSourceBuild)
but seems to work on OS X as well.  Seems like it would work on Solaris and BSD to.

```
usage: shib_it [-h] -p PREFIX --boost BOOST --curl CURL --openssl OPENSSL
                  --apxs APXS [-t TEMPDIR] [-f]
```

Requires boost headers to be installed.

## `jpache`

Install latest tomcat, ant, and maven.

```
usage: jpache [-h] -p PREFIX [-t TEMPDIR] [-f]
```

## `solr_it`

Solr distribution is set up different from the other apache java stuff.  Must 
specify the version of solr needed.

```
usage: solr_it [-h] -p PREFIX -v VERSION [-t TEMPDIR] [-f]
```

## Install the 'staller

```
pip install staller
```

or 
```
git clone https://github.com/ucldc/staller.git
cd staller
python setup.py install
```

