---
title: "Remote action execution"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.execution.client", "remote.execution.lifecycle", "remote.execution.fallback"]
last_verified: "2026-11-05"
---

# Remote action execution

## Use this when

Use this page when moving eligible action processes to remote workers. Repository
configuration, analysis, and the remote worker process are distinct responsibilities.

## Preserve the action contract

Bazel builds a command, input Merkle tree, and action; uploads required inputs;
and requests execution from the configured executor. The service's `Execute`
returns an operation that can report progress and ultimately an execution result.
The command's arguments and environment are explicit protocol fields.
[RemoteExecutionService][service]; [Execution and Command][protocol]

Our recommendation: begin with [declared inputs, tools, and environment](../actions/inputs-tools-environment.md).
Choose a toolchain that runs on the execution platform and produces outputs for
the target platform. Supply its executable and runtime files as action inputs,
or document an intentional worker-image dependency in the platform contract.
Do not assume the developer machine's installed compiler exists on the worker.
See [cross-compilation](../toolchains/cross-compilation.md).

Remote execution does not evaluate a rule's Starlark implementation on a worker.
Bazel's analysis registers actions; remote execution dispatches eligible spawns
from the execution machinery. Consequently, a loading or analysis rejection must
be checked by the Bazel invocation running the build, even in a remotely hosted
CI runner. [Phases](../core/phases-and-graphs.md); [remote service][service]

## Separate execution from reuse and fallback

An execution request may be served from the server's action cache unless the
request's policy prevents it. A successful remote build therefore does not imply
that every requested action executed freshly. [ExecuteRequest and ExecuteResponse][protocol]

`--remote_local_fallback` defaults to false in 9.3.1. Turning it on permits local
execution after applicable remote execution failures; it is not a replacement for
matching toolchains and platform requirements. Our recommendation is to investigate
why fallback occurred before claiming remote compatibility. [RemoteOptions][options]

Record queue, execution, transfer, and result-status evidence separately when the
service exposes it. REAPI's action timeout is scoped to execution rather than
queue time or all transfer overhead. [Action timeout and ExecutedActionMetadata][protocol]

## Coverage and next task

No worker images or remote backend were provisioned or tested. Continue with
[platform properties](platforms-and-properties.md), [capabilities](capabilities-and-versions.md),
and [hermeticity](../actions/hermeticity-and-reproducibility.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java
[service]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteExecutionService.java
