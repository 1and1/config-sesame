# config-sesame

![Logo](https://raw.githubusercontent.com/1and1/config-sesame/master/docs/_static/img/logo.png)
A tool to look up secrets from a vault based on existing shareable configuration.

 [![Travis CI](https://api.travis-ci.org/1and1/config-sesame.svg)](https://travis-ci.org/1and1/config-sesame)
 [![Coveralls](https://img.shields.io/coveralls/1and1/config-sesame.svg)](https://coveralls.io/r/1and1/config-sesame)
 [![GitHub Issues](https://img.shields.io/github/issues/1and1/config-sesame.svg)](https://github.com/1and1/config-sesame/issues)
 [![License](https://img.shields.io/pypi/l/config-sesame.svg)](https://github.com/1and1/config-sesame/blob/master/LICENSE)
 [![Latest Version](https://img.shields.io/pypi/v/config-sesame.svg)](https://pypi.python.org/pypi/config-sesame/)
 [![Downloads](https://img.shields.io/pypi/dw/config-sesame.svg)](https://pypi.python.org/pypi/config-sesame/)


## Overview

The ``config-sesame`` command line tool can be used as part of a continuous deployment pipeline
to provide applications with runtime secrets.
For this purpose, it scans already assembled application configuration (``application.yml``)
for references to secrets stored in a “vault”, and writes resolved secrets to an additional file
(``secrets.yml``).


## Installation

*Config Sesame* can be installed via ``pip install config-sesame`` as usual,
see [releases](https://github.com/1and1/config-sesame/releases) for an overview of available versions.
To get a bleeding-edge version from source, use these commands:

```sh
repo="1and1/config-sesame"
pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
pip install -U -e "git+https://github.com/$repo.git#egg=${repo#*/}"
```

See [Contributing](#contributing) on how to create a full development environment.

To add bash completion, read the [Click docs](http://click.pocoo.org/4/bashcomplete/#activation) about it,
or just follow these instructions:

```sh
cmdname=config-sesame
mkdir -p ~/.bash_completion.d
( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
  $cmdname >~/.bash_completion.d/$cmdname.sh )
grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
    || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
. "/etc/bash_completion"
```


## Usage

…


## Contributing

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See [CONTRIBUTING](https://github.com/1and1/config-sesame/blob/master/CONTRIBUTING.md) for more.

As a documentation author or developer,
to **create a working directory** for this project,
call these commands:

```sh
git clone "https://github.com/1and1/config-sesame.git"
cd "config-sesame"
. .env --yes --develop
invoke build --docs test check
```

You might also need to follow some
[setup procedures](https://py-generic-project.readthedocs.org/en/latest/installing.html#quick-setup)
to make the necessary basic commands available on *Linux*, *Mac OS X*, and *Windows*.

**Running the test suite** can be done several ways, just call ``invoke test`` for a quick check,
or ``invoke test.tox`` for testing with all supported Python versions
(if you [have them available](https://github.com/jhermann/priscilla/tree/master/pyenv)).
Use ``invoke check`` to **run a code-quality scan**.

To **start a watchdog that auto-rebuilds documentation** and reloads the opened browser tab on any change,
call ``invoke docs -w -b`` (stop the watchdog using the ``-k`` option).


## References

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.org/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [Rituals](https://jhermann.github.io/rituals)
* [Click](http://click.pocoo.org/)


## Acknowledgements

…
