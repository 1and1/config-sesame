..  documentation master file

    Copyright ©  2016 1&1 Group <jh@web.de>

    ## LICENSE_SHORT ##
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


=============================================================================
Welcome to the “Config Sesame” manual!
=============================================================================

.. |logo| image:: _static/img/logo.png

|logo| *A tool to look up secrets from a vault based on existing shareable configuration.*

Introduction
------------

The ``config-sesame`` command line tool can be used as part of a continuous deployment pipeline
to provide applications with runtime secrets.
For this purpose, it scans already assembled application configuration (``application.yml``)
for references to secrets stored in a “vault”, and writes resolved secrets to an additional file
(``secrets.yml``). See :doc:`usage` for more.

Read :doc:`overview` to get to know the ideas behind the design of the tool.


Important Links
---------------

  * `GitHub Project <https://github.com/1and1/config-sesame>`_
  * `Issue Tracker <https://github.com/1and1/config-sesame/issues>`_
  * `PyPI <https://pypi.python.org/pypi/config-sesame/>`_
  * `Latest Documentation <https://config-sesame.readthedocs.org/en/latest/>`_


Installing
----------

*Config Sesame* can be installed from PyPI
via ``pip install config-sesame`` as usual,
see `releases <https://github.com/1and1/config-sesame/releases>`_
on GitHub for an overview of available versions – the project uses
`semantic versioning <http://semver.org/>`_ and follows
`PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_ conventions.

To get a bleeding-edge version from source, use these commands:

.. code-block:: shell

    repo="1and1/config-sesame"
    pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
    pip install -U -e "git+https://github.com/$repo.git#egg=${repo#*/}"

See the following section on how to create a full development environment.

To add bash completion, read the
`Click docs <http://click.pocoo.org/4/bashcomplete/#activation>`_
about it, or just follow these instructions:

.. code-block:: shell

    cmdname=config-sesame
    mkdir -p ~/.bash_completion.d
    ( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
      $cmdname >~/.bash_completion.d/$cmdname.sh )
    grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
        || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
    . "/etc/bash_completion"


Contributing
------------

To create a working directory for this project, call these commands:

.. code-block:: shell

    git clone "https://github.com/1and1/config-sesame.git"
    cd "config-sesame"
    . .env --yes --develop
    invoke build --docs test check

Contributing to this project is easy, and reporting an issue or
adding to the documentation also improves things for every user.
You don’t need to be a developer to contribute.
See :doc:`CONTRIBUTING` for more.


Documentation Contents
----------------------

.. toctree::
    :maxdepth: 4

    overview
    usage
    api-reference
    CONTRIBUTING
    LICENSE


References
----------

Tools
^^^^^

-  `Cookiecutter <http://cookiecutter.readthedocs.org/en/latest/>`_
-  `PyInvoke <http://www.pyinvoke.org/>`_
-  `pytest <http://pytest.org/latest/contents.html>`_
-  `tox <https://tox.readthedocs.org/en/latest/>`_
-  `Pylint <http://docs.pylint.org/>`_
-  `twine <https://github.com/pypa/twine#twine>`_
-  `bpython <http://docs.bpython-interpreter.org/>`_
-  `yolk3k <https://github.com/myint/yolk#yolk>`_

Packages
^^^^^^^^

-  `Rituals <https://jhermann.github.io/rituals>`_
-  `Click <http://click.pocoo.org/>`_


Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
