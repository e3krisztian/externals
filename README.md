# Externals

Externals is intended to be a light abstraction of hierarchically named
resources, potentially external to the current process.

Goal: provide a common, minimal interface for accessing, discovering, creating
and destroying data on common resource providers.

It is definitely not the intention to provide a rich set of operations.


## Explicit goals:

- simple access to content - both read and write
- easy discovery of namespace
- create new content
	- temporary storage
	- save output
- destroy content
	- free temporary storage


## Explicit non-goals:

- access to security attributes - security is service dependent
- support for efficient service side reorganization of the namespace - by
  moving, duplicating content - these operations require more than one resource
  path

## Development

### Run Tests
Use `tox` to run the tests:

    tox
