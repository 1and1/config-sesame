..  documentation: usage

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
Using Config Sesame
=============================================================================

*See* :doc:`deploy` *for instructions on how to install and configure the tool.*


Performing Password Lookups
---------------------------

The following examples ilustrate the process of augmenting secrets references
with their resolution from Vault; see :ref:`parsing-rules` for more.

* ``my: database: password_secret: vault:db/password``

  gets resolved to

  ``my: database: password: the_actual_password``
* The configuration…

    .. code-block:: yaml

        db:
          auth_secret: "vault:db/credentials"

  becomes…

    .. code-block:: yaml

        db:
          auth:
            user: jane
            password: test123


A Practical Example
-------------------

To see how everything works in reality, the project repository comes with test data
that can be used in combination with the Vault setup described in the previous chapter.

First, let's populate the test server with some secrets:

.. code-block:: shell

    $ invoke populate
    vault write "secret/sesame/db/credentials" pwd="SECRET" user="kermit"
    Success! Data written to: secret/sesame/db/credentials
    vault write "secret/sesame/db2/password" value="ALSO_SECRET"
    Success! Data written to: secret/sesame/db2/password
    vault write "secret/sesame/resource/password" value="MORE_SECRETS"
    Success! Data written to: secret/sesame/resource/password

Since this delegates the work to the ``vault`` command, you have to set both
the ``VAULT_ADDR`` and ``VAULT_TOKEN`` environment variables beforehand.

Now we can use the sample data in ``src/tests/data`` to perform a lookup on these keys:

.. code-block:: shell

    $ config-sesame open src/tests/data/*yml -o- -b secret/apps -b secret/sesame
    db:
      auth:
        pwd: SECRET
        user: kermit
      auth_secret_url: http://127.0.0.1:8200/v1/secret/sesame/db/credentials
    my:
      database:
        password: ALSO_SECRET
        password_secret_url: http://127.0.0.1:8200/v1/secret/sesame/db2/password
      resource:
        password: MORE_SECRETS
        password_secret_url: http://127.0.0.1:8200/v1/secret/sesame/resource/password

Note that the source of each resolved secret is also added to the result, for diagnostic
and auditing purposes. In case one of the secret references cannot be resolved, we get an error:

.. code-block:: shell

    $ config-sesame open src/tests/data/*yml -b foo -b bar
    Usage: config-sesame open [OPTIONS] CFGFILE [...]

    Error: Cannot find key "db/credentials" in any of these bases: foo, bar.


.. _parsing-rules:

Details of Configuration Parsing
--------------------------------

To support reading multiple input files, a simple merging strategy is used:

* Objects (dicts, hashes) are merged recursively.
* Scalar values and lists are simply replaced (i.e. the last file has priority).

For the purpose of finding references to secrets and writing their resolution to a new file,
this always fits the bill.

The rules for handling secrets references:

* Secrets references are stored like any other configuration key, and take the form ``vault:«vault-path»``.
* The ``«vault-path»`` part is resolved relative to a base path, e.g. “apps/«app name»/«brand»/«environment»”.
* The Vault base path is part of the tool's configuration.
* Resolved secrets are added to ``secrets.yml`` as ``«key»`` for a reference named ``«key»_secret``.
* If ``«vault-path»`` references a single scalar value, it is added as such.
* If ``«vault-path»`` references a collection of values, they are added as an object (a/k/a dict or hash).
* The URL where the secret was retrieved from is added as ``«key»_secret_url``.
