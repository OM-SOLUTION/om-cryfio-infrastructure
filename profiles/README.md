# Profiles

One file per deployment plan. A profile holds only what differs from the defaults in
`config.example.yaml`; `make` merges the two into `build/<profile>/config.yaml`, which Terraform
and the chart read.

| Profile | Private site | Cloud site | Public domain | Use |
|---|---|---|---|---|
| `local` | Server on the local network | Self-hosted server on the local network | No (self-signed certificates) | First baseline, test data only |

To use a plan: copy `<name>.example.yaml` to `<name>.yaml` (git-ignored), fill in the values, then run
`make plan PROFILE=<name>`. Terraform state, secrets and the kubeconfig are kept per plan
(`state/<name>/`, `secrets/<name>/`, the kubeconfig path in the profile), so switching plans never
overwrites another plan.

To add a plan later (for example a VPS private site or the AWS cloud site), add one new
`<name>.example.yaml` here that overrides what differs, and list it in the table above. Nothing else
in the repository has to change.
