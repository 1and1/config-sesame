..  documentation: usage

    Copyright ©  2016 1&1 Group <jh@web.de>

    ## LICENSE_SHORT ##
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=============================================================================
Overview of Config Sesame
=============================================================================

Motivation
----------

Collaborative workflows in a devops environment profit from shared code and configuration repositories, due to increased transparency and lowered maintenance efforts.
Having fewer redundantly maintained copies of shareable information also reduces hand-over friction and thus error rates.

As a consequence, secrets need their own place outside of code and configuration SCM systems, with an enforced access policy.
That leaves the rest of the configuration in a state where it can be freely shared amongst technical staff (i.e. put into the application's source code repository).
The secrets that are left out are then replaced by *references* to those secrets, so they can be looked up later on and provided to the consuming applications as part of the delivery process.
Typical secrets are passwords, SSH private keys + certificates, and API keys.
Secrets can be used both for purposes of controlling the pipeline and protecting target assets, as well as merely transported to target systems by inserting them into configuration sets.

The purpose of this tool is protecting sensitive information when it's used in the delivery pipeline and its workflows.
How secrets are stored and used on the target systems is out of scope, since that is strongly coupled to external (technical) restrictions of the target platforms and applications.

Protecting the secrets is done by delaying their injection into the pipeline as long as possible, and create a *separate* configuration file on either a deployment agent (e.g. a machine running Ansible playbooks), or the target system.
Using an agent machine is preferable, since then the vault access credentials are used at fewer places, and you have fewer machines to consider when maintaining your tools.


Concepts
--------

The following tenets and requirements were considered in the design:

  * Secrets need to be **managed and stored securely**, ideally *apart* from other not so sensitive configuration information.
  * Secrets must be **identifiable**, so they can be **referenced** from openly available configuration.
  * Secrets must be **distinguishable**, so they can be **filtered or hidden** in reports, logs, web interfaces, or for anonymous access.
  * During deployment, secrets need to be **looked up and added** to already collected configuration sets, by augmenting references to them, as late as technically possible.
  * **Access and use secrets as late as possible** in a pipeline, and keep tight control where they end up.
  * Secrets must be **handled in a transient fashion** (don't add them to persistent storage if avoidable).
  * Use authorization credentials of the *initiator* of a pipeline run to access secrets, but **without revealing them**.


Why Use a Vault?
----------------

While SCM-based encryption tools (like `ansible-vault`_) might fit your needs, using a vault backend has additional advantages.

`Hashicorp Vault`_ specifically offers these features:
  * dynamic credentials.
  * more versatile authentication options.
  * key management over time is more stringent (leases, revoke, …).
  * better auditing (non-repudiation is a primary concern).


.. _`Hashicorp Vault`: https://www.vaultproject.io/
.. _`ansible-vault`: http://docs.ansible.com/ansible/playbooks_vault.html


Implementation
--------------

The first release will support `Hashicorp Vault`_ as the secrets store.
If you need support for other backends, please open an issue, or even better,
file a PR – see :doc:`CONTRIBUTING` for more.

We also restrict the configuration file support to YAML for the initial implementation,
to keep things simple and because we think that amongst the standard formats it's the one
most easily handled by humans, while still being very versatile and powerful.

The format used for referencing secrets is ``vault:[‹vault-name›:]‹secret-name›``.
Edge cases where a backend uses colons for their own purposes, or an application uses
``vault:`` as a prefix in its own configuration values, can be handled by escaping
via duplication (``::``).


A Typical CD Pipeline
---------------------

**TODO**
