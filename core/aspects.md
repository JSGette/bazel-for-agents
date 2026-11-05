---
title: "Augment dependency graphs with aspects"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md", "core/providers.md", "actions/declaring-actions.md"]
claim_ids: ["core.aspects.graph", "core.aspects.application", "core.aspects.providers", "core.aspects.composition", "core.aspects.parameters", "core.aspects.default-files", "core.aspects.output-groups", "core.aspects.generating-rules"]
last_verified: "2026-11-05"
---

# Augment dependency graphs with aspects

Use an aspect when additional analysis or actions should follow selected edges of
an existing target graph: metadata extraction, language-specific code generation,
or a consumer-specific view of transitive dependencies. An aspect augments the
analysis of those targets; it does not rewrite their BUILD declarations.
[Graph model][guide]

## Define the additional analysis contract

Define an aspect in a `.bzl` file with `aspect()` and export it as a global value.
Its implementation receives `target` and `ctx` and runs during analysis for an
aspect application. Inspect the base rule through `ctx.rule` and its providers
through `target`; the aspect's own attributes use `ctx.attr`.
[Aspect API][api], [rule-context API][context]

An aspect can register actions and return providers. Return a list of provider
instances for a consistent interface; the 9.3.1 implementation also accepts a
single declared provider instance. It validates declared artifacts after creating
the configured aspect. [Evaluation implementation][factory]

`attr_aspects` selects the dependency attributes along which the aspect propagates.
A list containing `"*"` requests all dependency attributes. Propagated dependencies
expose the corresponding aspect results alongside the underlying target's
providers. Edges outside the propagation set do not automatically participate.
[Aspect API][api], [graph model][guide]

Our recommendation: begin with the specific attributes the analysis needs. A
whole-graph traversal is appropriate only when the task requires it. Preserve
transitive data in [depsets](../starlark/depsets.md) rather than repeatedly flattening
all descendants at each application.

## Choose how a consumer applies it

A rule can attach an aspect to a label dependency attribute through its `aspects`
parameter. Its implementation then consumes the augmented dependency through that
attribute. A command-line invocation instead selects an exported aspect using
`--aspects`, whose specification names the `.bzl` label and exported symbol
separated by `%`. These are different entry points into the same aspect model.
[Application guide][guide], [attribute API][attr]

`toolchains_aspects` separately names toolchain types whose resolved toolchains
receive the aspect. This is distinct from the aspect's `toolchains` declaration,
which requests toolchains for its own implementation. The API also exposes
function-valued propagation selectors and a propagation predicate as experimental
interfaces; this basic guidance uses explicit lists. [Aspect API][api]

## Check advertised providers and aspect composition

`required_providers` filters applicable rules by their **advertised** providers.
A flat list requires every listed provider; a list of lists permits any complete
inner group. Returning a provider at runtime without advertising it in the rule's
`provides` declaration is not the same applicability contract.
[API][api], [advertised-provider matching][definition]

`required_aspect_providers` controls visibility of other aspects' provider
interfaces. `requires` explicitly lists aspects that must propagate before this
one. Keep these separate from `required_providers`, which concerns the underlying
rule. An aspect's own `provides` declaration promises provider types its
implementation must return. [Aspect API][api]

Our recommendation: choose a distinct custom provider for the aspect's semantic
result. Ordinary duplicate provider types across a target and its aspects are
rejected during merging; selected built-in interfaces have special merge rules.
Do not mutate providers returned by the base rule.
[Provider merging][merged], [aspect graph guide][guide]

## Use the current output contracts

Bazel 9.3.1 permits an aspect to return `DefaultInfo` containing a `files` depset.
For an aspect merged into a dependency below the top level, those files join the
base target's default files. That non-top-level case rejects runfiles, executable,
and files-to-run fields. The blanket claim that aspects can never return
`DefaultInfo` is incorrect for this baseline. [Merge implementation][merged],
[`mergesFileProvider` and rejection tests][tests]

`OutputGroupInfo` from a rule and its aspects is merged. At this baseline,
**same-named groups also combine their files**: `OutputGroupInfo.merge()` adds
transitive contributions for each group name, and `duplicateOutputGroups` tests
that both rule and aspect files survive. Choose descriptive group names and a
custom provider when a consumer needs a stronger semantic interface.
[Merge implementation][groups], [regression test][tests]

These statements are source-verified; the referenced upstream tests were inspected,
not executed here. The release's general aspect guide and the `merge()` comment
retain older restrictions contradicted by these implementations and tests.

## Keep parameters and file traversal bounded

Public aspect parameters may have `bool`, `int`, or `string` types in the 9.3.1
implementation. Rule-propagated parameter values come from matching attributes
on the consuming rule; command-line aspects obtain parameter values through
`--aspects_parameters`. Check allowed values and required/default values before
choosing an entry point. These parameters are not arbitrary configurable rule
attributes. [Parameter validation][functions], [parameter extraction][defined],
[application guide][guide]

`apply_to_generating_rules` defaults to `False`. Enabling it makes an application
on an output-file target apply to its generating rule, allowing traversal to
continue there. The constructor rejects combining this mode with nonempty
`required_providers` or a propagation predicate. [API][api], [constructor checks][functions]

Our recommendation: test the intended dependency paths, provider contract, and
output selection with [analysis tests](../testing/analysis-tests.md). Add execution
coverage when the aspect generates files whose contents matter.

## Evidence boundary

This page is source-verified against Bazel 9.3.1. No new aspect fixture, upstream
suite, or remote execution test was run. The
[claim ledger](../verification/starlark-actions-testing.md) records exact symbols
and the documentation discrepancies resolved by implementation and tests.

[guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/aspects.md
[api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
[context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleContextApi.java
[attr]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java
[factory]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/StarlarkAspectFactory.java
[definition]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/AspectDefinition.java
[merged]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/configuredtargets/MergedConfiguredTarget.java
[groups]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/OutputGroupInfo.java
[tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/starlark/StarlarkDefinedAspectsTest.java
[functions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java
[defined]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/StarlarkDefinedAspect.java
