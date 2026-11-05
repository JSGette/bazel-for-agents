---
title: "Choose Python runtimes and toolchain versions"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_python": "2.4.6"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md"]
claim_ids: ["python.setup.exports", "python.setup.defaults", "python.setup.version", "python.setup.overrides"]
last_verified: "2026-11-05"
---

# Choose Python runtimes and toolchain versions

## Use this when

Add Python build targets, select an interpreter, or run several Python versions
in one dependency graph. Record the Bazel, `rules_python`, interpreter, and
package-lock versions separately.

## Public entry points

Load `py_library`, `py_binary`, and `py_test` from their respective
`@rules_python//python:py_library.bzl`, `:py_binary.bzl`, and `:py_test.bzl`
files. Configure runtimes with the `python` extension at
`@rules_python//python/extensions:python.bzl`.
[Library export](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/py_library.bzl);
[Binary export](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/py_binary.bzl);
[Test export](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/py_test.bzl);
[Extension export](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/extensions/python.bzl).

Repository recommendation: specify a deliberate default runtime in the root
module with `python.defaults`, and declare the required runtime with
`python.toolchain`. The ruleset provides a convenience default and registers
`@pythons_hub//:all`, but its own module warns that the default version changes
with releases. Do not treat upgrading the ruleset as an intentional interpreter
upgrade. [Default runtime and registration](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/MODULE.bazel);
[Default and toolchain processing](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl).

## Default selection and per-target selection

`python.defaults` can obtain a version from an explicit value, project metadata,
a version file, or an environment variable. If using those inputs, record them
as part of configuration. For reproducible project guidance, prefer an explicit
version unless the project deliberately centralizes it in a checked-in file.
[_compute_default_python_version](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl).

`py_binary` and `py_test` accept `python_version` values in `X.Y` or `X.Y.Z`
form. They inherit the incoming configuration when the attribute is omitted.
Declaring the attribute does not install a runtime: a matching toolchain must
exist, and the API warns that otherwise the value may be ignored or resolution
may fail depending on the toolchain setup.
[Version attribute contract](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl).

The runtime extension maps minor versions to concrete versions and supports
multiple registered versions. Record the actual resolved patch and distribution,
not just a minor selector, when reporting verification.
[Version expansion and hub construction](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl).

## Library-module responsibilities

A reusable module that can use the consumer's Python default can depend on the
ruleset and use the normal public rules. A module whose tools require a specific
runtime should declare that runtime and pin the tools' `python_version`.
Use development-only module dependencies/extensions only for tools needed to
develop the module itself. [Library-module cases](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/docs/toolchains.md).

Runtime overrides exist at global, single-version, and single-version/platform
scopes. Custom distributions require matching URLs, digests, layout, and target
constraints; an override is a separate integration to verify, not merely a
version label. [Override validation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl).

Continue with [targets](targets.md), [dependencies](dependencies.md), and
[native extensions](native-extensions.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#python-setup).
