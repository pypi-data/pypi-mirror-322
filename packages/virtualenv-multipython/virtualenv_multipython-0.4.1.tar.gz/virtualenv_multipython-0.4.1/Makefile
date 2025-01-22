.PHONY: all
all: pkg samplepkg


.PHONY: pkg
pkg: dist/

dist/: src/ pyproject.toml README.md uv.lock
	uv build .


.PHONY: samplepkg
samplepkg: tests/samplepkg/dist/samplepkg-1-py2.py3-none-any.whl

tests/samplepkg/dist/samplepkg-1-py2.py3-none-any.whl: tests/samplepkg
	uv build tests/samplepkg
