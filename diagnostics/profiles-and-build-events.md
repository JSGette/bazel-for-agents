---
title: "Profiles and build events"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.profile.trace", "diagnostics.bep.events", "diagnostics.bep.transport"]
last_verified: "2026-11-05"
---

# Profiles and build events

## Use this when

Use profiles to explain time spent in a build, BEP to consume structured build/test
outcomes, and execution logs to compare action execution details. They answer
different questions. [Trace guide][trace]; [BEP schema][bep]; [execution log](execution-and-cache-misses.md)

## Follow time with a trace

Bazel 9.3.1 exposes `--generate_json_trace_profile`, `--profile`, and
`--profiles_to_retain`. The standard profile is a JSON trace with invocation
metadata and timing events; an explicit profile path can preserve the artifact
for an investigation. Defaults produce profiles for build-like commands and query.
[CommonCommandOptions][profile]; [profile location and format][trace]

Our recommendation: compare matched workloads and preserve the source commit,
options, cache state, machine resources, and invocation identity. Inspect loading,
analysis, execution, transfer/wait time, and critical-path behavior before choosing
an optimization. A single wall-clock number cannot explain which stage changed.
The trace guide documents these diagnostic uses, not a promised improvement for
any particular optimization. [Trace interpretation][trace]

## Consume outcomes with BEP

A build event has an identifier, announced child IDs, and a payload. The graph can
include aborted events, and abrupt termination or transport failure can leave
announced events absent. Consumers should not assume a flat list of successful
targets or that every payload is the expected success message.
[BEP schema][bep]; [event graph contract][bep-guide]

File transports include `--build_event_binary_file`, `--build_event_json_file`,
and `--build_event_text_file`. The binary transport is length-delimited protobuf;
JSON and text transports have their own representation. The Build Event Service
is a separate transport configured with `--bes_backend`; BEP recording does not
itself enable remote execution. [File options][bep-options]; [BES options][bes-options]

Keep links to artifacts together with their availability policy: an event may
reference an artifact instead of containing its bytes. Output uploading and
server access must be configured separately for a remote consumer.
[BEP file schema][bep]; [BEP and remote caching][bep-guide]

## Coverage and next task

Schemas and flags are source-reviewed; no viewer, BES service, or performance
benchmark was integrated. BuildBuddy exploration is tracked in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[profile]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/CommonCommandOptions.java
[trace]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/advanced/performance/json-trace-profile.md
[bep]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventstream/proto/build_event_stream.proto
[bep-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventstream/transports/BuildEventStreamOptions.java
[bes-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventservice/BuildEventServiceOptions.java
[bep-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/bep.md
