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
* If ``«vault-path»`` references a sub-tree, the *immediate children* of that tree are added to a dict under the key ``«reference key»_secrets``. Note the immediate children restriction, which prevents mis-configurations from exploding deeply nested trees into ``secrets.yml`` (we can still loosen or lift that restriction later on, if necessary).
