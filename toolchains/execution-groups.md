---
title: "Choose execution groups for actions"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["toolchains/consuming.md", "toolchains/resolution.md"]
claim_ids: ["toolchains.named-groups", "toolchains.automatic-groups", "toolchains.group-action-routing", "toolchains.group-properties"]
last_verified: "2026-11-05"
---

# Choose execution groups for actions

Use this when one rule needs different execution environments, or when several
toolchains must run together on the same execution platform.

## Give a group one coherent execution requirement

A rule declares named groups in `exec_groups`, with each `exec_group(...)` carrying
its own toolchain requirements and execution constraints. Each group resolves
independently. A compile group and a signing group can therefore choose different
platforms even though they belong to the same target.
[Group declaration API][rule-api], [group model][exec-guide]

Access a group's tools through `ctx.exec_groups[name].toolchains[type]`. Select the
group on an action with `exec_group = name`. If a separately built executable
attribute belongs to that group, configure it with `config.exec(exec_group = name)`
so its build configuration agrees with the action's execution platform.
[Group access][exec-guide], [execution transition API][config-api]

When an action uses tools from several types, put those types in one named group
and consume them from that group. Independently resolved tools are not guaranteed
to run on the same platform. Named groups also express a distinct constraint or
execution policy for a particular stage. [Automatic-group model][auto-exec-guide],
[named groups][exec-guide]

## Check whether automatic groups are enabled

Bazel 9.3.1's `--incompatible_auto_exec_groups` default is **false**. A rule can
override the dynamic setting through `_use_auto_exec_groups`, and rule classes can
have an always-enabled or disabled mode. Therefore neither “all Bazel 9 rules use
automatic groups” nor “the global flag determines every rule” is accurate.
[Flag default][core-options], [per-rule mode implementation][rule-class]

When automatic groups are enabled for a rule, Bazel uses a separate group for each
of its toolchain types. The action's `toolchain` argument identifies the appropriate
group. This allows toolchain-dependent actions in the same rule to use different
execution platforms without manually declaring a group per type.
[Automatic-group behavior][auto-exec-guide], [action routing][action-impl]

Our authoring recommendation is to annotate toolchain-consuming actions explicitly
and document the rule's group policy. Do not enable or disable a global flag as an
unexamined fix for a toolchain error; first establish the rule's effective mode.

## Align action routing and tool access

If an action provides an explicit `exec_group`, that group selects the platform.
When automatic groups are active and both `exec_group` and `toolchain` are supplied,
9.3.1 checks that the named group declares that type. Without an explicit group,
a toolchain type selects its automatic group when that feature is active;
otherwise the default group is used. [Routing and validation implementation][action-impl]

`toolchain = None` explicitly states that the action's tools do not come from a
toolchain. It is not equivalent to selecting a different named group. Bazel can
infer some implicit-dependency tools, but it rejects ambiguous missing toolchain
annotations in the automatic-group cases checked by the action implementation.
[Action contract][action-api], [tool-origin checks][action-impl]

## Scope constraints and execution properties

Targets can add group-specific constraints through `exec_group_compatible_with`.
Execution properties can be scoped with a group-name prefix in a target's
`exec_properties`; group-specific values take precedence over the target's
unprefixed values for that group. These properties are execution metadata,
separate from toolchain requirement labels and platform constraints.
[Group constraint and property contract][exec-guide]

Continue with [cross-compilation](cross-compilation.md) for the relationship between
execution groups, code generators, target libraries, and target tests.

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[rule-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
[exec-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/exec-groups.md
[config-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java
[auto-exec-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/auto-exec-groups.md
[core-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java
[rule-class]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/RuleClass.java
[action-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java
[action-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
