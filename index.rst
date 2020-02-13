:tocdepth: 1

.. sectnum::

Location and basic usage
========================

LSST Data Management maintains an instance of Hashicorp's Vault product
at `vault.lsst.codes <https://vault.lsst.codes/>`_ .  To use Vault, set
``VAULT_ADDR`` to ``https://vault.lsst.codes``, and set the appropriate
token (described later) in the environment variable ``VAULT_TOKEN``.
Then use the `Vault CLI <https://www.vaultproject.io/downloads.html>`_
(or other client of your choice) to access secrets under the structure
allowed for your token.

Note that we are using Version 2 of the KV Secret Engine (allowing
versioned secrets), and therefore you must read and write secrets with
``vault kv get`` or ``vault kv put`` rather than simple ``vault read``
or ``vault write`` commands.

Vault Implementation
====================

This vault implementation is simply Seth Vargo's `Vault On GKE
<https://github.com/sethvargo/vault-on-gke>`_ with the TLS certificates
replaced with actual certificates rather than self-signed ones.  It is
running on a Kubernetes Cluster in the ``us-central1`` region.  Members
of the LSST DM SQuaRE team have access to the credentials necessary to
administer the cluster.

Taxonomy
========

There are two primary use cases for using Vault.  One is as a generic
secret store.  In that case, our intention is for Vault to be organized
with secret paths under the top-level secret store (``secret/``) as
follows:

``secret/:subsystem:/:team:/:category:/:instance:``

As an example, secrets for the ``nublado.lsst.codes`` instance of
the LSST Science Platform Notebook Aspect are stored in
``secret/dm/square/nublado/nublado.lsst.codes``.  Within that
secret path are ``hub`` and ``tls`` folders, which each
contain a number of individual secrets,
e.g. ``secret/dm/square/nublado/nublado.lsst.codes/hub/oauth_secret``.

The second use case is in conjunction with the `Kubernetes Vault Secrets
Operator <https://github.com/ricoberger/vault-secrets-operator>`_.  If
that is the use case, the secret paths should be organized as:

``secret/k8s_operator/:k8s_cluster_identifier:``

An example thereof would be ``secret/k8s_operator/lsst-lsp-stable.ncsa.illinois.edu``.  In
this case, the Vault Secrets Operator would have complete control over
the secrets underneath that path, although we still advocate creating a
structure out of some combination of namespace and functional role.

Tokens
======

Each secret path will have two tokens created: ``read`` and ``write``.
The ``read`` token can view but not alter data, while the ``write``
token can create, update, or delete data within the secret path.

Token Acquisition and Revocation
================================

To acquire a token pair, ask Adam Thornton (``athornton@lsst.org``) (or
any other SQuaRE personnel) to create a pair for your desired secret
path.  Assuming that the path is correctly-structured, he will give you
a pair of tokens (both ``id`` and ``accessor``) for reading and writing
to the secret path.

To revoke or renew these tokens, indicate to Adam (or another SQuaRE
team member) what path you want revoked or renewed, and (if revocation)
whether the corresponding data should be deleted as well.

Administrative Tools
====================

Administrative tools for working with Vault can be found at the
`LSST Vault Utils GitHub Repository
<https://github.com/lsst-sqre/lsstvaultutils>`_ or by ``pip``-installing
``lsstvaultutils``.

Without an administrative token (limited to SQuaRE team members), you
will not be able to use the ``tokenadmin`` tool, which is the tool by
which token issuance and revocation is managed.

However, with ``read`` and ``write`` tokens you can use ``copyk2v`` and
``copyv2k`` to copy secrets back and forth between Kubernetes secrets
and the Vault implementation.

With a write token you will also be able to use ``vaultrmrf``, which is
exactly as dangerous as it sounds.
