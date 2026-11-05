# Diagnostics: source evidence

Reviewed 2026-11-05 against Bazel9.3.1 commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`.

All new diagnostic guidance is source-verified. The existing foundations record
owns the runtime evidence for simple query, cquery files, and aquery observations.
No new diagnostic integration, remote service, log-consumer, or performance suite
was executed. Page-local source links identify the inspected section/symbol.

| Claim IDs | Source scope |
| --- | --- |
| `diagnostics.query.graph`, `diagnostics.query.operators` | [query](../diagnostics/query.md): exact-source links beside each bounded assertion. |
| `diagnostics.cquery.configuration`, `diagnostics.cquery.outputs` | [cquery](../diagnostics/cquery.md): exact-source links beside each bounded assertion. |
| `diagnostics.aquery.graph`, `diagnostics.aquery.filters`, `diagnostics.aquery.identity` | [aquery](../diagnostics/aquery.md): exact-source links beside each bounded assertion. |
| `diagnostics.modules.graph`, `diagnostics.modules.repositories` | [module-resolution](../diagnostics/module-resolution.md): exact-source links beside each bounded assertion. |
| `diagnostics.toolchains.debug`, `diagnostics.toolchains.layers` | [toolchain-resolution](../diagnostics/toolchain-resolution.md): exact-source links beside each bounded assertion. |
| `diagnostics.execution.logs`, `diagnostics.execution.compare`, `diagnostics.execution.summary` | [execution-and-cache-misses](../diagnostics/execution-and-cache-misses.md): exact-source links beside each bounded assertion. |
| `diagnostics.profile.trace`, `diagnostics.bep.events`, `diagnostics.bep.transport` | [profiles-and-build-events](../diagnostics/profiles-and-build-events.md): exact-source links beside each bounded assertion. |

## Exact sources

- [query](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/language.md)
- [cquery](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/cquery.md)
- [aquery](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/aquery.md)
- [aoptions](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/query2/aquery/AqueryOptions.java)
- [modules](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/mod-command.md)
- [platform](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java)
- [cache](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/cache-remote.md)
- [execution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/exec/ExecutionOptions.java)
- [spawn](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/protobuf/spawn.proto)
- [profile](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/CommonCommandOptions.java)
- [trace](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/advanced/performance/json-trace-profile.md)
- [bep](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventstream/proto/build_event_stream.proto)
- [bep-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventstream/transports/BuildEventStreamOptions.java)
- [bes-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/buildeventservice/BuildEventServiceOptions.java)
- [bep-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/bep.md)
