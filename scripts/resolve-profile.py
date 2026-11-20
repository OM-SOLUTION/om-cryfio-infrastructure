#!/usr/bin/env python3
"""Merge config.example.yaml with a profile, write build/<profile>/config.yaml, print a summary."""
import os, sys
import yaml


def merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            merge(base[k], v)
        else:
            base[k] = v
    return base


def flatten(d, prefix=""):
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            yield from flatten(v, key + ".")
        else:
            yield key, v


def main():
    name = sys.argv[1]
    quiet = "--quiet" in sys.argv
    get = sys.argv[sys.argv.index("--get") + 1] if "--get" in sys.argv else None
    own = f"profiles/{name}.yaml"
    example = f"profiles/{name}.example.yaml"
    src = own if os.path.exists(own) else example
    if not os.path.exists(src):
        sys.exit(f"unknown profile '{name}'")
    cfg = yaml.safe_load(open("config.example.yaml", encoding="utf-8"))
    cfg = merge(cfg, yaml.safe_load(open(src, encoding="utf-8")))
    provider = cfg["cloud"]["provider"]
    cloud_dir = {"selfhosted": "cloud-site/selfhosted/terraform", "aws": "cloud-site/aws"}.get(provider, "(undefined)")
    if get:
        print({"cloud_dir": cloud_dir, "provider": provider}[get])
        return
    os.makedirs(f"build/{name}", exist_ok=True)
    yaml.safe_dump(cfg, open(f"build/{name}/config.yaml", "w", encoding="utf-8"), sort_keys=False)
    if quiet:
        return
    skip = []
    if cfg["tls"]["mode"] == "selfsigned":
        skip.append("acme.")
    if provider != "aws":
        skip.append("cloud.aws.")
    placeholders = ("TODO", "CHANGEME", "example.com")
    todo = [k for k, v in flatten(cfg)
            if not any(k.startswith(s) for s in skip)
            and (v in ("", None) or (isinstance(v, str) and any(t in v for t in placeholders)))
            and k not in ("private_site.backend.image", "private_site.backend.tag")]
    tls = cfg["tls"]["mode"]
    tls_text = f"{tls} ({cfg['acme']['environment']})" if tls == "letsencrypt" else f"{tls} (cert-manager local CA)"
    print(f"Plan:            {name}  (from {src})")
    print(f"Cloud site:      {provider}  ->  {cloud_dir}")
    print(f"Private site:    k3s, kubeconfig {cfg['private_site']['kubeconfig']}")
    print(f"Certificates:    {tls_text}")
    print(f"Domain:          {cfg['domain']}   api.{cfg['domain']}  s3.{cfg['domain']}")
    print(f"Object store:    {cfg['object_store']['type']}")
    print(f"Merged config:   build/{name}/config.yaml")
    print(f"State:           state/{name}/        Secrets: secrets/{name}/")
    print("Steps:           make cloud -> make server -> make cluster -> make check")
    print(f"Still to fill in ({len(todo)}): " + (", ".join(todo) if todo else "nothing"))


main()
