# Secrets

Passwords, keys and connection details, encrypted with SOPS so they are safe to commit. One folder per
plan (`secrets/<profile>/`), created when the plan is first used. The age private key that decrypts them
is never stored here or in git.
