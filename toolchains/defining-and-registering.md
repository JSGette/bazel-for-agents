---
title: "Define and register a toolchain"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/providers.md", "configuration/platforms-and-constraints.md", "toolchains/consuming.md"]
claim_ids: ["toolchains.definition-parts", "toolchains.compatibility", "toolchains.registration", "toolchains.registration-scope"]
last_verified: "2026-11-05"
---

# Define and register a toolchain

Use this when a reusable rule needs interchangeable platform-specific tools.
Our recommendation is to define the consumer interface first, then package and
register implementations that satisfy it.

## Keep the three targets separate

| Part | Purpose |
| --- | --- |
| `toolchain_type` target | Identifies the role requested by consumers |
| Implementation target | Returns `platform_common.ToolchainInfo` with the interface's fields |
| `toolchain` target | Connects the type to an implementation and declares selection constraints |

The implementation must return `ToolchainInfo`; resolution rejects a selected
target without it. The wrapper's `toolchain` attribute names that implementation,
while `toolchain_type` names the type. Register the wrapper target, not merely the
implementation. [Wrapper attributes][toolchain-rule], [provider check][resolved]

Bazel permits arbitrary named fields on `ToolchainInfo`. Document their types and
meaning, including executable providers, compiler flags, SDK files, and transitive
runtime support. Treat that documented schema as the shared contract between
producers and consumers. [Toolchain provider API][toolchain-info]

## Describe both sides of a cross toolchain

`exec_compatible_with` specifies constraints the execution platform must satisfy.
`target_compatible_with` specifies constraints the target platform must satisfy.
`target_settings` adds `config_setting` requirements evaluated against the target
configuration. A compiler's execution CPU and the CPU it produces code for are
separate choices. [Selection attributes][toolchain-rule]

`use_target_platform_constraints = True` makes the wrapper use the target
platform's constraints on both sides; explicit execution and target constraint
lists must then be absent. It expresses matching execution/target requirements,
not a general cross-compilation shortcut. Use explicit lists when the sides differ.
[Attribute contract][toolchain-rule]

Our recommendation is to declare the real runtime requirements of the compiler,
including its support files, rather than label a host-installed executable as
portable. Constraints describe eligibility; they do not download the compiler or
supply its dynamic libraries. Runtime closure remains part of the implementation's
action/tool contract. See [consuming](consuming.md).

## Register through the module interface

In `MODULE.bazel`, `register_toolchains` accepts absolute target patterns for
already-defined wrappers. `register_execution_platforms` separately registers
execution-platform candidates. Registering a toolchain does not register an
execution platform, and defining either target does not by itself register it.
[Module registration API][module-globals]

When a module extension generates the repositories containing wrappers, import the
needed repositories with the module's repository interface before naming them from
the root module. Registration uses that module's repository mapping; do not invent
canonical repository names. [Registration label resolution][registered]

`dev_dependency = True` registrations apply only when the declaring module is the
root and development dependencies are not ignored. Use this for a module's own
tests or development toolchains when downstream consumers should choose their own
implementations. This is a scope choice, not a marker of toolchain quality.
[Development registration scope][module-globals]

## Make priority deliberate

Explicit registration order matters. Patterns expanding to several wrappers are
registered lexicographically by wrapper target name, not implementation name.
Our recommendation is to register specific wrapper labels when priority is part
of the interface. See [resolution](resolution.md) before relying on module or
command-line ordering. [Pattern expansion contract][module-globals]

Keep tool acquisition, interface design, registration, and compatibility claims
separate in reviews. A well-formed registered wrapper does not prove that its
compiler can run on every platform satisfying the chosen constraints; that requires
integration evidence for the supplied binaries and SDKs.

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[toolchain-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ToolchainRule.java
[resolved]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/ResolvedToolchainContext.java
[toolchain-info]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java
[module-globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[registered]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredToolchainsFunction.java
