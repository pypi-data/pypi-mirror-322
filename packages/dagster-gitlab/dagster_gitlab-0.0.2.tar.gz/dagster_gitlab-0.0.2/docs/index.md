# Home

This library provides an integration with GitLab for Dagster.

!!! note

    This project is **not** affiliated with Dagster.

It provides a thin wrapper around the `python-gitlab` SDK with a REST or GraphQL client.
It integrates with convienient Dagster features by providing configurable resources and run sensors so that you can alert and control GitLab issues from Dagster.

## Inspiration

It is inspired largely by `dagster-github` for the resources, and `dagster-slack` and `dagster-msteams` for the sensors.

The library is intended to be familiar for Dagster users that have used those other integrations, while remaining familiar to GitLab users.

## Versioning

The project does not follow SemVer.
For the foreseeable future, it will always be behind the official Dagster integrations version.

- **Major** - not planning on bumping this
- **Minor** - what most projects would consider "major", along with large feature sets
- **Patch** - Any small change, including some new features and bug fixes

## Roadmap

- `v0.2` is targeting feature parity with `dagster-github` using the REST client
- `v0.3` is targeting feature similarity with `dagster-slack` and `dagster-msteams`
- `v0.4` is targeting feature parity with `dagster-github` using the GraphQL client
