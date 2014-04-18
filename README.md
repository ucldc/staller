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

Requires boost headers to be installed.

## `jpache`

Install tomcat, ant, and maven.

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

