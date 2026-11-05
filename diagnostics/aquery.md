---
title: "Inspect analyzed actions"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.aquery.graph", "diagnostics.aquery.filters", "diagnostics.aquery.identity"]
last_verified: "2026-11-05"
---

# Inspect analyzed actions

## Use this when

Use `aquery` when the target graph is plausible but an action has wrong arguments,
inputs, outputs, tools, or configuration. It inspects analyzed actions rather than
reporting which processes actually executed. [aquery introduction][aquery]

## Narrow to the relevant action

The `mnemonic`, `inputs`, and `outputs` filters select actions from an analyzed
target expression. Action filters produce actions, so they cannot be inserted
where an ordinary target-producing query function expects targets. Start with a
small target/dependency scope, then filter its actions. [Filter grammar][aquery]

Bazel 9.3.1 includes command lines and artifacts in ordinary aquery output by
default. Parameter-file contents and file-write contents require their respective
`--include_param_files` and `--include_file_write_contents` options; both default
to false. Parameter-file inclusion also enables command-line inclusion.
Use only the extra detail needed for the investigation. [AqueryOptions][aoptions]

Compare the executable, arguments, declared inputs, outputs, environment, and
execution requirements. Treat file paths passed only as strings as a prompt to
check whether the files were also declared as action inputs. See
[inputs and tools](../actions/inputs-tools-environment.md).

## Do not confuse identities

The `ActionKey` displayed by aquery is not a complete remote-cache digest of the
input file contents. It can remain unchanged when an input's contents change.
The remote action identity includes an input-tree digest. Do not diagnose a
remote-cache bug from equality of these two displayed action keys alone.
[Aquery ActionKey explanation][aquery]; [REAPI model](../remote/reapi-model.md)

An action visible after analysis may never execute in a particular build because
its output is not requested or an existing result is reused. Use execution logs
or profiles to establish execution behavior. [Phases](../core/phases-and-graphs.md);
[aquery/profile distinction][aquery]

## Coverage and next task

The [foundation fixture](../verification/foundations.md) inspects template/write
actions. Other filters and output modes here are source-reviewed. Continue with
[execution and cache misses](execution-and-cache-misses.md).

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[aquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/aquery.md
[aoptions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/query2/aquery/AqueryOptions.java
