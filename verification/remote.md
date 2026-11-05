# Remote reference: source evidence

Reviewed 2026-11-05 against Bazel9.3.1 commit
`fee2bf2d1c14bc2096068a4d46f1842472092044` and REAPI v2.12.0 commit
`9e084d0e43e717128ee72b5be584a7ba33e8006b`.

All records below are **source-verified**. No server was queried, credentials
configured, remote action run, or performance benefit measured. Commands, fixture,
expected runtime output, and observed runtime output are not applicable to this
source-only review. Protocol semantics and Bazel implementation are separate.
Each page places exact-source links beside the relevant statements. Recommendations
about diagnostic sequencing or project integration are editorial guidance.

| Claim ID | Bounded assertion / inspected source |
| --- | --- |
| `remote.model.services` | CAS, AC, Execution and Capabilities have separate contracts: protocol service definitions. |
| `remote.model.action` | Action references Command/input Directory by digest and includes timeout/platform: protocol Action; RemoteExecutionService.buildRemoteAction/buildCommand. |
| `remote.model.result` | ActionResult carries outputs/exit/streams; output format permits Tree and/or Directory encodings, whose digests are not interchangeable; inspected Bazel download path reads tree_digest: protocol Command/OutputDirectory and RemoteExecutionService. |
| `remote.cache.transport` | remote_cache supports cache transports separately from remote_executor: RemoteOptions. |
| `remote.cache.controls` | Read/upload defaults true; upload capability warning: RemoteOptions and RemoteServerCapabilities. |
| `remote.cache.identity` | Remote identity depends on declared command/input graph; local reuse can mask remote lookup: protocol and cache docs. |
| `remote.execution.client` | Bazel builds remote action from analyzed spawn: RemoteExecutionService; phases ledger. |
| `remote.execution.lifecycle` | Execute returns operation/response, may use cache; action timeout scopes execution: protocol. |
| `remote.execution.fallback` | remote_local_fallback defaults false and controls eligible failure fallback: RemoteOptions. |
| `remote.version.reference` | Pinned protocol reference is v2.12.0: baseline release identity and protocol source. |
| `remote.version.client` | Declared Bazel range is2.0–2.11; range intersection/deprecation logic: ApiVersion and ClientApiVersion. |
| `remote.version.features` | Checks distinguish execution/cache digests, enablement, priorities, updates, compression and chunking: RemoteServerCapabilities. |
| `remote.platform.distinction` | Constraint matching and remote property serialization are distinct: toolchains ledger and PlatformUtils. |
| `remote.platform.translation` | Default exec properties are conditional, not unconditional overlay: PlatformUtils.getPlatformProto and RemoteOptions. |
| `remote.platform.lexicon` | Server defines property names/interpretations; properties affect action digest: protocol Platform. |
| `remote.digest.identity` | Digest is hash+size; algorithm comes from context; Bazel computes through configured hash: protocol Digest and DigestUtil. |
| `remote.digest.transfer` | Missing/blob/batch/stream transfers and limits have distinct contracts: protocol CAS and CacheCapabilities. |
| `remote.digest.compression` | Compressed transfers preserve uncompressed identity; Bazel compression false/download verification true defaults: protocol and RemoteOptions. |
| `remote.outputs.policy` | remote_download_outputs default toplevel with minimal/toplevel/all: RemoteOptions. |
| `remote.outputs.local` | Local use and top-level/test selection influence materialization: RemoteOutputChecker and RemoteExecutionService. |
| `remote.outputs.result` | Result metadata, CAS contents, and local filesystem are distinct: protocol ActionResult/ExecuteResponse. |

## Exact sources

- [protocol](https://github.com/bazelbuild/remote-apis/blob/9e084d0e43e717128ee72b5be584a7ba33e8006b/build/bazel/remote/execution/v2/remote_execution.proto)
- [options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/options/RemoteOptions.java)
- [service](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteExecutionService.java)
- [capabilities](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteServerCapabilities.java)
- [api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/ApiVersion.java)
- [client](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/ClientApiVersion.java)
- [digest](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/util/DigestUtil.java)
- [output](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/RemoteOutputChecker.java)
- [platform](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/platform/PlatformUtils.java)
- [cache](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/caching.md)
- [cache-debug](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/cache-remote.md)
- [utils](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/remote/util/Utils.java)
