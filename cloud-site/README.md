# Cloud site

The off-site side of OM-Cryfio: a WireGuard endpoint and a private bucket holding the encrypted file replica and the database backups. It comes in two interchangeable versions, `aws/` and `selfhosted/`, which follow the same contract in `contract/`.

Terraform runs from the operator workstation. The setup in `selfhosted/host/` runs on the cloud server itself.
