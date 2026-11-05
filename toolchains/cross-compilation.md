---
title: "Separate build tools from target artifacts"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["configuration/platforms-and-constraints.md", "configuration/transitions.md", "toolchains/consuming.md"]
claim_ids: ["toolchains.cross-platform-model", "toolchains.cross-tool-dependencies", "toolchains.cross-selection", "toolchains.cross-validation"]
last_verified: "2026-11-05"
---

# Separate build tools from target artifacts

Use this when the requested artifact is for a different platform from the machine
running Bazel or its actions. Our recommendation is to trace execution and target
requirements through the dependency graph before changing compiler flags.

## Write down the platform roles

For a build running a compiler on Linux x86_64 to produce a Linux ARM64 binary,
the compiler action's execution platform is Linux x86_64 and the binary's target
platform is Linux ARM64. The host platform describes the Bazel process and need
not be either remote execution platform. A toolchain wrapper can constrain both
sides independently. [Platform roles][platform-guide], [wrapper contract][toolchain-rule]

Selecting a target platform affects resolution; it does not manufacture a cross
compiler, a sysroot, target libraries, or a way to run the produced binary. Those
must be supplied by the ruleset/toolchain integration. Inspect the chosen
implementation and its declared tool/files interface before assuming support.
[Resolution matching][single-resolution], [toolchain provider contract][toolchain-info]

## Classify each dependency by its job

| Dependency | Intended configuration | Reason |
| --- | --- | --- |
| Source library linked into the output | Target | Its compiled code runs as part of the target artifact |
| Code generator invoked during the build | Execution | The generator process must run where its action executes |
| Compiler executable and its process support | Execution-compatible toolchain inputs | The compiler process runs on the execution platform |
| Target sysroot, headers, and runtime libraries | Inputs selected for the target ABI | They describe or become part of the target output |
| Runtime data | Rule-specific data/runfiles interface | Follow the consuming rule's semantics; do not infer a CPU transition from the word “data” |

This table is a design guide. The actual dependency transition belongs to the
rule/attribute definition; dependency names alone do not enforce it.
[Attribute configuration API][attr-api], [execution transition][exec-transition]

A generator that is itself built from source normally uses an executable dependency
with an execution transition. Its generated source can then become input to target
compilation. Passing a target-configured generator into an action can produce an
executable that cannot run on that action's platform. Associate toolchain tools and
named-group tools with the same action group used to resolve/build them.
[Execution configuration][exec-transition], [action tool association][action-api]

## Inspect the selected pair

Our recommended review records the target platform, execution platform, toolchain
type, selected wrapper/implementation, compiler distribution, target ABI/sysroot,
and any relevant feature settings. Check both sides of native interop: for example,
the Rust/C or Go/C dependency graph must agree on target ABI while build-script and
generator processes remain runnable on the execution platform.

The generic resolver checks declared constraints and target settings. It does not
interpret language-specific ABI promises in arbitrary `ToolchainInfo` fields.
Language rules and compiler toolchain implementations must enforce their own
contracts. [Generic matching][single-resolution], [provider interface][toolchain-info]

## Validate compilation and execution separately

A successful compile/link result establishes less than a successful target test.
Our recommended validation records separately whether the artifact was built,
whether its metadata matches the expected target, and whether it actually ran in
a compatible target environment. An execution-platform registration alone is not
a test runner or emulator installation; it is a candidate declaration for
resolution. [Execution-platform registration][module-globals]

For multi-architecture output, use a ruleset's supported integration or a deliberate
split transition; putting several labels in `--platforms` is insufficient because
9.3.1 uses one target platform per configuration. See
[transitions](../configuration/transitions.md) for split semantics and
[resolution](resolution.md) for selection diagnostics.
[Target platform normalization][platform-options]

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[platform-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/platforms.md
[toolchain-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ToolchainRule.java
[single-resolution]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java
[toolchain-info]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java
[attr-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java
[exec-transition]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java
[action-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[module-globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[platform-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java
