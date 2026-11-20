# cryfio chart

Our own Helm chart, holding only what is specific to OM-Cryfio. Templates are grouped by namespace: `cluster-wide`, `cryfio-app`, `cryfio-data`, `cryfio-admin` and `cryfio-ops`.

Third-party software (cert-manager, CloudNativePG, monitoring) is installed from its official chart by `private-site/terraform/`, not here.
