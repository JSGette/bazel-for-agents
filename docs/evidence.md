# Initial evidence

Checked on 2026-11-05. These initial findings seeded the first topics. The entire
planned reference is not yet written or verified. Published foundation pages
are indexed in the [README](../README.md); their more detailed claim records are
listed below.

## Published foundation evidence

- [Labels, phases, and graphs](../verification/core-labels-phases.md).
- [Rules and providers](../verification/core-rules-providers.md).
- [Outputs, runfiles, and actions](../verification/core-outputs-actions.md).
- [Target and load visibility](../verification/core-visibility.md).
- [Starlark dialect and collections](../verification/starlark-basics.md).
- [Executed producer/consumer fixture](../verification/foundations.md).

These records pin the Bazel 9.3.1 source commit and separate source inspection
from execution. The README also explains the research motivation; functional
fixture checks do not measure whether this reference improves coding agents.

## Reference identities

- **Bazel 9.3.1:** confirmed by the [official release](https://github.com/bazelbuild/bazel/releases/tag/9.3.1),
  exact-tag source, and a locally executed official binary. See the
  [probe record](../verification/starlark-set.md) for its SHA-256 and output.
- **REAPI v2.12.0:** latest stable release returned by the upstream releases API
  during this investigation; tag commit `9e084d0e43e717128ee72b5be584a7ba33e8006b`.
  Sources: [release](https://github.com/bazelbuild/remote-apis/releases/tag/v2.12.0),
  [tag identity](https://api.github.com/repos/bazelbuild/remote-apis/git/ref/tags/v2.12.0).
- **Rulesets:** current stable registry candidates appear with an immutable BCR
  snapshot in the [inventory](../rulesets/README.md). Their examples have not yet
  been tested individually or together on the exact baseline.

## Claims checked against Bazel 9.3.1

| Claim | Evidence | Status and limits |
| --- | --- | --- |
| `set()` is enabled by default; its controlling flag can still disable it. | [BuildLanguageOptions](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java#L781) | Source-verified; constructor, membership, deduplication, mutation, union, and sorting also passed in the [local probe](../verification/starlark-set.md). |
| Sets require hashable elements, iterate in first-addition order, and have no set-literal syntax. | [StarlarkSet](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/net/starlark/java/eval/StarlarkSet.java#L44) | Source-verified. Ordering and rejected syntax were not separately runtime-tested. |
| Rule implementations run during analysis and register actions for later execution. | [Rules](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/extending/rules.md) | Source-verified; the probe also built a declared output using `FileWrite` and `DefaultInfo`. |
| Providers expose information to dependent rule implementations. | [Providers](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/extending/rules.md#L416) | Source-verified; a custom-provider fixture remains planned. |
| Depsets support shared transitive aggregation across dependency graphs. | [Depset structure](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/extending/depsets.md#L12) | Source-verified. Our recommendation is to distinguish local set operations from transitive propagation. |
| Symbolic macros are enabled by default. | [BuildLanguageOptions](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java#L261) | Source-verified; macro examples are not yet tested. |
| Automatic loading of externalized rule symbols in the main repository is disabled by default. | [BuildLanguageOptions](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java#L159) | Source-verified. This does not imply all native symbols have been removed. |
| Module version selection uses versions requested in the dependency graph rather than automatically choosing the newest published version. | [Module version selection](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/external/module.md#version-selection) | Source-verified; overrides and compatibility levels need separate treatment. |
| Module extensions create repositories; `use_repo` exposes selected generated repositories to the consuming module. | [Module extensions](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/external/extension.md) | Source-verified; each ruleset's extension API needs separate verification. |
| Toolchain resolution checks target and execution constraints separately. | [SingleToolchainResolutionFunction](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java#L163) | Source-verified; registration precedence and allowed toolchain types also need coverage. |
| Normal execution-platform selection scores suitable platforms by the number of resolved requested toolchains, including optional types; ties preserve order. | [Implementation](https://github.com/bazelbuild/bazel/blob/9.3.1/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunction.java#L329), [optional-toolchain test](https://github.com/bazelbuild/bazel/blob/9.3.1/src/test/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunctionTest.java#L328) | Source-verified, including upstream test inspection. Those tests were not run here. Forced-platform handling is separate. |

## Protocol claims

REAPI defines separate services for action execution, the action cache, and
content-addressable storage. Its capabilities response describes API version
bounds and cache/execution capabilities. These facts were verified from the
[pinned protocol definition](https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto).
They do not establish that Bazel 9.3.1 implements every feature in that release,
or that a particular remote service supports them. Client feature auditing and
client/server integration tests remain future work.

## Documentation discrepancies for maintainers

The Bazel 9.3.1 source tree itself contains stale guidance:

- Its [language overview](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/rules/language.md)
  contains language limitations that conflict with the set implementation and
  successful binary probe.
- Its [depset guide](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/extending/depsets.md#L306)
  retains a dictionary-based set example.
- Its [toolchain guide](https://github.com/bazelbuild/bazel/blob/9.3.1/site/en/extending/toolchains.md)
  retains obsolete registration sources and an incomplete platform-selection
  description. The version-specific implementation and tests above support the
  planned resolution page.

Agent-facing instructions should teach the resolved current behavior directly,
without reproducing stale recipes.
