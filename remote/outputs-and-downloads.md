---
title: "Remote outputs and local materialization"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.outputs.policy", "remote.outputs.local", "remote.outputs.result"]
last_verified: "2026-11-05"
---

# Remote outputs and local materialization

## Use this when

Use this page when a successful remote build has fewer files on the local disk
than an external tool expects.

## Choose an output policy deliberately

Bazel 9.3.1's `--remote_download_outputs` defaults to `toplevel`. The accepted
policies include `all`, `toplevel`, and `minimal`. At the basic level, `minimal`
avoids downloading outputs except when needed locally; `toplevel` additionally
selects top-level outputs. The concrete client also handles local actions, tests,
and other required materialization. [Flag][options]; [RemoteOutputChecker][output]

Our recommendation: preserve the project's output policy, identify what the
consumer needs, and make those outputs explicit targets or output groups. Do not
assume that successful analysis or an AC hit leaves every transitive generated
file in the local output tree. See [outputs and runfiles](../core/outputs-and-runfiles.md).

A local action depending on a remote output still needs access to its input. A
build-wide policy to reduce downloads does not remove the action's declared input
contract. Conversely, an unrelated external script walking Bazel's output tree
is not automatically a dependency known to Bazel. The first behavior is handled
by output checking/materialization; declaring the script as a consumer is our
recommended integration approach. [RemoteOutputChecker][output]; [service][service]

## Inspect the result representation

Remote results can describe files, directory trees, and symlinks. The `ActionResult`
metadata and referenced CAS objects must be interpreted together; an action-result
entry alone is not a local filesystem copy. Input roots reference `Directory`
graphs. For outputs, REAPI defines `Tree` and separately stored `Directory`
representations selected through `Command.output_directory_format`; a returned
`tree_digest` identifies a `Tree`, while `root_directory_digest` identifies a
`Directory`. Bazel 9.3.1's inspected output-download path reads `tree_digest`.
[Command, ActionResult and OutputDirectory][protocol]; [Bazel output parsing][service]

Report artifact availability separately from execution location and cache reuse.
A downloaded file may come from a cached result; a result retained remotely may
have been freshly executed. These are separate observations in the protocol model.
[ExecuteResponse and ActionResult][protocol]

## Coverage and next task

No download-mode integration or external consumer was run. This page records
source-level policy and the relevant implementation, not complete materialization
coverage on every platform. Continue with [action directories](../actions/directories-and-symlinks.md)
and [cache diagnosis](../diagnostics/execution-and-cache-misses.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java
[service]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteExecutionService.java
[output]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteOutputChecker.java
