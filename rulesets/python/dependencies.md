---
title: "Resolve Python packages, hubs, and platform variants"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_python": "2.4.6"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/python/setup.md", "rulesets/python/targets.md"]
claim_ids: ["python.dependencies.hubs", "python.dependencies.locks", "python.dependencies.platforms", "python.dependencies.labels", "python.dependencies.sources"]
last_verified: "2026-11-05"
---

# Resolve Python packages, hubs, and platform variants

## Use this when

Add a Python distribution, choose wheel variants, maintain lock inputs, or explain
why packages differ by interpreter or platform.

## Use the current hub model

The `pip` extension is exported at `@rules_python//python/extensions:pip.bzl`.
`pip.parse` associates a concrete `hub_name`, Python version, and dependency
inputs. Multiple Python versions can share a hub name in one module. Concrete
hub names must be unique across modules, so reusable modules should include
their own name. Separate hubs represent separate resolutions and should not be
mixed casually in one program. [parse and hub_name contracts](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl).

In this release, `pypi` is reserved for the unified proxy hub; using it as a
concrete `pip.parse` hub is deprecated. Choose a distinct concrete name and
import it with `use_repo`. The unified `@pypi` repository can route package
references to configured hubs, with `pip.default.default_hub` controlling the
default. A `pip.dep` abstract declaration ensures a package target exists but
does not supply its implementation; an unresolved declaration fails when built.
[Unified hub, defaults and dep tag](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl).

## Lock the dependency input deliberately

Requirements files are supported through `requirements_lock` and
`requirements_by_platform`. This release also has `pip.parse.uv_lock`; the
implementation reads it as the primary package-metadata source. Do not repeat
the stale claim that only requirements.txt is supported. Package source kinds
and platform filtering still have implementation-specific handling; this page
does not claim that every possible uv project layout works unchanged.
[uv_lock API](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl);
[Lock parsing and package filtering](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/parse_requirements.bzl).

`compile_pip_requirements`, exported from `@rules_python//python:pip.bzl`,
maintains a pinned requirements file and supplies update/check targets. The
separate `@rules_python//python/uv:lock.bzl` API is marked experimental and has
a different output/check contract. Use the project's chosen lock workflow and
review hashes and build-system dependencies alongside application dependencies.
[Public pip helper exports](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/pip.bzl);
[Lock workflows and limitations](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/docs/pypi/lock.md).

## Match Python and target platform

`pip.parse.python_version` must match a configured Python toolchain unless an
interpreter is supplied explicitly. It is separate from OS, architecture, libc,
and threading variants. `target_platforms` controls which named pip variants
are evaluated; when unset, hub construction uses the host `{os}_{arch}`
placeholder. Setting a target Bazel platform does not retroactively fetch every
needed wheel variant. [Version/platform attrs](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl);
[Platform evaluation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/hub_builder.bzl).

`requirements_by_platform` maps files to pip platform names, including patterns.
These names are extension configuration names, not Bazel `platform` target
labels. `pip.default` can associate a named variant with configuration settings.
For cross builds, explicitly cover the intended variants and inspect the aliases
selected in the configured graph.
[Requirements map](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/pip_repository_attrs.bzl);
[Configured package aliases](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/pkg_aliases.bzl).

## Consume packages and handle native distributions

A concrete hub exposes package library labels such as `@project_pip//numpy`,
plus `:data`, `:dist_info`, `:extracted_whl_files`, and `:whl` targets. Upstream
now recommends direct labels over adding the `requirement()` indirection.
Use the dedicated `py_console_script_binary` interface for wheel console entry
points. [Consumer interfaces](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/docs/pypi/use.md).

`download_only` disables building wheels from source. Source distributions can
introduce build tools and host-dependent build behavior; they are not made
cross-compilable just by selecting a target wheel platform. `pip.whl_mods`
changes generated BUILD metadata; `pip.override` applies distribution patches
by filename. Keep those interventions reviewable and verify the resulting
import/native-loading behavior. [Download/build boundary](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/attrs.bzl);
[Modification and patch contracts](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#python-dependencies).
