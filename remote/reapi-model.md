---
title: "The Remote Execution API object model"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.model.services", "remote.model.action", "remote.model.result"]
last_verified: "2026-11-05"
---

# The Remote Execution API object model

## Use this when

Read this before diagnosing remote caching, execution, or artifact transfer.
The protocol reference is **REAPI v2.12.0**; Bazel client behavior is separately
bounded to **9.3.1**. A protocol field is not a promise that every client uses it.

## Follow the objects

| Object or service | Responsibility |
| --- | --- |
| Content Addressable Storage (CAS) | Stores blobs addressed by digest, including file contents and serialized protocol messages. |
| `Directory` | Describes one input-tree node: files, child directories, and symlinks. Child directories are referenced by digest. |
| `Command` | Specifies arguments, environment, working directory, and requested output paths. |
| `Action` | Refers to the command and input root by digest; also carries timeout, cache policy, and optional platform requirements. |
| Action Cache (AC) | Looks up an `ActionResult` using an action digest and request context. |
| `Execution` | Executes an action, returning a long-running operation and ultimately an `ExecuteResponse`. |
| `Capabilities` | Describes the server's supported API range and cache/execution features. |

These are distinct protocol objects and services. A cache service alone need not
provide execution. The action's inputs and command must be present in CAS for
execution; the server can request missing inputs. [REAPI definitions][protocol]

The digest of a serialized `Action` depends on its command and input-tree digests.
Changing an input's content can therefore change the remote action identity even
when its path and command-line arguments stay the same. Timeout and platform
requirements also participate in this object model. This is a protocol-level
explanation; it does not equate the remote digest with the `ActionKey` displayed
by `aquery`. [Action and Directory][protocol]; [Bazel construction][service]

## Interpret a result

`ActionResult` describes output files/directories/symlinks, exit code, stdout and
stderr, and optional execution metadata. File contents and streams can be inline
where the protocol permits, or referenced by digest. An input root uses a `Directory` digest. Output
directories can carry a `tree_digest`, a `root_directory_digest`, or both, according
to the command's requested output-directory format and worker support. A `Tree`
message and a `Directory` message are different encodings; interpret each digest
using its field's contract. Bazel 9.3.1's inspected download path consumes the
`tree_digest` representation. [ActionResult, Command.OutputDirectoryFormat,
Tree, OutputDirectory][protocol]; [Bazel output parsing][service]

Our recommendation: diagnose an AC lookup, missing CAS blob, rejected execution,
and failed command as different events. Preserve the action digest, instance,
capabilities, and status when investigating; a generic “remote failed” label
loses the distinction needed to fix the problem.

## Coverage and next task

Definitions were source-reviewed, with no remote service integration run.
Continue with [caching](caching.md), [execution](execution.md), or
[capabilities](capabilities-and-versions.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[service]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteExecutionService.java
