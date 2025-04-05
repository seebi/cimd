<!-- markdownlint-disable MD012 MD013 MD024 MD033 -->
# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/)

## [Unreleased]

### Changed

- tables are rendered by rich now (#2)

### Fixed

- list command does not create zero-item JSON files anymore (#3)


## [0.11.1] 2025-03-21

### Fixed

- shields.io API: missing path encoding of special chars (e.g. %)


## [0.11.0] 2025-03-21

### Added

- `--version` root option to show the version and exit
- `delete` command:
  - option `--field` to optionally change the target of the expression pattern
- `extend gitlab-link` command:
  - option `--field` to optionally change the target of the expression pattern

### Changed

- `extend coverage-xml` command:
  - item key now `coverage-xml-line-rate`


## [0.10.1] 2025-03-21

### Fixed

- `extract junit-xml` command:
  - fix description of extracted items


## [0.10.0] 2025-03-20

### Added

- `extract coverage-xml` command:
  - Extract metadata from a Coverage XML output files


## [0.9.1] 2025-03-19

### Fixed

- fix README for pypi.org


## [0.9.0] 2025-03-19

### Added

- `extract junit-xml` command:
  - Extract metadata from a JUnit XML output files

### Fixed

- shields.io API: proper handling of spaces


## [0.8.2] 2025-03-18

### Fixed

- `extend gitlab-link` command:
  - correct handling of job URL parts


## [0.8.1] 2025-03-17

### Fixed

- `extend gitlab-link` command:
  - exception when using `CI_JOB_URL` environment variable


## [0.8.0] 2025-03-17

### Added

- `extend` command group:
  - `gitlab-link` command - extend metadata items with a raw gitlab artifact link

### Changed

- `delete` command:
  - key argument now a key expression argument, to allow deletion of multiple items


## [0.7.0] 2025-03-17

### Added

- `extract trivy-scan` command:
  - `--all` option to extract all vulnerability groups
  - `--severity` option to extract an explicit vulnerability group

### Fixed

- even extraction of zero keys will result in a metadata file


## [0.6.2] 2025-02-05

### Added

- docker image available: [`seebi/cimd`](https://hub.docker.com/repository/docker/seebi/cimd/)


## [0.6.1] 2025-02-04

### Fixed

- `extract trivy-scan` command:
  - model error on empty results and vulnerabilities list


## [0.6.0] 2025-02-04

### Added

- `extract` command group:
  - `trivy-scan` command - extract metadata from a trivy scan JSON output file
- api to prepare shields.io image links

### Changed

- `scratch` command group
  - rename to `extract`


## [0.5.1] 2025-01-04

### Added

- initial version
- basic crud commands:
  - `add` - Add a metadata item
  - `delete` - Delete metadata items
  - `get` - Get data of a metadata item
  - `list` - List metadata items
- `scratch` command group:
  - `pipeline-logs` command - extract metadata from gitlab pipeline job logs

