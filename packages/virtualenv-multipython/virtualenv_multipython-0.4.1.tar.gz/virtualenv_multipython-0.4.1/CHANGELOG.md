# Changelog

All notable changes to this project will be documented in this file. Changes for the *upcoming release* can be found in [News directory](https://github.com/makukha/virtualenv-multipython/tree/main/src/NEWS.d).

* The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
* This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

<!-- towncrier release notes start -->

## [v0.4.1](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.4.1) — 2025-01-21

***Changed:***

- Use stdlib `logging` when `loguru` is not installed ([#48](https://github.com/makukha/virtualenv-multipython/issues/48))

***Fixed:***

- Bug when system executable was not selected for some Python versions ([#48](https://github.com/makukha/virtualenv-multipython/issues/48))

***Misc:***

- Started using  [just](https://just.systems) ([#48](https://github.com/makukha/virtualenv-multipython/issues/48))
- Switched tests from Docker Bake to shell scripts and [GNU parallel](https://www.gnu.org/software/parallel) ([#48](https://github.com/makukha/virtualenv-multipython/issues/48))


## [v0.4.0](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.4.0) — 2025-01-19

***Breaking 🔥***

- When no version is requested, use `sys.executable` ([#38](https://github.com/makukha/virtualenv-multipython/issues/38))

***Fixed:***

- Fixed command line invocation without python version request ([#38](https://github.com/makukha/virtualenv-multipython/issues/38))

***Misc:***

- Refactored tests ([#43](https://github.com/makukha/virtualenv-multipython/issues/43))


## [v0.3.2](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.3.2) — 2025-01-18

***Added 🌿***

- Debug mode, if installed with extra `virtualenv-multipython[debug]` and set env variable `MULTIPYTHON_DEBUG=true` ([#39](https://github.com/makukha/virtualenv-multipython/issues/39))

***Fixed:***

- Inconsistent behaviour when Python interpreter requested by executable path was ignored ([#38](https://github.com/makukha/virtualenv-multipython/issues/38))

***Docs:***

- Updated docs generation process with new features in [docsub](https://github.com/makukha/docsub) v0.8.0 ([#34](https://github.com/makukha/virtualenv-multipython/issues/34))

***Misc:***

- Added more realistic test case ([#38](https://github.com/makukha/virtualenv-multipython/issues/38))


## [v0.3.1](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.3.1) — 2025-01-12

***Fixed:***

- Possible bug caused by unconditionally using `utf-8` for `py bin` results ([#28](https://github.com/makukha/virtualenv-multipython/issues/28))

***Misc:***

- Fixed cross testing charts display ([#30](https://github.com/makukha/virtualenv-multipython/issues/30))
- Improved testing Dockerfile structure ([#33](https://github.com/makukha/virtualenv-multipython/issues/33))


## [v0.3.0](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.3.0) — 2025-01-12

***Added 🌿***

- Support for Python 2.7, 3.5, 3.6 ([#24](https://github.com/makukha/virtualenv-multipython/issues/24))

***Changed:***

- Updated tests to generate test matrix docs ([#20](https://github.com/makukha/virtualenv-multipython/issues/20))

***Docs:***

- Added test matrix similar to [tox-multipython](https://github.com/makukha/tox-multipython) ([#20](https://github.com/makukha/virtualenv-multipython/issues/20))

***Misc:***

- Tests are now linted with [Hadolint](https://github.com/hadolint/hadolint) ([#22](https://github.com/makukha/virtualenv-multipython/issues/22))
- Added virtualenv-only test setup ([#24](https://github.com/makukha/virtualenv-multipython/issues/24))


## [v0.2.1](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.2.1) — 2025-01-09

***Fixed:***

- Project metadata ([#16](https://github.com/makukha/virtualenv-multipython/issues/16))


## [v0.2.0](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.2.0) — 2025-01-09

***Breaking 🔥***

- Support for Python 2.7, 3.5, 3.6 passed to [tox-multipython](https://github.com/makukha/tox-multipython) ([#8](https://github.com/makukha/virtualenv-multipython/issues/8)) — by @makukha in #11

***Misc:***

- Tests for Python 3.7+ ([#5](https://github.com/makukha/virtualenv-multipython/issues/5)) — by @makukha in #10
- Linting with [mypy](https://mypy.readthedocs.io) and [ruff](https://docs.astral.sh/ruff) ([#6](https://github.com/makukha/virtualenv-multipython/issues/6)) — by @makukha in #7

***Fixed:***

- Multiple issues, not detected before using `py tag` and Docker test matrix ([#5](https://github.com/makukha/virtualenv-multipython/issues/5), [#8](https://github.com/makukha/virtualenv-multipython/issues/8)) — by @makukha in #10, #11


## [v0.1.2](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.1.2) — 2025-01-04

***Misc:***

- Fix docs and metadata — by @makukha ([#3](https://github.com/makukha/virtualenv-multipython/issues/3))


## [v0.1.1](https://github.com/makukha/virtualenv-multipython/releases/tag/v0.1.1) — 2025-01-04

***Misc:***

- Migrate to separate repository — by @makukha ([#1](https://github.com/makukha/virtualenv-multipython/issues/1))


## [v0.1.0](https://github.com/makukha/docsub/releases/tag/v0.1.0) — 2024-01-03

***Added 🌿***

- Initial release — by @makukha ([#47](https://github.com/makukha/multipython/issues/47))
