..  documentation: usage

    Copyright ©  2016 1&1 Group <jh@web.de>

    ## LICENSE_SHORT ##
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=============================================================================
Using Config Sesame
=============================================================================


Providing Credentials for Vault
-------------------------------

**TODO**


Performing Password Lookups
---------------------------

The following examples ilustrate the process of augmenting secrets references
with their resolution from Vault; see :ref:`parsing-rules` for more.

* “my: database: password: vault:db/password” gets resolved to “my: database: password_secret: the_actual_password”.
* The configuration…

    .. code-block:: yaml

        db:
          auth: "vault:db/credentials"

  becomes…

    .. code-block:: yaml

        db:
          auth_secrets:
            user: jane
            password: test123


.. _parsing-rules:

Details of Configuration Parsing
--------------------------------

To support reading multiple input files, a simple merging strategy is used:

* objects (dicts, hashes) are merged recursively.
* scalar values and lists are simply replaced (i.e. the last file has priority).

For the purpose of finding references to secrets and writing their resolution to a new file,
this always fits the bill.

The rules for handling secrets references:

* Secrets references are stored like any other configuration key, and take the form ``vault:«vault-path»``.
* The ``«vault-path»`` part is resolved relative to a base path, e.g. “apps/«app name»/«brand»/«environment»”.
* The Vault base path is part of the tool's configuration.
* If ``«vault-path»`` references a single scalar value, it is added to ``secrets.yml`` as ``«reference key»_secret`` (this considers the restrictions of YAML, a key cannot be both a value and a dict, so we cannot use “.secret”).
* If ``«vault-path»`` references a sub-tree, the immediate children of that tree are added to a dict under the key ``«reference key»_secrets``. Note the immediate children restriction, which prevents mis-configurations from exploding deeply nested trees into ``secrets.yml`` (we can still loosen or lift that restriction later on, if necessary).
