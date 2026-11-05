---
title: "Choose list, dict, set, or depset"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/dialect-and-contexts.md"]
claim_ids: ["starlark.collections.list", "starlark.collections.dict", "starlark.set.default", "starlark.set.semantics", "starlark.set.probe", "starlark.collections.depset", "starlark.collections.flatten"]
last_verified: "2026-11-05"
---

# Choose list, dict, set, or depset

## Use this when

Choose a representation for local Starlark data or for information passed across
rule dependencies. The following choices are repository recommendations grounded
in each type's verified semantics.

| Need | Prefer | Relevant semantics |
| --- | --- | --- |
| An explicit sequence, including repeated values | `list` | Indexed sequence; supports concatenation and mutation while unfrozen. [Evidence][list] |
| A mapping from keys to associated values | `dict` | Hashable keys; iteration yields keys in insertion order. [Evidence][dict] |
| Unique values, membership, or local set operations | `set` | Hashable elements, duplicate elimination, membership, and union. [Evidence][set] |
| Transitive aggregation across rule dependencies | `depset` | Immutable nested aggregation with efficient merging and traversal rules. [Evidence][depset] |

## Use the core set type for ordinary sets

On Bazel 9.3.1, `--experimental_enable_starlark_set` defaults to `true`.
No enabling flag was needed in this repository's probe. A caller can explicitly
disable the flag, so check effective configuration when `set()` is unexpectedly
unavailable. The flag's spelling still includes `experimental`.
[Default source and execution evidence][default]

Construct a set with `set()` or `set(iterable)`. There is no set-literal syntax.
Elements must satisfy the same hashability requirement as dictionary keys.
Iteration follows first-addition order, while equality depends on the elements
and ignores their iteration order. A frozen set cannot be mutated.
[Evidence][set]

Our recommendation: use `set` directly when the data is a collection of unique
values. Choose `dict` when the values associated with keys have meaning. Use
`sorted()` at an output boundary when the required order is lexical rather than
first-addition order, as demonstrated by the fixture below.

## Keep transitive aggregation as a depset

A `depset` is immutable and combines direct elements with child depsets supplied
through its `transitive` argument. Its elements must have the same Starlark type;
the documented element contract also requires hashability. Duplicate values are
suppressed when the structure is flattened. [Evidence][depset]

Depsets do not provide fast set-style membership operations. Their default
traversal order is deterministic but unspecified. Our recommendation: preserve
depsets across provider boundaries when aggregating transitive data, and do not
depend on a specific traversal sequence without an explicit ordering contract.
[Evidence][depset]

`to_list()` traverses the nested structure. Repeatedly flattening transitive data
at each dependency can duplicate work; retain the nested representation until an
actual consumer needs a list. This is a performance recommendation based on the
implementation's documented traversal cost. [Evidence][flatten]

## Minimal verified example

The [complete fixture](../examples/starlark-set/probe.bzl) constructs a set from
three strings containing a duplicate, checks its length and membership, adds a
value, takes a union, and writes its sorted contents. It returns the generated
file through `DefaultInfo(files = depset([out]))`.

The expected and observed output is:

```text
alpha
beta
delta
gamma
```

Use the [exact build command and environment record][probe] to reproduce it.
This executed example checks the set operations and the file result. It does not
exercise transitive depset merging, set iteration order, freezing, or rejection
of invalid element types; those claims are source-verified only.

## Evidence and next task

Sources are pinned to the Bazel 9.3.1 release commit in the
[claim ledger](../verification/starlark-basics.md). Continue to
[providers](../core/providers.md) when these collections cross dependency edges.

[list]: ../verification/starlark-basics.md#starlarkcollectionslist
[dict]: ../verification/starlark-basics.md#starlarkcollectionsdict
[default]: ../verification/starlark-basics.md#starlarksetdefault
[set]: ../verification/starlark-basics.md#starlarksetsemantics
[depset]: ../verification/starlark-basics.md#starlarkcollectionsdepset
[flatten]: ../verification/starlark-basics.md#starlarkcollectionsflatten
[probe]: ../verification/starlark-basics.md#executed-fixture
