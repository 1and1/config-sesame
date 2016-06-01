..  documentation for deployment

    Copyright ©  2016 1&1 Group <jh@web.de>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=============================================================================
Installing Config Sesame
=============================================================================

Below you find several different options to install the tool and
*Hashicorp Vault*, and how to connect them.


Installing Into a Python Virtualenv
-----------------------------------

These commands install ``config-sesame`` into its own virtualenv in your home.
It can be easily removed again, since most everything is contained
within the virtualenv's directory.
Also see `Installing Python Software`_ in case your machine lacks *Python*
or tools like ``virtualenv``.

.. code-block:: shell

    #release="config-sesame"
    release="https://github.com/1and1/config-sesame/archive/master.zip#egg=config-sesame"

    # install "config-sesame" to its own virtualenv
    mkdir -p ~/.local/venvs
    test -d ~/.local/venvs/config-sesame \
        || virtualenv ~/.local/venvs/config-sesame
    ~/.local/venvs/config-sesame/bin/pip install -U pip setuptools wheel
    ~/.local/venvs/config-sesame/bin/pip install -U "$release"
    mkdir ~/bin 2>/dev/null && exec $SHELL -l
    ln -s ~/.local/venvs/config-sesame/bin/config-sesame ~/bin
    config-sesame --version

On *Linux*, if you want to safely store the credentials to access *Vault* in your account's keyring,
execute these additional commands:

.. code-block:: shell

    sudo apt-get install libdbus-glib-1-dev python-dev libffi-dev build-essential
    ~/.local/venvs/config-sesame/bin/pip install secretstorage dbus-python keyring

See `keyring installation`_ for more details on that.


Installing Hashicorp Vault
--------------------------

See `Vault's documentation`_ for detailed instructions.
For a simple development / test installation on *Ubuntu*,
this works when called in a ``root`` shell:

.. code-block:: shell

    version=0.5.3
    curl -sLS "https://releases.hashicorp.com/vault/${version}/vault_${version}_linux_amd64.zip" \
        | funzip >/usr/local/bin/vault
    chmod a+x /usr/local/bin/vault
    apt-get install supervisor
    adduser vault --ingroup daemon --home /var/lib/vault --system --disabled-password
    cat >/etc/supervisor/conf.d/vault.conf <<'EOF'
    [program:vault]
    command         = /usr/local/bin/vault server -dev
    user            = vault
    redirect_stderr = True
    autostart       = True
    EOF
    supervisorctl update
    supervisorctl tail -2200 vault

.. warning::

    As mentioned above, this is intended for experimenting with Vault on
    your workstation. Do **NOT** run it this way on anything that is intended
    for production use.


Providing Credentials for Vault
-------------------------------

**TODO**


.. _`Installing Python Software`: https://py-generic-project.readthedocs.io/en/latest/installing.html#quick-setup
.. _`keyring installation`: https://rudiments.readthedocs.io/en/latest/end-user.html#installation-procedures
.. _`Vault's documentation`: https://www.vaultproject.io/intro/getting-started/install.html
