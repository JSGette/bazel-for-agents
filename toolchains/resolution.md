---
title: "Understand toolchain resolution"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["configuration/platforms-and-constraints.md", "toolchains/defining-and-registering.md"]
claim_ids: ["toolchains.registration-priority", "toolchains.execution-candidates", "toolchains.matching", "toolchains.platform-selection", "toolchains.resolution-debug"]
last_verified: "2026-11-05"
---

# Understand toolchain resolution

Use this when Bazel selects an unexpected implementation or cannot find a toolchain.
Read the resolver's decisions in terms of requested types, compatible wrappers,
and execution platforms; avoid treating registration as a global compiler switch.

## Establish registration priority

For toolchain candidates, 9.3.1 considers command-line `--extra_toolchains` before
module registrations. The extra-toolchain list is reversed so the last specified
entry has priority. Module registrations follow the resolved module graph's
breadth-first order, starting at the root, with each module's registration order
preserved. Repository mappings are resolved for the declaring module.
[Registered toolchains][registered], [graph-order contract][depgraph]

Patterns can expand to several targets. Their lexical target-name order and
pattern expansion/filtering affect the resulting candidates, so a broad pattern
is not a promise of implementation-specific priority. Use explicit wrapper labels
when diagnosing an ordering issue. [Pattern registration API][module-globals]

Execution-platform candidates have their own order: `--extra_execution_platforms`
precedes module registrations, and the host platform is added as a fallback
candidate. Duplicate registrations retain the earliest position. Unlike
`--extra_toolchains`, the extra-execution-platform list is not reversed; repeated
uses of that flag replace its earlier list. A host candidate still must satisfy
the resolver's requirements. [Platform registration][registered-platforms],
[candidate assembly][platform-keys], [flag definition][platform-options]

## Match each type on each execution platform

The resolver filters wrappers by requested type and target requirements, then
checks execution constraints for each candidate execution platform. For a given
type/platform pair, the first compatible registered toolchain wins. It does not
rank matching compilers by version or by how many constraints they declare.
[Single-type resolution][single-resolution]

`target_settings` filters wrappers against the target configuration. Execution
platforms can also impose `required_settings` and, when enabled on that platform,
allowed-toolchain-type restrictions. Rule or execution-group execution constraints
filter the platform candidates. These filters are distinct from matching the
wrapper's target constraints. [Wrapper filtering][registered],
[platform filtering and suitability][platform-keys], [type restrictions][single-resolution]

## Select a suitable execution platform

For normal selection, a platform must satisfy every mandatory toolchain
requirement. Among suitable platforms, 9.3.1 selects one resolving the largest
number of the requested types, including optional types. Ties preserve candidate
priority. Thus “always select the first platform satisfying mandatory toolchains”
is an incomplete description when optional requirements are present.
[Selection implementation][resolution]

The upstream tests `resolve_optional_on_second_platform` and
`resolve_max_optional_on_second_platform` exercise this preference. They were inspected as
source, not run in this repository. The resolver also has a forced-execution-
platform path that first accepts a suitable forced platform; the normal ranking
rule should not be generalized to that path. [Resolver tests][resolution-tests],
[forced selection branch][resolution]

Resolution is scoped to an execution group. With automatic groups enabled,
requirements can resolve separately by type; a named group can keep several types
on one platform. See [execution groups](execution-groups.md) before assuming all
actions of a rule share one execution platform.

## Investigate in a stable order

Our recommended investigation is:

1. Identify the configured target, requested types, and execution group.
2. Inspect the effective target platform and configuration settings.
3. Confirm imported repositories and registered wrapper labels.
4. Check rejection reasons for target constraints/settings and execution constraints.
5. Compare candidate order and optional requirements before changing registrations.
6. Inspect the selected implementation's provider and action tools.

`--toolchain_resolution_debug` accepts a regex filter matched against toolchain
types and targets and emits resolver diagnostics. Its default excludes everything.
Use a focused filter to inspect a failing type. The flag reports resolution;
it does not prove the selected executable works on the worker.
[Diagnostic flag][platform-options]

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[registered]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredToolchainsFunction.java
[depgraph]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/BazelDepGraphValue.java
[module-globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[registered-platforms]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredExecutionPlatformsFunction.java
[platform-keys]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/PlatformKeys.java
[platform-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java
[single-resolution]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java
[resolution]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunction.java
[resolution-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunctionTest.java
