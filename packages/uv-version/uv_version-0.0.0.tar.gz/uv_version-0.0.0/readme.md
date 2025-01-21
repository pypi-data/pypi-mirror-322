# uv-version

CLI tool for managing package version

[![PyPI](https://img.shields.io/pypi/v/uv-version)](https://pypi.org/project/uv-version/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-version)](https://pypi.org/project/uv-version/)
[![uvxt](https://img.shields.io/badge/family-uvxt-purple)](https://pypi.org/project/uvxt/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uv-version&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_uv-version)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_uv-version&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_uv-version)

[![Downloads](https://static.pepy.tech/badge/uv-version)](https://pepy.tech/project/uv-version)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/uv-version)](https://gitlab.com/rocshers/python/uv-version)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/uv-version)](https://gitlab.com/rocshers/python/uv-version)

## Functionality

- Parsing: `git`, `pyproject.toml`, `env`, `stdin`
- Output to: `pyproject.toml`, `stdout`
- `Increment`

## Quick start

```bash
uvx uv-version increment
```

## Configs

## Commands

### Arguments for using version

- `--to-pyproject`: Set a new version in pyproject.toml. \[Default\]
- `--to-print`: Print the new version to the console.

### Arguments for getting version

- `--from-pyproject`: Version is determined by the value in pyproject.toml project.version \[Default\]
- `--from-git`: Version is determined based on the `git status`
- `--from-stdin`: Version is expected as the last argument of the call or from stdin
- `--from-env`: Version is expected in the environment variable `$PACKAGE_VERSION`.

You can use multiple attributes together.

When retrieving the version from different sources, keep in mind that the **highest version will be used** in the end.

### uvx increment

Increases the version by 1

```bash
$ uvx uv-version --to-print
0.1.1
$ uvx uv-version --to-print increment prerelease
0.1.2a1
$ uvx uv-version --to-print increment micro
0.1.3
$ uvx uv-version --to-print increment minor
0.2.0
$ uvx uv-version --to-print increment major
1.0.0
```

## Use cases

### Publishing python package to pypi via uv with version equal to git tag

.gitlab-ci.yml:

```yaml
pypi:
  stage: publishing
  image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim
  tags:
    - docker
  script:
    - apt install git
    - uvx uv-version --from-git
    - uv build --no-sources
    - uv publish
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

- When creating a git tag: new package with version == {TAG}
- When pushing to CI_DEFAULT_BRANCH: new package with version == {TAG}a{N}

### Publishing python package to private pypi via uv with version equal to git tag and commit hash

.gitlab-ci.yml:

```yaml
pypi:
  stage: publishing
  image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim
  tags:
    - docker
  script:
    - apt install git
    # set alpha version template
    - PACKAGE_VERSION_ALPHA_VERSION_FORMAT='{version}a{distance}+{commit_hash}'
    # Update package version
    - uvx uv-version --from-git
    # Publishing to gitlab
    - UV_PUBLISH_URL=https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/packages/pypi
    - UV_PUBLISH_TOKEN=${PYPI_TOKEN}
    - uv build --no-sources
    - uv publish
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

- When creating a git tag: new package with version == {TAG}
- When pushing to CI_DEFAULT_BRANCH: new package with version == {TAG}a{N}+{COMMIT_HASH}

## Roadmap

- logging
- tests
- version construct
- Set to `__init__`, `__version__`,`VERSION` files

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/uv-version/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/uv-version>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
