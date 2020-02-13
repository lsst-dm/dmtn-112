:tocdepth: 1

.. sectnum::

Location and Basic Usage
========================

LSST Data Management maintains an instance of HashiCorp's Vault product at `vault.lsst.codes <https://vault.lsst.codes/>`_.
To use Vault, set ``VAULT_ADDR`` to ``https://vault.lsst.codes``, and set the appropriate token (described later) in the environment variable ``VAULT_TOKEN``.
Then use the `Vault CLI <https://www.vaultproject.io/downloads.html>`_ (or other client of your choice) to access secrets under the structure allowed for your token.

Note that we are using Version 2 of the KV Secret Engine (allowing versioned secrets), and therefore you must read and write secrets with ``vault kv get`` or ``vault kv put`` rather than simple ``vault read`` or ``vault write`` commands.

Vault Implementation
====================

There is currently a single Vault instance for LSST Data Management.
That instance is deployed in the Roundtable Kubernetes cluster hosted on :abbr:`GCP (Google Cloud Platform)`.
It is deployed using the standard HashiCorp `Vault Helm chart <https://www.vaultproject.io/docs/platform/k8s/index.html>`__.
The server uses Let's Encrypt certificates and does not require client certificate authentication.
See the `operational documentation <https://roundtable.lsst.io/ops/vault/index.html>`__ for more information.

In the future, we may separate the Vault instance for production services running at the LDF from the Roundtable Vault for other supporting services and test environments.

Each Kubernetes cluster that uses Vault to store secrets has one instance of the Kubernetes `Vault Secrets Operator`_ deployed in the cluster.
This service is responsible for retrieving secrets from Vault and materializing them as Kubernetes ``Secret`` resources.
This is configured via Kubernetes ``VaultSecret`` resources.

.. _Vault Secrets Operator: https://github.com/ricoberger/vault-secrets-operator

HashiCorp provides a `Vault Agent Injector`_ as an alternate way to integrate Kubernetes workloads with Vault.
We considered using this instead of Vault Secrets Operator primarily because HashiCorp supports it, but decided against it for several reasons:

.. _Vault Agent Injector: https://www.vaultproject.io/docs/agent/

#. Vault Secrets Operator allows us to generate one Vault token per Kubernetes cluster that has read access to all secrets for that cluster.
   Vault Agent Injector requires either configuring tokens per service or requires configuring Kubernetes or GCP authentication to Vault, both of which are more complex.
#. Vault Secrets Operator exposes the secrets as Kubernetes secrets, which allows for easy interoperability with Helm charts and other resources that expect Kubernetes secrets.
   Vault Agent Injector creates a separate local file system, which applications then have to be configured to use.
#. Injecting sidecars can cause problems and complexity with some Kubernetes workloads that don't interact well with sidecar processes.

Taxonomy
========

There are two primary use cases for using Vault.
One is as a generic secret store.
In that case, our intention is for Vault to be organized with secret paths under the top-level secret store (``secret/``) as follows::

    secret/:subsystem:/:team:/:category:/:instance:

As an example, secrets for the ``nublado.lsst.codes`` instance of the LSST Science Platform Notebook Aspect are stored in ``secret/dm/square/nublado/nublado.lsst.codes``.
Within that secret path are ``hub`` and ``tls`` folders, which each contain a number of individual secrets, e.g. ``secret/dm/square/nublado/nublado.lsst.codes/hub/oauth_secret``.

The second use case is in conjunction with the Kubernetes `Vault Secrets Operator`_.
If that is the use case, the secret paths should be organized as::

    secret/k8s_operator/:k8s_cluster_identifier:

An example thereof would be ``secret/k8s_operator/lsst-lsp-stable.ncsa.illinois.edu``.
In this case, the owner of the relevant Kubernetes cluster may choose how to organize secrets under that path.
However, we recommend using a similar structure of::

    secret/k8s_operator/:k8s_cluster_identifier:/:subsystem:/:team:/:application:

For example, the secret for a SQuaRE microservice named ``uservice-ghslacker`` deployed to Roundtable would be named ``secret/k8s_operator/roundtable/dm/square/uservice-ghslacker``.
If the application required more than one secret, that would instead be a folder containing multiple secrets.

Tokens
======

Each secret path will have two tokens created: ``read`` and ``write``.
The ``read`` token can view but not alter data, while the ``write`` token can create, update, or delete data within the secret path.

An installation of the Kubernetes Vault Secrets Operator will be given a ``read`` token for the entire ``secret/k8s_operator/:k8s_cluster_identifier:`` path for that Kubernetes cluster.
(In the future, we may replace this with Kubernetes authentication for the case of a Vault Secrets Operator running in the same cluster as Vault itself.)

Token Acquisition and Revocation
================================

To acquire a token pair, ask `Russ Allbery`_ (or any other SQuaRE team member) to create a pair for your desired secret path.
Assuming that the path is correctly-structured, he will give you a pair of tokens (both ``id`` and ``accessor``) for reading and writing to the secret path.

.. _Russ Allbery: rra@lsst.org

To revoke or renew these tokens, indicate to Russ (or another SQuaRE team member) what path you want revoked or renewed, and (if revocation) whether the corresponding data should be deleted as well.

Administrative Tools
====================

Administrative tools for working with Vault can be found at the `LSST Vault Utils GitHub Repository <https://github.com/lsst-sqre/lsstvaultutils>`_ or by ``pip``-installing ``lsstvaultutils``.

Without an administrative token (limited to SQuaRE team members), you will not be able to use the ``tokenadmin`` tool, which is the tool by which token issuance and revocation is managed.

However, with ``read`` and ``write`` tokens you can use ``copyk2v`` and ``copyv2k`` to copy secrets back and forth between Kubernetes secrets and the Vault implementation.
(That said, you should generally use a ``VaultSecret`` resource and let Vault Secrets Operator create Kubernetes secrets for you, rather than using the ``copyv2k`` tool.)

With a write token you will also be able to use ``vaultrmrf``, which is exactly as dangerous as it sounds.
