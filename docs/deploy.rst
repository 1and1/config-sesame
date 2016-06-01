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

Installing Hashicorp Vault
--------------------------

See `Vault's documentation`_ for detailed instructions.
For a simple development / test installation on *Ubuntu*, this works:

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


.. _`Vault's documentation`: https://www.vaultproject.io/intro/getting-started/install.html
