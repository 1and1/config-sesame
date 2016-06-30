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
    mkdir -p ~/.local/virtualenvs
    test -d ~/.local/virtualenvs/config-sesame \
        || virtualenv ~/.local/virtualenvs/config-sesame
    ~/.local/virtualenvs/config-sesame/bin/pip install -U pip setuptools wheel
    ~/.local/virtualenvs/config-sesame/bin/pip install -U "$release"
    mkdir ~/bin 2>/dev/null && exec $SHELL -l
    ln -s ~/.local/virtualenvs/config-sesame/bin/config-sesame ~/bin
    config-sesame --version

On *Linux*, if you want to safely store the credentials to access *Vault* in your account's keyring,
execute these additional commands:

.. code-block:: shell

    sudo apt-get install libdbus-glib-1-dev python-dev libffi-dev build-essential
    ~/.local/virtualenvs/config-sesame/bin/pip install secretstorage dbus-python keyring

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

Make sure your *Vault* server is up and reachable by using these commands:

.. code-block:: shell

    export VAULT_ADDR="http://127.0.0.1:8200"
    vault status

If the server runs on a remote machine, adapt the ``VAULT_ADDR`` accordingly.

Let's try accessing the server via ``config-sesame`` next. First, add the
*vault root token* to your keyring, by calling the ``config-sesame login`` command
which will prompt you for the token and remember it in a safe place.
For the test setup as outlined above, you'll find that token in the file
``/var/lib/vault/.vault-token``.
You can also set the ``VAULT_TOKEN`` environment variable
or create the ``~/.vault-token`` file (which is not as secure as using the keyring),
otherwise you'll be prompted for the token on the console each time it is needed.
Finally call the ``config-sesame help`` command, and it should show some information
about your running *Vault* service.

Note that in a production setup, you will have a personal access token, e.g. obtained
via LDAP or similar credentials.


Production Deployment
---------------------

The project contains a ``debian`` directory that supports building
a self-contained Python virtualenv wrapped into a Debian package
(an "omnibus" package, all passengers on board).
The packaged virtualenv is kept in sync with the host's interpreter automatically.
See `dh-virtualenv`_ for more details.
On platforms that are not some *Debian* flavour, consider using `rpmvenv`_, `platter`_ or `fpm`_.
The motivation to strongly prefer native packages for deployment can be found in
`Python Application Deployment with Native Packages`_.

Note that you need to install the usual Debian development tools and ``dh-virtualenv``
(at least version 0.10), before you can actually build the DEB package.
These incantations will perform that for you (on *Xenial*):

.. code-block:: shell

    sudo apt-get install build-essential debhelper devscripts equivs
    sudo mk-build-deps --install debian/control

*Jessie* only comes with version ``0.7`` – that might work,
otherwise you have to build a newer version from source,
or use ``0.10`` from backports.

Then, if you have all pre-requisites satisfied, try this:

.. code-block:: shell

    dpkg-buildpackage -uc -us -b

The resulting package, if all went well, can be found in the parent of your project directory.
You can upload it to a Debian package repository via e.g. `dput`, see `dput-webdav`_
for a hassle-free solution that works with *Artifactory* and *Bintray*.


.. _`Installing Python Software`: https://py-generic-project.readthedocs.io/en/latest/installing.html#quick-setup
.. _`Python Application Deployment with Native Packages`: https://hynek.me/articles/python-app-deployment-with-native-packages/
.. _`keyring installation`: https://rudiments.readthedocs.io/en/latest/end-user.html#installation-procedures
.. _`Vault's documentation`: https://www.vaultproject.io/intro/getting-started/install.html
.. _`dh-virtualenv`: https://github.com/spotify/dh-virtualenv
.. _`dput-webdav`: https://github.com/jhermann/artifactory-debian#package-uploading
.. _`platter`: http://platter.pocoo.org/
.. _`fpm`: https://github.com/jordansissel/fpm
.. _`rpmvenv`: https://github.com/kevinconway/rpmvenv
