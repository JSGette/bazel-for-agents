---
title: "Model protobuf sources and generated libraries"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"protobuf": "36.2", "rules_go": "0.65.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/protobuf/setup.md"]
claim_ids: ["protobuf.sources.graph", "protobuf.sources.providers", "protobuf.codegen.languages", "protobuf.codegen.descriptors"]
last_verified: "2026-11-05"
---

# Model protobuf sources and generated libraries

Keep the schema graph explicit, then attach each required language generator.
Our recommendation is to give a schema library a stable label and avoid making
consumers depend on guessed generated filenames.

## Define the schema graph

`proto_library.srcs` supplies source schemas. `deps` accepts other `ProtoInfo`
providers; it does not accept a language-specific generated library as a schema
dependency. `option_deps` is the separate interface for schemas required only for
custom options. [Rule attributes][proto-rule].

For public imports, represent the exported schema dependency in both `deps` and
`exports`, following the release API contract. `allow_exports` can restrict where
a schema may be re-exported or wrapped by language rules. This is distinct from
ordinary target visibility. [Export-related attributes and checks][proto-rule].

`strip_import_prefix` removes a source path prefix, then `import_prefix` adds the
logical import prefix. Relative strip prefixes are package-relative; absolute
ones are repository-relative. Choose a stable import spelling and inspect it in
the generated action rather than compensating with ad hoc include paths.
[Import path validation and rewriting][proto-rule].

## Consume providers rather than output paths

`ProtoInfo` carries `direct_sources`, `transitive_sources`,
`direct_descriptor_set`, `transitive_descriptor_sets`, and `proto_source_root`,
among other fields. Option-only dependencies participate in source inputs but are
excluded from the transitive descriptor-set closure after descriptor compilation.
[Provider construction][proto-info].

A generator rule should consume that interface and its declared compiler/plugin
inputs. An alias schema with empty `srcs` can expose schemas through `deps` under
a stable label. [Schema rule][proto-rule].

## Choose the language interface

| Consumer | Public entry point | Schema input |
| --- | --- | --- |
| C/C++ | `cc_proto_library` from `@protobuf//bazel:cc_proto_library.bzl` | `deps` on schema libraries. |
| Python | `py_proto_library` from `@protobuf//bazel:py_proto_library.bzl` | `deps` on schema libraries. |
| Go | `go_proto_library` from `@rules_go//proto:def.bzl` | `protos` plus explicit `importpath`; Go dependency edges are separate. |
| Rust Prost | `rust_prost_library` from the selected Prost integration | See [Prost](prost.md); the attribute is `proto`. |

[C++ implementation][proto-cc-impl], [Python implementation][proto-python-impl],
[Go rule and attributes][go-proto]. The language wrapper owns language compilation
and runtime dependencies; source descriptors alone do not replace that wrapper.

The Go rule exposes generated sources through the `go_generated_srcs` output
group. Its ordinary default output can instead be the compiled Go archive.
Choose the interface needed by the downstream task. [Go output selection][go-proto].

## Export descriptors deliberately

For tooling that needs one descriptor set, use `proto_descriptor_set` from
`@protobuf//bazel:proto_descriptor_set.bzl`. It collects transitive descriptor sets
from its `deps` and combines them into its `.pb` output.
[Descriptor rule][proto-descriptors].

Our validation recommendation is to check import paths, generated APIs, and a
real consuming target. A successful descriptor build does not exercise language
linking or service-code generation. Continue to [gRPC](grpc.md) for services.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[proto-rule]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_library_rule.bzl
[proto-info]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_info.bzl
[proto-cc-impl]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/cc_proto_library.bzl
[proto-python-impl]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/py_proto_library.bzl
[proto-descriptors]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/proto_descriptor_set.bzl
[go-proto]: https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/def.bzl
