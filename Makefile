# Main commands, each for one plan: 'make plan PROFILE=local' shows what a plan will do.
# 'make cloud' sets up the cloud site, 'make server' the private server, 'make cluster' deploys
# onto k3s, 'make check' verifies everything works. Plans are listed by 'make profiles'.
PROFILE ?=
PROFILES := $(basename $(basename $(notdir $(wildcard profiles/*.example.yaml))))
RESOLVE := python3 scripts/resolve-profile.py
NEED_PROFILE = test -n "$(PROFILE)" || { echo "PROFILE is required, for example: make plan PROFILE=local" >&2; echo "Available plans: $(PROFILES)" >&2; exit 2; }

.PHONY: profiles plan cloud server cluster check
profiles:
	@echo "Available plans: $(PROFILES)"; echo "Details: profiles/README.md"
plan:
	@$(NEED_PROFILE)
	@$(RESOLVE) $(PROFILE)
cloud:
	@$(NEED_PROFILE)
	@$(RESOLVE) $(PROFILE) --quiet
	@echo "make cloud [$(PROFILE)]: would apply $$($(RESOLVE) $(PROFILE) --get cloud_dir): not implemented yet" >&2; exit 1
server:
	@$(NEED_PROFILE)
	@echo "make server [$(PROFILE)]: not implemented yet" >&2; exit 1
cluster:
	@$(NEED_PROFILE)
	@echo "make cluster [$(PROFILE)]: not implemented yet" >&2; exit 1
check:
	@echo "make check: not implemented yet" >&2; exit 1
