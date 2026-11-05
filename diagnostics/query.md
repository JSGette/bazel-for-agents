---
title: "Inspect the unconfigured target graph"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.query.graph", "diagnostics.query.operators"]
last_verified: "2026-11-05"
---

# Inspect the unconfigured target graph

## Use this when

Use `query` to investigate target existence, declared dependencies, package
boundaries, and paths through the graph before configuration is resolved.
It operates on the post-loading graph. For configuration-dependent dependencies,
it conservatively includes alternatives rather than choosing a `select()` branch.
[Query graph][query]; [configured-query comparison][cquery]

## Choose the question first

| Question | Query-language operation |
| --- | --- |
| What does a target depend on? | `deps` computes its transitive dependency closure. |
| What depends on a target within a chosen universe? | `rdeps` searches reverse dependencies inside its explicit universe. |
| Why is one target reachable from another? | `somepath` returns a path; `allpaths` returns the graph on connecting paths. |
| Which results have a particular rule kind? | `kind` filters a result set. |
| Which labels match a regular expression? | `filter` filters labels in an already chosen result set. |
| Which build/extension files are involved? | `buildfiles` exposes the relevant build-file dependencies within its documented model. |

These are query-language operations, not Starlark functions. Apply filters to a
bounded graph instead of scanning an entire repository without a question.
The operation semantics are sourced; choosing a narrow universe is our recommendation.
[Query language and functions][query]

Implicit dependencies are included by default. Removing them with
`--noimplicit_deps` changes what question the graph answers; a missing tool or
private dependency after that filter is not evidence that Bazel ignored it.
Query also does not perform target-visibility checking as analysis does.
[Implicit dependencies and query limitations][query]

## Interpret the result

A path in the unconfigured graph need not be a path in the actual build's
configured graph. Use [cquery](cquery.md) with the real build options to answer that
second question. Use [aquery](aquery.md) for command arguments and declared action
inputs; a target edge is not itself an action input list.
[Query/cquery comparison][cquery]; [aquery introduction][aquery]

The existing [foundation fixture](../verification/foundations.md) records an actual
9.3.1 dependency-query result. The operation catalog here is source-reviewed;
there is no exhaustive query-language runtime suite in this repository.

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[query]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/language.md
[cquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/cquery.md
[aquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/aquery.md
