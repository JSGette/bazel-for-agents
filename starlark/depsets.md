---
title: "Preserve transitive data with depsets"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/collections.md", "core/providers.md"]
claim_ids: ["starlark.depset.structure", "starlark.depset.elements", "starlark.depset.order", "starlark.depset.identity", "starlark.depset.args"]
last_verified: "2026-11-05"
---

# Preserve transitive data with depsets

Use depsets when a provider aggregates information through a dependency graph.
Use [ordinary collections](collections.md) for local transformations and set-style
membership decisions.

## Carry the graph across provider boundaries

A depset combines immediate elements through `direct` with existing child depsets
through `transitive`. It is immutable; extending an aggregation creates another
depset that can share its children. The type is intended for efficient transitive
merging in rules and aspects. [Source][depset]

Our recommendation: give the provider field a documented element type and ordering
contract. Collect the child depsets from dependencies and construct the new depset
once, with all immediate contributions. Avoid flattening every child and rebuilding
a large direct list at every node. The nested representation is the mechanism
that preserves sharing. [Implementation][depset]

For action command lines, pass the depset to `Args.add_all()` or `add_joined()`.
`Args` keeps this representation until it constructs the command line for
execution. Do not call `to_list()` merely to supply an `Args` method that already
accepts depsets. [Args API][args]

## Choose an order because the consumer requires it

| Order | Traversal contract |
| --- | --- |
| `default` | Deterministic, unspecified ordering. |
| `postorder` | Traverse children from left to right before the node's direct elements. |
| `preorder` | Visit direct elements before traversing children from left to right. |
| `topological` | Parents precede descendants; there is no general left-to-right guarantee. |

These contracts are defined by the [depset API][depset] and [order implementation][order].
A diamond graph makes `preorder` and `topological` observably different: visiting
one branch's shared descendant early need not put every parent before that child.
[Order implementation][order]

Two different nondefault orders cannot be merged. A default-ordered depset is
compatible with the other orders, but that does not create a stronger ordering
contract for its contents. Duplicate elements and child depsets with a different
order also limit the sequence promised by `to_list()`. Do not infer an ordered
linking interface merely from one observed traversal. [Source][depset]

Our recommendation: choose `default` when sequence is irrelevant. If a consumer
requires meaningful order or repetition, inspect that consumer's contract before
choosing a depset: flattening removes duplicates. [Source][depset]

## Keep element and equality contracts precise

All elements of a nonempty depset have one Starlark type. An empty depset can be
combined with any element type. The documented contract requires hashable
elements; the implementation separately rejects lists and dictionaries and checks
immutability. Prefer established immutable types such as `File` or strings, not
compound values relying on implementation gaps in hashability checking.
[Source][depset]

Depsets are not ordinary sets: they do not provide fast membership tests, and
separately constructed depsets are not equal merely because their elements are
equal. `to_list()` returns a deduplicated copy; modifying that copy does not change
the depset. Boolean conversion checks whether the depset is empty in constant
time. [Source][depset]

When testing provider contents, compare the appropriate values after an explicit
flattening boundary. Assert ordering only where the provider promises it. Continue
with [argument construction](../actions/arguments-and-param-files.md).

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[depset]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java
[order]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Order.java
[args]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java
