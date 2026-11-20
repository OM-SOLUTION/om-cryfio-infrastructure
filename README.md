# OM-Cryfio infrastructure

Infrastructure for **OM-Cryfio**, a secure file-storage platform. Files are encrypted on the user's Android phone before upload, so the servers only ever hold ciphertext plus readable metadata.

This repository sets up both sites:

- **Private site**: one server running single-node k3s with the backend, PostgreSQL, the object store, Dolibarr, the sync gateway and monitoring.
- **Cloud site**: a WireGuard peer plus a versioned, private, encrypted S3-compatible bucket that holds the encrypted replica and the database backups. No application compute runs there.

The Android app, the Spring Boot backend and the Dolibarr module are developed separately. Until their images exist, the cluster runs placeholders.

> **Status:** skeleton. Every file is a placeholder that describes what it will contain. Nothing has been deployed yet.

## Architecture

```
Android app ──HTTPS (api., s3.)──▶ Private site (k3s) ──WireGuard──▶ Cloud site (bucket)
```

- The phone only talks to the private site, never to the cloud site.
- The private site uses four namespaces separated by NetworkPolicies: `cryfio-app`, `cryfio-data`, `cryfio-admin` and `cryfio-ops`.
  - Traefik ingress with cert-manager.
  - The Spring Boot backend.
  - PostgreSQL through CloudNativePG, with WAL archiving to the cloud bucket.
  - The object store: Garage in production, MinIO as the development placeholder.
  - Dolibarr with its own PostgreSQL, not exposed publicly.
  - An rclone sync CronJob and the WireGuard gateway pod.
  - Prometheus, Grafana and Loki.
- The cloud site has two interchangeable implementations behind one contract:
  - `cloud-site/aws/`: the reference deployment on AWS, with an EC2 WireGuard peer, an S3 bucket, an S3 interface endpoint and IAM.
  - `cloud-site/selfhosted/`: a dedicated server running WireGuard and MinIO, used until AWS is available.

  Switching between them is a configuration change (`cloud.provider`) plus the migration runbook. The only link between the two sites is the set of values listed in [`cloud-site/contract/outputs-schema.md`](cloud-site/contract/outputs-schema.md).

The software requirements specification (SRS) and the architecture diagram are the source of truth and are kept outside this repository. Requirement IDs such as `AR-17` used in this repository refer to that SRS.

## Repository layout

| Path | Contents |
|---|---|
| `cloud-site/` | Cloud site: `contract/` (shared spec), `aws/`, `selfhosted/` |
| `private-site/host/` | One-time server setup: k3s install, hardening, power settings |
| `private-site/terraform/` | Namespaces, secrets, operators, monitoring and the chart, deployed onto the cluster |
| `private-site/charts/cryfio/` | Our own Helm chart; templates grouped by namespace |
| `secrets/` | SOPS-encrypted files, one folder per plan (safe to commit) |
| `scripts/` | WireGuard key generation, smoke test, restore drill, image-tag verification |
| `docs/runbooks/` | Install, upgrade, restore, secret rotation, self-hosted → AWS migration |
| `dev/` | Compose stack (PostgreSQL, MinIO, Dolibarr) for developing before the cluster exists |
| `config.example.yaml` | Defaults shared by every plan |
| `profiles/` | One file per deployment plan (currently `local`); each overrides only what differs from the defaults |

Each folder has its own `README.md` describing what belongs there.

## Requirements

The operator workstation is Linux or WSL. `make` and the scripts are written for bash and do not run in PowerShell or cmd.

Tools: `make`, `terraform` (1.10 or later for the AWS state backend), `kubectl`, `helm`, `sops`, `age`, `wireguard-tools`, plus `awscli` for the AWS cloud site.

Terraform runs from the operator workstation. k3s is installed by script on the private server, outside Terraform.

## Configuration and secrets

1. Pick a plan from `profiles/` (for now `local`). Copy `profiles/<name>.example.yaml` to `profiles/<name>.yaml`. The copy is git-ignored. Fill in every `CHANGEME` and `TODO`.
2. Run `make plan PROFILE=<name>` to see the merged result and what is still unfilled. `make` merges the profile with `config.example.yaml` into `build/<name>/config.yaml`, which Terraform and the chart read.
3. Generate an age key with `age-keygen` and put its public key in `.sops.yaml`. The private key never goes into git.
4. Keep secrets in `secrets/<name>/*.enc.yaml`, always encrypted with SOPS.

Image tags and chart versions under `versions:` are pinned explicitly and checked with `scripts/verify-images.sh`. Never commit a real profile (`profiles/<name>.yaml`), the merged config, the age key, kubeconfigs or Terraform state; `.gitignore` covers them. State, secrets and the kubeconfig are kept per plan, so switching plans never overwrites another plan.

## Usage

```bash
make profiles                 # list the available plans
make plan PROFILE=local       # show what a plan will do and what is still unfilled
make cloud PROFILE=local      # deploy the cloud site
make server PROFILE=local     # set up the private server
make cluster PROFILE=local    # deploy onto the cluster
make check                    # verify the deployment
```

`make profiles` and `make plan` work now. The other targets are not implemented yet; each one currently exits with "not implemented yet".

## Security rules

- Only TCP 80 and 443 are exposed to the internet. The Kubernetes API (6443) and SSH never are.
- The cloud bucket has no public access and is reached only through the WireGuard tunnel.
- No real user data in MinIO.

## Roadmap

| Phase | Scope |
|---|---|
| 0 | Prerequisites: domain, server facts, tools, DNS |
| 1 | Skeleton and placeholders *(done)* |
| 2 | Cloud site (self-hosted first) |
| 3 | Server base: k3s, certificates, network policies |
| 4 | WireGuard link and bucket access |
| 5 | Data layer |
| 6 | Application placeholders and operations |
| 7 | Production readiness, including a restore drill from nothing |
| 8 | Hand-over contract for the backend |

## Team

Youssef EL AFIFI and Mossab MILHA. Academic project at ENSAH Al Hoceïma (Génie Informatique), 2026–2027.
