---
title: "Diagnose execution and cache misses"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.execution.logs", "diagnostics.execution.compare", "diagnostics.execution.summary"]
last_verified: "2026-11-05"
---

# Diagnose execution and cache misses

## Use this when

Use this page after analysis succeeds but an action fails, reruns unexpectedly,
or does not share remote results as expected.

## Separate the observations

The process summary distinguishes remote execution, remote cache hits, and local
execution strategies. Local incremental reuse may produce no spawn to count in
that summary. A low process count therefore does not by itself indicate a failed
remote cache. [Cache troubleshooting][cache]

Our recommendation: preserve the failed invocation's inputs and logs before
changing configuration. Avoid indiscriminate cleaning as the first diagnostic
step. For a controlled cache comparison, use disposable output bases so that
local reuse does not mask the remote-cache behavior under investigation.

## Compare actions, then service behavior

`--execution_log_compact_file` writes Zstd-compressed, length-delimited
`ExecLogEntry` records. Binary and JSON alternatives use `SpawnExec` records;
the three output modes are mutually exclusive. The compact format is the
upstream-recommended format. Do not treat it as newline JSON or compare its bytes
as a stable action ordering. [ExecutionOptions][execution]; [log schemas][spawn]

Compare corresponding actions across runs: tool/arguments, environment, declared
input paths and digests, outputs, platform properties, and cacheability. If the
actions differ, determine which project/configuration change explains it. If they
match, inspect cache reads/writes, instance names, authorization, missing blobs,
and service errors. The comparison procedure follows upstream's diagnostic model;
it is not evidence that every mismatch is caused by non-hermeticity.
[Cache troubleshooting][cache]

BEP's canonical structured command line exposes expanded options. It can help
identify an rc-configured cache policy different from what the short shell command
suggests. Handle logs according to the project's data policy because arguments
and environment may contain sensitive values. [Cache troubleshooting][cache]

## Coverage and next task

Log schemas and flags were source-reviewed. No cache experiment or performance
measurement was run. Continue with [profiles and events](profiles-and-build-events.md),
[hermeticity](../actions/hermeticity-and-reproducibility.md), or
[remote caching](../remote/caching.md).

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[cache]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/cache-remote.md
[execution]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/exec/ExecutionOptions.java
[spawn]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/protobuf/spawn.proto
