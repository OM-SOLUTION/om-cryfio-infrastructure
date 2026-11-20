# Cluster deployment

Deploys everything onto the k3s cluster: namespaces, secrets, cert-manager, CloudNativePG, monitoring and the cryfio chart.

The Kubernetes API port (6443) must never be exposed to the internet.
