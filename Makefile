PIP_OPTIONS =
NOSE_OPTIONS =

.PHONY: FORCE_MAKE

.PHONY: default
default: list

## list targets (help) {{{
.PHONY: list
# https://stackoverflow.com/a/26339924/2239985
list:
	@echo "This Makefile has the following targets:"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^(:?[^[:alnum:]]|FORCE_MAKE$$)' -e '^$@$$' | sed 's/^/    /'
## }}}

## Fail when git working directory for the Make prerequisites has changed.
.PHONY: check
check: check-nose2

# git diff --quiet --exit-code HEAD -- $^

.PHONY: check-nose
check-nose:
	nosetests3 $(NOSE_OPTIONS)

.PHONY: check-nose2
check-nose2:
	(nose2-3 --start-dir tests $(NOSE_OPTIONS) || nose2-3.4 --start-dir tests $(NOSE_OPTIONS))

## Git hooks {{{
.PHONY: install-pre-commit-hook
install-pre-commit-hook: ./docs/_prepare/hooks/pre-commit
	ln -srf "$<" "$(shell git rev-parse --git-dir)/hooks"

.PHONY: run-pre-commit-hook
run-pre-commit-hook: ./docs/_prepare/hooks/pre-commit
	"$<"

.PHONY: remove-pre-commit-hook
remove-pre-commit-hook:
	rm -f "$(shell git rev-parse --git-dir)/hooks/pre-commit"
## }}}
