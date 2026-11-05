---
title: "Work with mutable local values and frozen shared values"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/dialect-and-contexts.md", "starlark/collections.md"]
claim_ids: ["starlark.freeze.evaluation", "starlark.freeze.iteration", "starlark.freeze.copy", "starlark.freeze.macro"]
last_verified: "2026-11-05"
---

# Work with mutable local values and frozen shared values

Use this page when a helper unexpectedly reports a frozen-value error, or when
choosing where to keep state during rule implementation.

## Keep shared values immutable

A Starlark evaluation has a mutability context. When evaluation finishes and that
context closes, its mutable values become frozen. In particular, a `.bzl` module
is frozen before another module imports its symbols. A list or dictionary loaded
from another file is therefore shared data, not a mutable cache. [Source][mutability]

Our recommendation: keep module-level values as constants and allocate working
lists, dictionaries, and sets inside the function performing the work. Return the
result or pass it explicitly. This follows the evaluator's isolation rule: one
evaluation cannot mutate another evaluation's bindings or values. [Source][mutability]

The rule also applies to a mutable function-default value created while the `.bzl`
module was evaluated. Prefer a default sentinel and a newly constructed local
container when the function needs scratch state. This recommendation follows from
freezing the objects created by that module, rather than from Python's execution
model. [Source][mutability]

## Copy at the boundary where mutation is needed

`list(value)`, `dict(value)`, and `set(value)` construct new containers in the
current evaluation. They reuse the contained elements: copying a dictionary does
not make a nested list inside it mutable. Copy the particular nested container
that you intend to change, or construct a new result from immutable inputs.
[Constructor implementations][constructors]

Our recommendation for helper APIs is to document whether they mutate arguments.
For reusable rule helpers, returning a new value usually makes ownership easier
to review. For symbolic macros, argument mutation is prohibited; the macro runs
in its own evaluation context. [Macro implementation][macro],
[macro restrictions][macro-guide]

## Do not mutate the collection being traversed

A mutable container is temporarily protected from mutation while a `for` loop or
comprehension is iterating over it. The protection applies to the container being
iterated, not recursively to its elements. A separate frozen-value restriction
can still prohibit mutation of those elements. [Source][mutability]

Our recommendation: accumulate removals/additions separately, or build a new
collection with a comprehension. Copying before traversal is appropriate when
snapshot semantics are actually desired; it should not conceal an unclear data
flow.

## Diagnose the owner of a value

When mutation fails, trace where the object was created and whether the current
operation is traversing it. Distinguish a loaded constant, a macro argument, a
nested object retained by a shallow copy, and a locally created collection. These
cases follow different paths to the same mutation guard. [Sources][mutability],
[constructors][constructors], [macro evaluation][macro]

Continue with [depsets](depsets.md) for immutable aggregation across dependency
edges, or [symbolic macros](symbolic-macros.md) for typed loading-time APIs.

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[mutability]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/Mutability.java
[constructors]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/MethodLibrary.java
[macro]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/MacroClass.java
[macro-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md
