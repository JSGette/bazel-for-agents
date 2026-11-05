---
title: "Inspect configured targets"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.cquery.configuration", "diagnostics.cquery.outputs"]
last_verified: "2026-11-05"
---

# Inspect configured targets

## Use this when

Use `cquery` to explain dependency selection, transitions, configured tools, and
outputs for a concrete build configuration. It runs analysis and follows resolved
`select()` branches. One label may appear in several configurations, so preserve
the configuration identifier when comparing results. [cquery][cquery]

## Reproduce the configuration

Our recommendation is to use the same target roots, platform flags, build settings,
rc expansion, and other analysis-affecting options as the failing build. A query
under different options can correctly answer a different question.

`--universe_scope` chooses the top-level targets used to establish the analyzed
universe. This matters for a dependency configured by an incoming transition:
analyzing that label alone need not reproduce its configuration as a dependency.
The `config` query function selects instances already present in the analyzed
universe; it does not synthesize an arbitrary new configuration. [Universe and config][cquery]

`--transitions=lite` or `full` exposes transition information. The full form shows
option changes and can help separate target and execution configurations.
Implicit dependencies, tool dependencies, and aspect inclusion have independent
query filters; report them when sharing findings. [Options and transitions][cquery]

## Choose an output view

| View | Use |
| --- | --- |
| Default label/configuration output | Identify multiple configured instances. |
| `--output=files` | Inspect files selected by the query's output behavior. |
| `--output=starlark` | Format configured-target information using the cquery dialect. |
| Protocol output | Consume structured targets/configuration IDs. |

The cquery Starlark context provides helpers such as `providers(target)` and
`build_options(target)`; it is not the same environment as a rule implementation.
File targets can have a null configuration. [Output formats and Starlark dialect][cquery]

## Coverage and next task

The [foundation verification](../verification/foundations.md) exercises a simple
files query only. Transition/universe cases here are source-reviewed. Continue
with [transitions](../configuration/transitions.md), [toolchain diagnosis](toolchain-resolution.md),
or [aquery](aquery.md).

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[cquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/cquery.md
