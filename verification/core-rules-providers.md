# Rule and provider claim records

Verified 2026-11-05 against Bazel **9.3.1**, source commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`. These records support
[rule contracts](../core/rule-contract.md) and [providers](../core/providers.md).
Each source link pins that commit. Recommendations are identified as such in the
guidance; the records below establish the underlying API behavior.

All records are **source-verified**. The linked [foundation execution record](foundations.md)
adds runtime evidence where specified, including commands, configuration inputs,
environment, expected and observed results. No external ruleset is used by these
pages' examples. No special semantic feature flags are required. Runtime coverage
is limited to the Linux x86_64 fixture; source-only claims do not assert tested
cross-platform coverage.

## rules.definition

`rule()` defines a rule kind, assigned to a `.bzl` global; calling the symbol from
a BUILD file or macro instantiates a target. The implementation takes one context
parameter and is evaluated during analysis.

Source: [StarlarkRuleFunctionsApi.rule and implementation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java#L428).
Fixture: `greeting` and `greeting_report` definitions and target declarations.

## rules.attributes

`rule.attrs` maps names to attribute schemas; common names are already defined.
Dependency attributes expose `Target` objects at analysis time. `ctx.file` accesses
the singular file for an `allow_single_file` attribute; `ctx.files` exposes default
files of dependencies.

Sources: [rule.attrs](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java#L463),
[dependency attributes](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java#L67),
[context accessors](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleContextApi.java#L70).
Fixture: string, single-file, and provider-constrained attributes are exercised.
`ctx.files` and split-transition attribute behavior are not exercised.

## rules.implementation

Rule implementation evaluation registers actions and returns providers. It does
not directly execute external commands or read/write artifact contents. `File`
objects refer to artifacts; `ctx.actions.write` registers a file-producing action.

Sources: [implementation and Files](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L240),
[action registration](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L341),
[ctx API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleContextApi.java#L46).
Fixture: template expansion and metadata writing, inspected with `aquery`.
No attempt to read artifact contents during analysis was added as a negative test.

## rules.action-cardinality

A rule need not correspond to one action. The fixture registers two producing
actions for its producer. `filegroup` aggregates existing artifacts and builds
providers without registering a producing action of its own.

Sources: [filegroup implementation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/filegroup/Filegroup.java#L50),
[fixture source](../examples/foundations/defs.bzl).
Runtime evidence covers the producer's actions; zero producing actions in
`filegroup` is verified by source inspection.

## rules.output-demand

For ordinary output selection, Bazel follows requested outputs and their
dependencies. Action registration alone does not require that action to run.
Default outputs and named output groups provide ways to select results.

Sources: [default outputs and pruning](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L434),
[requesting outputs](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L727).
Fixture: metadata was absent after the report build and present after explicitly
selecting its output group. Special validation and internal output groups are not
covered by this ordinary-output description.

## providers.identity

`provider()` defines a symbol stored in a `.bzl` global. Calling it constructs an
instance; a target's implementation returns provider instances. A consumer indexes
a dependency by the provider symbol to retrieve that instance.

Source: [provider API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java#L65).
Fixture: `GreetingInfo` construction, return, lookup, and use as an action input.

## providers.schema

The `fields` parameter restricts allowed field names; listed fields are optional.
Its documentation strings do not constrain the types of values assigned to fields.
The `init` parameter supports preprocessing and validation when constructing
instances.

Source: [fields and constructor semantics](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java#L106).
Fixture uses documented fields. Omitted fields, wrong value types, and custom
initialization are not runtime-tested here.

## providers.requirements

Dependency attribute `providers` constrains returned providers: all members of one
alternative must be present. A flat list is one alternative. This does not require
the dependency's rule to advertise those providers. Separately, `rule.provides`
requires the implementation to return every advertised provider.

Sources: [attribute provider requirements](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java#L171),
[rule provides contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java#L44).
Fixture: valid dependency accepted; `//:bad_provider` fails analysis because
`//:plain_file` lacks `GreetingInfo`. Nested alternatives and missing advertised
providers are not separately runtime-tested.

## providers.defaults

Every rule type has `DefaultInfo`. Its `files` field selects default output
artifacts; `runfiles` describes runtime files; executable information is separate.
Custom provider fields do not substitute for `DefaultInfo.files`.

Source: [DefaultInfo API and constructor](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/DefaultInfoApi.java#L31).
Fixture: consumer asserts the exact default file and separately checks the runtime
file. It does not launch an executable or test runfiles lookup on any platform.

## providers.output-groups

`OutputGroupInfo` exposes named artifact groups; `--output_groups` selects groups
for a build. Custom providers carry consumer-facing semantics independently of
that selection interface.

Sources: [output-group selection](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L745),
[OutputGroupInfo API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/OutputGroupInfoApi.java#L29).
Fixture: selecting `metadata` produces `greeting.metadata.txt` with checked content.

## providers.transitive

Rule implementations read providers of direct dependencies. Information needed
further up the dependency graph must be forwarded through providers; Bazel's guide
recommends depsets for accumulating transitive collections.

Source: [provider propagation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#L414).
The fixture exercises one provider edge. Larger transitive aggregation and its
performance characteristics are source-only here.
