# Changelog

All notable changes to this project will be documented in this file. Changes for the *upcoming release* can be found in [News directory](https://github.com/makukha/tox-multipython/tree/main/src/NEWS.d).

* The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
* This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

<!-- towncrier release notes start -->

## [v0.2.2](https://github.com/makukha/tox-multipython/releases/tag/v0.2.2) — 2025-01-22

***Changed:***

- Use stdlib `logging` when `loguru` is not installed ([#23](https://github.com/makukha/tox-multipython/issues/23))

***Misc:***

- Switched tests from Docker Bake to shell scripts and [GNU parallel](https://www.gnu.org/software/parallel) ([#23](https://github.com/makukha/tox-multipython/issues/23))
- Started using [just](https://just.systems) ([#23](https://github.com/makukha/tox-multipython/issues/23))


## [v0.2.1](https://github.com/makukha/tox-multipython/releases/tag/v0.2.1) — 2025-01-19

***Added 🌿***

- Debug mode, if installed with extra `tox-multipython[debug]` and set env variable `MULTIPYTHON_DEBUG=true` ([#17](https://github.com/makukha/tox-multipython/issues/17))

***Misc:***

- Added more realistic test cases ([#18](https://github.com/makukha/tox-multipython/issues/18))


## [v0.2.0](https://github.com/makukha/tox-multipython/releases/tag/v0.2.0) — 2025-01-12

***Changed:***

- Use `py bin --path` to discover interpreter ([#10](https://github.com/makukha/tox-multipython/issues/10))

***Docs:***

- Added test report ([#7](https://github.com/makukha/tox-multipython/issues/7))

***Misc:***

- Tests are now linted with [Hadolint](https://github.com/hadolint/hadolint) ([#6](https://github.com/makukha/tox-multipython/issues/6))
- Fixed testing bug with not pinned tox version ([#5](https://github.com/makukha/tox-multipython/issues/5))
- Added test setups with pinned `virtualenv` ([#7](https://github.com/makukha/tox-multipython/issues/7))


## [v0.1.0](https://github.com/makukha/tox-multipython/releases/tag/v0.1.0) — 2025-01-10

***Added 🌿***

- Initial release ([#1](https://github.com/makukha/tox-multipython/issues/1))
