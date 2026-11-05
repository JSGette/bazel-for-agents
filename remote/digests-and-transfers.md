---
title: "Digests and artifact transfer"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["remote.digest.identity", "remote.digest.transfer", "remote.digest.compression"]
last_verified: "2026-11-05"
---

# Digests and artifact transfer

## Use this when

Use this page when a cache entry exists but a blob cannot be retrieved, or when
investigating upload/download behavior.

## Identify the data precisely

A REAPI `Digest` contains a hash and byte size. The digest function is established
by the relevant request/capability context; the `Digest` message itself does not
carry an algorithm field. The same bytes under a different algorithm must not be
treated as the same storage identity. Bazel's `DigestUtil` uses its configured
hash function to compute message and file digests. [Digest definition][protocol];
[DigestUtil][digest]

File content is one blob. Serialized commands, directories, and actions are other
blobs. The input root references the entire directory graph by digest; having
just its root message does not prove that every child blob is available.
[Directory, Action, CAS][protocol]

`FindMissingBlobs` identifies absent blobs. CAS batch methods transfer multiple
blobs subject to server limits; ByteStream provides streaming transfer. Servers
advertise batch limits and supported digest/compression capabilities. Follow the
negotiated contract rather than assuming a fixed maximum upload size from a
particular service. [CAS services and CacheCapabilities][protocol]

## Separate content identity from transfer encoding

The protocol supports compressed blob transfer. Compressed ByteStream resource
names identify the **uncompressed** digest and size. Compression changes transport
representation, not the original content identity. [CAS compressed resource names][protocol]

In Bazel 9.3.1, `--remote_cache_compression` defaults to false and requests Zstd
when enabled for eligible blobs. The client checks server support.
`--remote_verify_downloads` defaults to true. These defaults are source facts;
no bandwidth benefit or server compatibility was measured here.
[Options][options]; [capability checks][capabilities]

Our recommendation: distinguish a missing action result, a missing referenced
blob, a digest mismatch, a permission error, and a transient transfer failure.
Preserve the relevant digest, instance, RPC status, and effective feature settings.
Do not disable download verification as a generic repair for a mismatch.

## Coverage and next task

Source-reviewed protocol and Bazel options only. Continue with
[output materialization](outputs-and-downloads.md).

## Evidence

Source review and limitations: [remote claim ledger](../verification/remote.md).

[protocol]: https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java
[capabilities]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteServerCapabilities.java
[digest]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/util/DigestUtil.java
