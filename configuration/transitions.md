---
title: "Change configurations on dependency edges"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["configuration/select-and-build-settings.md", "core/rule-contract.md"]
claim_ids: ["configuration.transition-placement", "configuration.transition-contract", "configuration.transition-allowlist", "configuration.execution-transition", "configuration.transition-cost"]
last_verified: "2026-11-05"
---

# Change configurations on dependency edges

Use this when a dependency must be analyzed under different build settings from
its consumer. Our recommendation is to start with ordinary target dependencies,
use an execution transition for build-time tools, and introduce a custom transition
only for a concrete configuration requirement.

## Choose the transition boundary

| Boundary | Declaration | Meaning |
| --- | --- | --- |
| Rule's incoming edge | `rule(cfg = transition_object)` | Changes the configuration of the rule itself; must produce one configuration |
| Dependency's outgoing edge | Dependency attribute's `cfg` | Changes the dependency configuration; can produce one or several configurations |
| Execution tool dependency | `cfg = "exec"` or `config.exec(...)` | Configures the dependency for the selected execution platform |

These attach to rule definitions or attribute schemas, not arbitrary target calls.
For named execution groups, `config.exec(exec_group = ...)` uses that group's
execution platform. [Transition API][rule-api], [attribute API][attr-api],
[configuration API][config-api]

For a split transition, consume the dependency partitions through `ctx.split_attr`
when the distinction between splits matters. Do not assume an `attr.label` always
becomes a single target after a split transition. [Split dependency access][config-guide]

## Declare the settings read and written

`transition()` takes an implementation with `settings` and `attr` arguments, an
`inputs` list, and an `outputs` list. `settings` exposes the declared input keys.
A normal returned settings dictionary must have exactly the declared output keys;
each split's dictionary is checked the same way. Return an unchanged input value
explicitly when it remains part of a nonempty result. A top-level empty dictionary
is a special no-change result in this implementation. Do not infer that arbitrary
partial dictionaries are accepted from the API prose's weaker “superset” wording.
[Evaluation and validation implementation][function-transition]

Use build-setting labels for Starlark settings. Native options use
`//command_line_option:<option_name>`, but this is not access to every command-line
flag: native options must exist, be configurable, and satisfy transition
restrictions. Read the option's exact implementation before changing it.
[Native option validation][function-util], [transition declaration][function-transition]

For outgoing transitions, `attr` contains the owner's attributes after selector
resolution. Incoming transitions do not expose attributes whose values require
selector resolution. Keep transition inputs small and avoid a circular design
where the transition's decision depends on its own resulting `select()` value.
[Attribute timing][config-guide]

## Use the current allowlist behavior

Bazel 9.3.1's rule-definition implementation automatically adds the function
transition allowlist attribute when a Starlark transition requires it and the
attribute is absent. It also installs the allowlist check. Do not add repetitive
`_allowlist_function_transition` boilerplate solely because a remembered example
contains it. If explicitly supplied, its type, default, and expected label are
validated; an unused explicit allowlist is an error. [Automatic insertion and checks][rule-functions]

This does not mean allowlist enforcement is absent. It means the ordinary
attribute declaration is supplied by Bazel. The implementation and allowlist
identity are recorded in the [claim ledger](../verification/configuration-toolchains.md#configurationtransition-allowlist).

## Separate execution and target choices

An executable dependency attribute must declare its `cfg` explicitly. For a tool
that runs during the build, use an execution configuration and pass the executable
or files-to-run provider into the action. Ordinary libraries remain in the target
configuration unless the rule deliberately transitions them. Setting
`executable = True` alone does not choose an execution platform.
[Executable attribute contract][attr-api], [execution transition][exec-transition]

Custom transitions can increase the number of configured targets and multiply
analysis work, particularly when splits compose through a graph. Keep settings
stable, avoid gratuitous per-target variants, and inspect the configured dependency
graph before adding another transition. This is an engineering recommendation
supported by the transition model, not a measured performance result for this
repository. [Transition cost discussion][config-guide]

Continue with [toolchain consumption](../toolchains/consuming.md) when the changed
configuration exists to run a compiler, generator, or other build tool.

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[rule-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
[attr-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java
[config-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java
[config-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md
[function-transition]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/StarlarkDefinedConfigTransition.java
[function-util]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/FunctionTransitionUtil.java
[rule-functions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java
[exec-transition]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java
