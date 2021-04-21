# order of libs is meaningful. First, we install libs without internal dependencies that other libs depend on.
libs := downloads downloads_infrastructure common

define install_dev
	pip install -e manager/$(1)

endef

.PHONY: dev
dev:
	pip install --use-feature=2020-resolver -r requirements.txt
	$(foreach lib,$(libs),$(call install_dev,$(lib)))

.PHONY: freeze-deps
freeze-deps:
	pip install pip-tools==6.1.0
	pip-compile --upgrade --output-file=requirements.txt $(foreach lib,$(libs), ./manager/$(lib)/requirements.txt ./manager/$(lib)/requirements-dev.txt)
