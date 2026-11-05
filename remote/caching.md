---
title: "Remote caching"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.cache.transport", "remote.cache.controls", "remote.cache.identity"]
last_verified: "2026-11-05"
---

# Remote caching

## Use this when

Use this page to reason about sharing action results between invocations and
machines. Start with the [REAPI model](reapi-model.md).

## Choose the cache role

Bazel's `--remote_cache` configures a remote cache endpoint. Its accepted schemes
include HTTP(S) and gRPC(S); an HTTP cache is not the gRPC REAPI service merely
because both store build results. `--remote_executor` separately enables a remote
executor. Endpoint and instance details belong to the chosen service configuration.
[RemoteOptions, remote_cache and remote_executor][options]

At Bazel 9.3.1, remote-cache reads (`--remote_accept_cached`) and uploading local
results (`--remote_upload_local_results`) default to true; neither setting creates
an endpoint. Cache read access, write access, execution permission, and reporting
are separate operational concerns. The gRPC capability check warns when uploads
are enabled but server updates are unavailable. [Options][options]; [check][capabilities]

Our recommendation: record effective flags, credentials scope, instance name,
platform properties, toolchain selection, and relevant environment before comparing
cache behavior. Never embed private credentials in a generic example or checked-in
rc file. Use the service's supported credential mechanism for the actual project.

## Explain misses and misleading successes

The remote action identity includes command and input-tree content. An undeclared
input is outside that declared contract: a cache hit cannot establish that a
rule's dependencies are complete. Fix the action definition before treating its
reuse as correctness evidence. [Action definition][protocol]; [cache limitations][cache]

A local incremental build can perform no new spawn at all, so a process summary
with no remote hits does not by itself demonstrate a remote-cache failure. For
controlled comparison, use separate disposable output bases and otherwise matching
configuration. This is our diagnostic recommendation, derived from the documented
interaction between local reuse and remote-cache reporting. [Cache diagnosis][cache-debug]

Do not call a cache lookup fresh execution. A verification report should distinguish
an assertion evaluated locally from a reused build or test result.

## Coverage and next task

Source-reviewed flags and behavior; no endpoint, credentials, server permissions,
cache-hit rates, or reproducibility claims were tested. Continue with
[cache-miss diagnosis](../diagnostics/execution-and-cache-misses.md) and
[output downloads](outputs-and-downloads.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java
[capabilities]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteServerCapabilities.java
[cache]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/caching.md
[cache-debug]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/cache-remote.md
