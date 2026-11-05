---
title: "Model platforms and constraints"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["configuration.platform-roles", "configuration.constraints", "configuration.platform-inheritance", "configuration.platform-flags", "configuration.target-compatibility"]
last_verified: "2026-11-05"
---

# Model platforms and constraints

Use this when describing where a build runs, where its tools run, and where its
outputs will run. Our recommendation is to name those environments explicitly
before choosing a compiler, SDK, or remote worker.

## Keep three roles distinct

| Role | Meaning | Main selection input |
| --- | --- | --- |
| Host platform | Environment running Bazel itself | `--host_platform` |
| Execution platform | Environment selected for an action's tools | Registered execution platforms, constraints, and toolchains |
| Target platform | Environment the configured target is built for | `--platforms` and transitions |

A configuration uses one target platform. Although `--platforms` accepts a list,
9.3.1 uses its first entry; it is not a multi-platform build loop. If no target
platform is supplied, the platform options use the host platform. These are
configuration inputs, not a mechanism that installs a compiler or provisions a
worker. [Options and normalization][platform-options], [platform configuration][platform-config]

An execution transition configures a build-time dependency for the selected
execution platform. This makes a code generator and the code it generates capable
of targeting different machines. See [cross-compilation](../toolchains/cross-compilation.md).
[Execution transition][exec-transition]

## Model requirements with constraint values

A `constraint_setting` names a dimension, such as CPU architecture. A
`constraint_value` chooses one value in that dimension. A `platform` groups
constraint values; it cannot declare conflicting values for the same setting.
Use existing shared dimensions when they express the requirement, and introduce a
custom setting only for a property consumers really test. The latter is our
modeling recommendation. [Constraint API][constraint-rule], [platform validation][platform-impl]

A setting's `default_constraint_value` supplies the value when a platform omits
that setting. Without a default, omission is unspecified and does not satisfy a
requirement for a particular value. The default must be in the setting's package.
Do not interpret every omitted constraint as a wildcard. [Default semantics][constraint-rule]

For a conditional sub-dimension, 9.3.1 also exposes
`constraint_setting.refines_constraint_value`: explicit values for the refining
setting require the refined value on the platform, and refinement participates in
`select()` specificity. The declared default value is exempt from that requirement.
Use this only when the relationship is genuinely hierarchical; independent
properties belong in independent settings. [Refinement contract][constraint-rule]

## Distinguish inheritance, flags, and execution properties

A platform supports at most one parent. Child constraint values override the
parent's value for the same setting. `exec_properties` merge by key, child values
win, and an empty child value removes the inherited key. These strings are passed
to execution machinery; they are not constraint values and do not select
`select()` branches. [Platform contract][platform-rule], [constraint lookup][constraint-collection]

`platform.flags` sets configuration options when the platform becomes the target
platform of a configuration, including an execution configuration. Those values
override previous values from command lines, rc files, and transitions. Repeatable
flags are replaced by platform values rather than appended to previous values.
Our recommendation is to keep this attribute small and inspect it when a command
line flag appears ineffective. [Platform flags contract][platform-rule]

`platform.required_settings` filters execution-platform eligibility using
`config_setting` targets evaluated against the target configuration. These settings
are not inherited from the parent. It is a separate control from the platform's
own constraint values. [Required settings contract][platform-rule]

## State which targets can exist on a platform

Ordinary targets can declare `target_compatible_with`. Incompatible targets
selected through broad target patterns are skipped; explicitly requesting one
normally reports incompatibility. Incompatibility also propagates through target
dependencies. Use compatibility to exclude unsupported targets, and `select()`
to choose among supported implementations. [Compatibility behavior][platform-guide]

Do not confuse that target attribute with a `toolchain` declaration's
`target_compatible_with`, which filters candidate toolchains. Continue with
[selection and build settings](select-and-build-settings.md), then
[toolchain resolution](../toolchains/resolution.md).

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[platform-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java
[platform-config]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformConfiguration.java
[exec-transition]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java
[constraint-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ConstraintSettingRule.java
[platform-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/Platform.java
[platform-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/PlatformRule.java
[constraint-collection]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/platform/ConstraintCollection.java
[platform-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/platforms.md
