---
title: "Protocol versions and server capabilities"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.version.reference", "remote.version.client", "remote.version.features"]
last_verified: "2026-11-05"
---

# Protocol versions and server capabilities

## Use this when

Use this page before assuming a feature in the protocol release is available in
a particular Bazel/server combination.

## Keep four identities

| Layer | Reference in this repository | What it establishes |
| --- | --- | --- |
| Protocol definition | REAPI v2.12.0, commit `9e084d0e43e717128ee72b5be584a7ba33e8006b` | Available protocol fields and their specified meaning. |
| Bazel client | Bazel 9.3.1, commit `fee2bf2d1c14bc2096068a4d46f1842472092044` | This client's declared range and inspected behavior. |
| Server capabilities | No server queried | Must be obtained for the endpoint and relevant instance. |
| Interoperability | No integration run | Must be demonstrated with the intended client, feature, platform, and service. |

Protocol identity is recorded in [the baseline](../versions/baseline.json).
Bazel 9.3.1's `ApiVersion.low` is **2.0** and `ApiVersion.high` is **2.11**.
This is the current client's declaration, not guidance to adopt older build
practices and not a claim of complete implementation of every field in that range.
[ApiVersion][api]

## Inspect capabilities, not a product badge

`ClientApiVersion` intersects client and server API ranges and accounts for a
server-declared deprecated range. `RemoteServerCapabilities` additionally checks
requested cache/execution features: digest functions, execution enablement,
priority ranges, cache-update availability, and compression support, among others.
A compatible version range alone does not satisfy those feature checks.
[Client range check][client]; [feature checks][capabilities]

The protocol's `GetCapabilities` request accepts an instance name. Inspect
`CacheCapabilities` and `ExecutionCapabilities` separately: a server can offer
cache operations without execution, and account authorization may affect what
is available. [Capabilities messages][protocol]; [client execution check][capabilities]

For example, Bazel checks Zstd support when remote-cache compression is requested.
Its experimental chunking path also checks SplitBlob/SpliceBlob and associated
capabilities. Those checks establish implementation paths, not a recommendation
to enable experimental features without an integration test. [Capability checks][capabilities]

## Coverage and next task

The client's declared range and checks were read at the exact Bazel commit.
Neither server responses nor feature interoperability were tested. Recheck this
page when upgrading Bazel independently of the protocol reference.
Continue with [digests and transfers](digests-and-transfers.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[capabilities]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteServerCapabilities.java
[api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/ApiVersion.java
[client]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/ClientApiVersion.java
