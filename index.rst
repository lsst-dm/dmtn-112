..
  Technote content.

  See https://developer.lsst.io/restructuredtext/style.html
  for a guide to reStructuredText writing.

  Do not put the title, authors or other metadata in this document;
  those are automatically added.

  Use the following syntax for sections:

  Sections
  ========

  and

  Subsections
  -----------

  and

  Subsubsections
  ^^^^^^^^^^^^^^

  To add images, add the image file (png, svg or jpeg preferred) to the
  _static/ directory. The reST syntax for adding the image is

  .. figure:: /_static/filename.ext
     :name: fig-label

     Caption text.

   Run: ``make html`` and ``open _build/html/index.html`` to preview your work.
   See the README at https://github.com/lsst-sqre/lsst-technote-bootstrap or
   this repo's README for more info.

   Feel free to delete this instructional comment.

:tocdepth: 1

.. Please do not modify tocdepth; will be fixed when a new Sphinx theme is shipped.

.. sectnum::

   
.. Add content here.
.. Do not include the document title (it's automatically added from metadata.yaml).

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

Our intention is for Vault to be organized with secret paths under the
top-level secret store (``secret/``) as follows:

``secret/:subsystem:/:team:/:category:/:instance:``

As an example, secrets for the ``nublado.lsst.codes`` instance of
the LSST Science Platform Notebook Aspect are stored in
``secret/dm/square/nublado/nublado.lsst.codes``.  Within that
secret path are ``hub`` and ``tls`` folders, which each
contain a number of individual secrets,
e.g. ``secret/dm/square/nublado/nublado.lsst.codes/hub/oauth_secret``.

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

.. .. rubric:: References

.. Make in-text citations with: :cite:`bibkey`.

.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :style: lsst_aa
