---
title: "Declare action inputs, tools, environment, and resources"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["actions/declaring-actions.md", "core/outputs-and-runfiles.md"]
claim_ids: ["actions.inputs.contract", "actions.inputs.runfiles", "actions.inputs.exec", "actions.environment.defaults", "actions.resources.local", "actions.inputs.unused", "actions.inputs.platform"]
last_verified: "2026-11-05"
---

# Declare action inputs, tools, environment, and resources

Use this page to review the complete contract of an action that runs an executable.
A useful review starts with everything the process can read and everything it
must produce.

## Separate ordinary inputs from executable tools

`run()` receives ordinary `inputs`, declared `outputs`, an `executable`, optional
additional `tools`, and `arguments`. Inputs can be a list or depset of files.
Tools are also inputs, but can carry runtime support files. A path in the argument
list does not supply either kind of dependency. [Action API][actions]

The executable may be a `File`, a `FilesToRunProvider`, or a string path. Prefer a
declared tool dependency or toolchain value that includes its runtime contract.
A string path names a command without describing a tool distribution.
[API][actions], [executable handling][action-impl]

For tools passed in a list, direct `FilesToRunProvider` entries and `File` entries
obtained from `ctx.executable` have their runfiles added automatically. The list
can also contain depsets of files, but those are not interchangeable with a
provider carrying runfiles. Preserve the provider when that is the tool interface
you have. [Tool contract][actions], [registration][action-impl]

Our recommendation: declare a fixed executable dependency using an executable
label attribute configured for execution (`cfg = "exec"`). An executable attribute
requires an explicit configuration; a tool must run on the action's execution
platform, which can differ from the platform of the product being built.
[Attribute API][attr]

## Keep environment inputs deliberate

`use_default_shell_env` defaults to `False`. The `env` dictionary supplies explicit
variables. When default-shell environment is enabled, it includes OS-dependent
variables and `--action_env` values; explicit `env` values take precedence.
This is an action environment, not an instruction to inherit every variable from
the invoking shell. [Defaults][actions], [environment branch][action-impl]

Our recommendation: make behavior-changing environment values explicit and stable.
Do not make success depend on a developer's ambient `PATH`, locale, or private
configuration. When a toolchain requires an environment, pass the environment
provided by its supported API and record that dependency.

`execution_requirements` describes scheduling requirements. `toolchain` names the
toolchain type supplying the action's tools; set it to `None` when there is no such
toolchain. If `exec_group` is also supplied, that group selects the execution platform.
When automatic execution groups are active, the implementation checks that the
named group declares the supplied toolchain type. Read the
[toolchain consumer](../toolchains/consuming.md) contract before combining these
choices. [Action API][actions], [group-selection checks][action-impl]

## Treat resource estimates as scheduler inputs

At Bazel 9.3.1, `resource_set` accepts either a dictionary or a top-level callback.
The supported entries are `cpu`, `memory` in MB, and `local_test`; defaults are
1 CPU, 250 MB, and 1 local-test unit. A callback receives an OS-name string and an
input count. These estimates apply to local scheduling; they do not define a
remote worker's hardware contract or make undeclared tools available.
[Resource API][actions], [validation and parsing][action-impl]

Our recommendation: change estimates only with measurements of the actual tool and
workload. More parallelism is not evidence that an action is correctly declared.

## Use input-pruning features only with their full contract

`unused_inputs_list` refers to a file listing inputs unused by the action. Its
contract is stronger than “the compiler did not mention this file”: changing a
listed file must not affect any output. Keep a conservative input declaration
until that property has been established for the tool. [API][actions]

Continue with [directories and symlinks](directories-and-symlinks.md), then
[hermeticity](hermeticity-and-reproducibility.md).

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[action-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java
[attr]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java
