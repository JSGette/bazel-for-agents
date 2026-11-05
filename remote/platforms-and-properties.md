---
title: "Execution platforms and remote properties"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.platform.distinction", "remote.platform.translation", "remote.platform.lexicon"]
last_verified: "2026-11-05"
---

# Execution platforms and remote properties

## Use this when

Use this page when a selected execution platform needs to describe a remote worker.
Read [platform constraints](../configuration/platforms-and-constraints.md) first.

## Model two contracts

Bazel constraints participate in platform/toolchain compatibility. Remote execution
properties are string key/value requirements sent to the service. The latter do
not themselves replace Bazel's constraint matching. Our recommendation is to make
both describe the same intended worker, then inspect the selected toolchain and
resulting action separately. [Toolchain resolution](../toolchains/resolution.md);
[Bazel property serialization][platform]

Bazel's `PlatformUtils.getPlatformProto` builds the remote property message from
the spawn's combined execution properties and configured defaults. In particular,
`--remote_default_exec_properties` is not a universal overlay on a platform that
already sets `exec_properties`. Avoid inferring the effective message by reading
only the command line. [PlatformUtils][platform]; [flag definition][options]

REAPI defines the representation of a property, but the server defines accepted
names and their interpretation. It may reject unknown properties. A container
image selector, machine pool, or CPU quantity must therefore use that service's
supported contract; this repository does not invent portable property names.
[Platform.Property][protocol]

Platform properties participate in action identity. A property change can affect
cache reuse even when source files and command arguments are unchanged. Properties
should identify a reproducible execution environment; a mutable worker image tag
is a weaker identity than an immutable image reference. The first statement is
protocol semantics; the image-pinning advice is our recommendation.
[Action and Platform][protocol]

## Coverage and next task

Serialization and option behavior were source-reviewed. No scheduler lexicon,
container image, worker pool, or platform integration was tested. Continue with
[execution groups](../toolchains/execution-groups.md) or
[cache diagnosis](../diagnostics/execution-and-cache-misses.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java
[platform]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/platform/PlatformUtils.java
