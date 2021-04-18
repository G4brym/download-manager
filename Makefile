# order of libs is meaningful. First, we install libs without internal dependencies that other libs depend on.
libs := downloads downloads_infrastructure main

define install_dev
	pip install -e $(1)

endef

.PHONY: dev
dev:
	pip install --use-feature=2020-resolver -r requirements.txt
	$(foreach lib,$(libs),$(call install_dev,$(lib)))

.PHONY: freeze-deps
freeze-deps:
	pip install pip-tools==6.1.0
	pip-compile --upgrade --output-file=requirements.txt $(foreach lib,$(libs), ./$(lib)/requirements.txt ./$(lib)/requirements-dev.txt)
