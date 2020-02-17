"""Source for vault.png configuration diagram.

To regenerate vault.png, run Python on this file with diagrams installed.
"""

from diagrams import Cluster, Diagram
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.security import KMS
from diagrams.gcp.storage import GCS

graph_attr = {
    "label": "",
    "nodesep": "0.2",
    "pad": "0.2",
    "ranksep": "0.75",
}

node_attr = {
    "fontsize": "10.0",
}

with Diagram(
    "Vault",
    show=False,
    outformat="png",
    graph_attr=graph_attr,
    node_attr=node_attr,
):
    with Cluster("Roundtable"):
        with Cluster("Vault"):
            lb = LoadBalancing("vault.lsst.codes")

            with Cluster("Active"):
                vault_0 = KubernetesEngine("vault-0")

            lb >> vault_0

            with Cluster("Standby"):
                lb >> KubernetesEngine("vault-1")
                lb >> KubernetesEngine("vault-2")

        secrets_operator = KubernetesEngine("Vault Secrets Operator")

        with Cluster("Other Apps"):
            secrets_operator >> KMS("Secret") << KubernetesEngine("Other Pod")
            secrets_operator >> KMS("Secret") << KubernetesEngine("Other Pod")

        secrets_operator >> lb

    vault_0 >> KMS("vault-seal KMS key")
    vault_0 >> GCS("storage.lsst.vault.codes")
