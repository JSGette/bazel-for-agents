---
title: "Model Python sources, imports, tests, and runfiles"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_python": "2.4.6"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/python/setup.md", "core/outputs-and-runfiles.md"]
claim_ids: ["python.targets.files", "python.targets.entry", "python.targets.init", "python.targets.runfiles", "python.targets.precompile"]
last_verified: "2026-11-05"
---

# Model Python sources, imports, tests, and runfiles

## Use this when

Add an importable package, application entry point, test, or runtime resource.

## Keep source, dependency, and runtime relationships explicit

| Attribute | Role |
| --- | --- |
| `srcs` | Python source inputs owned by the target |
| `deps` | Library dependencies; the rule accepts Python and supported C/C++ provider interfaces |
| `data` | Files and targets needed at runtime |
| `imports` | Additional import directories, propagated to consumers |

`imports` is interpreted relative to the target's directory in the runfiles
layout. It affects this target and reverse dependencies, not the libraries this
target depends on. Absolute or escaping paths are rejected. Repository
recommendation: use it to express intentional package roots, not to hide missing
`deps` or depend on a developer's `PYTHONPATH`.
[Source, dependency, data and imports schemas](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/attributes.bzl).

## Choose the executable entry point

`main` identifies a source file that must also be in `srcs`; if omitted, the
rule derives a filename from the target name. `main_module` instead selects a
Python module to execute, and the module can come from a dependency without
local `srcs`. The two attributes are mutually exclusive.
[main and main_module](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl).

A `py_test` uses the executable rule machinery with test semantics. Choose its
entry point deliberately: declaring test files alone does not specify an
arbitrary third-party test runner's discovery configuration.
[Public test wrapper](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/py_test.bzl);
[Test rule construction](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_test_rule.bzl).

## Package initialization and runtime resources

Decide whether a package uses explicit `__init__.py` files or namespace-package
semantics. The executable `legacy_create_init` attribute's auto mode consults
module-level `explicit_init_py` configuration and the relevant flag. With
implicit creation disabled, ordinary package initialization files must be
listed as sources where needed. Do not assume an interpreter's import behavior
is independent of the launcher-created runfiles tree.
[Initialization policy](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl).

The `@rules_python//python/runfiles` library exports `runfiles.Create`,
`Rlocation`, `CurrentRepository`, and `EnvVars` behavior. Use logical lookup
with repository mapping instead of synthesizing an external-directory name.
Propagate the returned environment when a subprocess also needs runfiles.
[Library target](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/runfiles/BUILD.bazel);
[Lookup and propagation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/runfiles/runfiles.py).

## Bytecode is an explicit build choice

`precompile` can inherit, enable, or disable build-time bytecode compilation.
Separate attributes govern invalidation checks, optimization, and retaining
source files. Executables also expose `pyc_collection` for dependency bytecode.
Repository recommendation: validate startup and packaging behavior before
omitting sources; source presence can be relevant to application behavior.
[Precompile contracts](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/attributes.bzl);
[pyc_collection contract](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl).

Continue with [locked dependencies](dependencies.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#python-targets).
