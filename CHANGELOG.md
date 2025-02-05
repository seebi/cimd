# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/)

## [0.6.2] 2025-02-05

### Added

- docker image available: `seebi/cimd`
  - https://hub.docker.com/repository/docker/seebi/cimd/


## [0.6.1] 2025-02-04

### Fixed

- extract trivy-scan: model error on empty Results and Vulnerabilities list


## [0.6.0] 2025-02-04

### Added

- extract command: trivy-scan
  - Extract metadata from a trivy scan JSON output file
- api to prepare shields.io image links

### Changed

- rename scratch group to extract


## [0.5.1] 2025-01-04

### Added

- initial version
- crud commands: add, delete, get and list
- scratch command: pipeline-logs

