# Cloud contract: values each cloud-site version hands to the private site

Both implementations export exactly these keys into `secrets/cloud-contract.enc.yaml`.
The private site must not depend on anything else about the cloud side.

| Key | Meaning |
|---|---|
| wireguard.server_endpoint | address and port of the WireGuard server |
| wireguard.server_public_key | public key of the cloud peer |
| wireguard.tunnel_cidr | addresses used inside the tunnel |
| wireguard.cloud_network_cidr | network behind the peer that the private site must route through the tunnel |
| s3.endpoint_url | S3 endpoint reachable through the tunnel |
| s3.region | region string expected by S3 clients |
| s3.path_style | true: path-style addressing in both implementations |
| s3.ca_certificate | optional CA certificate (needed for a self-signed endpoint) |
| s3.bucket | bucket name |
| s3.access_key / s3.secret_key | credentials limited to that bucket |
