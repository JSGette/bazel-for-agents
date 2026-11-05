---
title: "Consume a resolved toolchain"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/providers.md", "actions/declaring-actions.md", "configuration/platforms-and-constraints.md"]
claim_ids: ["toolchains.requirement", "toolchains.provider", "toolchains.action-association", "toolchains.tool-dependencies"]
last_verified: "2026-11-05"
---

# Consume a resolved toolchain

Use this when writing a rule that needs a compiler, generator, SDK, or other
platform-dependent tool. Our recommendation is to consume a documented toolchain
interface rather than discover tools from a machine's `PATH` during analysis.

## Request a type, then read its provider

Declare required toolchain types in the rule's `toolchains` parameter. A plain
label names a mandatory type; `config_common.toolchain_type` makes mandatory or
optional status explicit. Its `mandatory` argument defaults to `True`.
[Rule declaration][rule-api], [requirement API][config-common]

In the implementation, use `ctx.toolchains[toolchain_type_label]` to retrieve the
resolved `platform_common.ToolchainInfo`. The label identifies a toolchain type,
not the implementation target or the registration wrapper. Fields on the returned
provider belong to that toolchain's contract; Bazel does not prescribe a universal
`compiler`, `tool`, or `sdk` field. [Context API][toolchain-context], [provider API][toolchain-info]

When an optional type has no selected implementation, its value is `None`. Test
for that case before accessing its fields and define what the rule does without
it. Requesting an undeclared type is an error. Do not turn a missing mandatory
toolchain into a shell lookup fallback. [Toolchain context contract][toolchain-context],
[resolved provider loading][resolved], [lookup validation][lookup]

## Associate each action with the tool it uses

For `ctx.actions.run` and `run_shell`, pass the toolchain type through the action's
`toolchain` argument when the executable or tools come from that toolchain. If
they do not come from a toolchain, use `toolchain = None`. The argument describes
where the tools came from so Bazel can select the corresponding execution group;
it is not a request to resolve an undeclared type. [Action API][action-api],
[group selection implementation][action-impl]

For a named group, read the toolchain through
`ctx.exec_groups[group_name].toolchains[type_label]` and select that same group on
the action. If an action needs two toolchain types on one execution platform,
request both in one named group. See [execution groups](execution-groups.md) for
automatic-group defaults and combined `exec_group`/`toolchain` behavior.
[Execution group API][exec-guide], [group selection][action-impl]

## Preserve the complete execution dependency

A tool's path is not its complete input closure. Pass the executable and its
runtime support through the appropriate `File`/`FilesToRunProvider` interfaces,
and declare other files the action reads as inputs or tools. The action API's
`tools` handling can bring in runfiles for files-to-run providers; a string path
does not provide that dependency information. [Action input and tool contract][action-api]

If a rule uses a fixed executable dependency instead of a toolchain, declare an
executable label attribute configured for execution. Keep the distinction explicit:
a private executable attribute is a dependency, while a toolchain requirement is
resolved against platforms and registrations. [Executable attribute API][attr-api]

## Inspect the effective selection

Before blaming an action command, establish the requested type, target platform,
execution group, selected execution platform, selected implementation, and required
provider fields. A different compatible registration can satisfy the same type.
A toolchain provider can carry paths, files, executables, or nested providers, so
check the particular ruleset's schema instead of copying a neighboring language's
field accesses. [Resolution implementation][resolved], [provider interface][toolchain-info]

Continue with [resolution](resolution.md) when selection is surprising, or
[defining and registering](defining-and-registering.md) when creating an interface.

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[rule-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
[config-common]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/ConfigStarlarkCommonApi.java
[toolchain-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainContextApi.java
[toolchain-info]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java
[resolved]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/ResolvedToolchainContext.java
[action-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[action-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java
[exec-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/exec-groups.md
[attr-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java
[lookup]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkToolchainContext.java
