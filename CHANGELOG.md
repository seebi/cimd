# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/)

## [0.8.0] 2025-03-17

### Added

- `extend` command group:
  - `gitlab-link` command - extend metadata items with a raw gitlab artifact link.

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
  - `add` - Add a metadata item.
  - `delete` - Delete metadata items.
  - `get` - Get data of a metadata item.
  - `list` - List metadata items.
- `scratch` command group:
  - `pipeline-logs` command - extract metadata from gitlab pipeline job logs.
