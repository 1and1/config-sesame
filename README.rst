config-sesame
=============

|Logo| A tool to look up secrets from a vault based on existing shareable configuration.

 |Travis CI|  |Coveralls|  |GitHub Issues|  |License|  |Latest Version|  |Downloads|

.. contents:: **Table of Contents**


Overview
--------

The ``config-sesame`` command line tool can be used as part of a
continuous deployment pipeline to provide applications with runtime
secrets. For this purpose, it scans already assembled application
configuration (``application.yml``) for references to secrets stored in
a “vault”, and writes resolved secrets to an additional file
(``secrets.yml``). The diagram below gives you an idea how the tool fits
into a typical CD pipeline – for more details, see the `main documentation`_.

.. figure:: https://raw.githubusercontent.com/1and1/config-sesame/master/docs/_static/img/cd-pipeline.png
   :alt: CD Pipeline


Installation
------------

*Config Sesame* can be installed via ``pip install config-sesame`` as
usual, see `releases`_ for an overview of available versions. To get a
bleeding-edge version from source, use these commands:

.. code:: sh

    repo="1and1/config-sesame"
    pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
    pip install -U -e "git+https://github.com/$repo.git#egg=${repo#*/}"

See `Contributing <#contributing>`_ on how to create a full development environment.

To add bash completion, read the `Click docs`_ about it, or just follow
these instructions:

.. code:: sh

    cmdname=config-sesame
    mkdir -p ~/.bash_completion.d
    ( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
      $cmdname >~/.bash_completion.d/$cmdname.sh )
    grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
        || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
    . "/etc/bash_completion"


Usage
-----

Please see the `main documentation`_ at *Read the Docs* for usage instructions.


Contributing
------------

Contributing to this project is easy, and reporting an issue or adding
to the documentation also improves things for every user. You don’t need
to be a developer to contribute. See `CONTRIBUTING <CONTRIBUTING.md>`_ for more.

As a documentation author or developer, to **create a working
directory** for this project, call these commands:

.. code:: sh

    git clone "https://github.com/1and1/config-sesame.git"
    cd "config-sesame"
    . .env --yes --develop
    invoke build --docs test check

You might also need to follow some `setup procedures`_ to make the
necessary basic commands available on *Linux*, *Mac OS X*, and
*Windows*.

**Running the test suite** can be done several ways, just call
``invoke test`` for a quick check, or ``invoke test.tox`` for testing
with all supported Python versions (if you `have them available`_). Use
``invoke check`` to **run a code-quality scan**.

To **start a watchdog that auto-rebuilds documentation** and reloads the
opened browser tab on any change, call ``invoke docs -w -b`` (stop the
watchdog using the ``-k`` option).


References
----------

**Tools**

-  `Cookiecutter`_
-  `PyInvoke`_
-  `pytest`_
-  `tox`_
-  `Pylint`_
-  `twine`_
-  `bpython`_
-  `yolk3k`_

**Packages**

-  `Rituals`_
-  `Click`_

Acknowledgements
----------------

…



.. _main documentation: http://config-sesame.readthedocs.io/en/latest/overview.html
.. _releases: https://github.com/1and1/config-sesame/releases
.. _Contributing: #contributing
.. _Click docs: http://click.pocoo.org/4/bashcomplete/#activation
.. _`CONTRIBUTING.md`: https://github.com/1and1/config-sesame/blob/master/CONTRIBUTING.md
.. _setup procedures: https://py-generic-project.readthedocs.io/en/latest/installing.html#quick-setup
.. _have them available: https://github.com/jhermann/priscilla/tree/master/pyenv
.. _Cookiecutter: http://cookiecutter.readthedocs.io/en/latest/
.. _PyInvoke: http://www.pyinvoke.org/
.. _pytest: http://pytest.org/latest/contents.html
.. _tox: https://tox.readthedocs.io/en/latest/
.. _Pylint: http://docs.pylint.org/
.. _twine: https://github.com/pypa/twine#twine
.. _bpython: http://docs.bpython-interpreter.org/
.. _yolk3k: https://github.com/myint/yolk#yolk
.. _Rituals: https://jhermann.github.io/rituals
.. _Click: http://click.pocoo.org/

.. |Logo| image:: https://raw.githubusercontent.com/1and1/config-sesame/master/docs/_static/img/logo.png
.. |Travis CI| image:: https://api.travis-ci.org/1and1/config-sesame.svg
   :target: https://travis-ci.org/1and1/config-sesame
.. |Coveralls| image:: https://img.shields.io/coveralls/1and1/config-sesame.svg
   :target: https://coveralls.io/r/1and1/config-sesame
.. |GitHub Issues| image:: https://img.shields.io/github/issues/1and1/config-sesame.svg
   :target: https://github.com/1and1/config-sesame/issues
.. |License| image:: https://img.shields.io/pypi/l/config-sesame.svg
   :target: https://github.com/1and1/config-sesame/blob/master/LICENSE
.. |Latest Version| image:: https://img.shields.io/pypi/v/config-sesame.svg
   :target: https://pypi.python.org/pypi/config-sesame/
.. |Downloads| image:: https://img.shields.io/pypi/dw/config-sesame.svg
   :target: https://pypi.python.org/pypi/config-sesame/
