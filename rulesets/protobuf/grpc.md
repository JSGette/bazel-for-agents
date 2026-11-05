---
title: "Select gRPC generation by language"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"protobuf": "36.2", "rules_go": "0.65.0", "rules_rust_prost": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/protobuf/code-generation.md"]
claim_ids: ["grpc.go.wrapper", "grpc.go.runtime", "grpc.rust.tonic"]
last_verified: "2026-11-05"
---

# Select gRPC generation by language

Choose the generator and runtime as a language-specific pair. This reference
covers the inspected Go and Rust entry points. It does not select an unverified
C++ or Python gRPC ruleset release.

## Go: use the current service wrapper

`go_grpc_library` is exported by `@rules_go//proto:def.bzl`. In rules_go 0.65.0,
its default `compilers` list contains `@rules_go//proto:go_proto` and
`@rules_go//proto:go_grpc_v2`. The first generates message types; the second uses
`protoc-gen-go-grpc` and the `_grpc.pb.go` output suffix.
[Wrapper implementation][go-proto], [compiler definitions][go-plugins].

Provide `protos` and a Go `importpath`, then declare the Go dependencies needed by
the consumer. The release includes a module-based service-generation and Go-test
fixture demonstrating that interface. The fixture was inspected here, not run.
[Upstream fixture][go-proto-test].

The compiler targets carry implicit Go runtime dependencies through
`GoProtoCompiler`; changing a plugin is more than changing an executable name.
When supplying a custom `compilers` list, review output suffixes, generated API,
plugin options, and runtime dependencies together. In particular, setting the
list replaces the wrapper defaults. [Compiler provider][go-compiler],
[wrapper defaults][go-proto].

The supplied `go_grpc_v2` compiler sets
`require_unimplemented_servers=false`. Treat that as this ruleset's generator
configuration, not the universal upstream plugin default.
[Compiler options][go-plugins].

## Rust: configure Tonic through the Prost toolchain

`rules_rust_prost` models Tonic generation through `tonic_plugin`,
`tonic_plugin_flag`, and `tonic_runtime`. The plugin is execution-configured; the
runtime is Rust build information for generated code. The implementation checks
that the Tonic configuration is complete. Its shipped default toolchain supplies
both Prost and Tonic components. [Rule attributes and checks][prost-rules],
[default implementation][prost-runtime].

Keep the Prost/Tonic provider family aligned with either direct Rust rules or the
`rules_rs` facade; see [the dedicated integration page](prost.md).

## Validate the service boundary

Our recommendation is to test message generation, client/server API compilation,
and a small service interaction separately. Generation alone cannot establish
transport behavior or application interoperability. Record plugin/runtime versions
from the selected module/Cargo/Go dependency graph before upgrading.

C++ and Python gRPC setup remains a release-selection and integration-test gap.
Do not infer a gRPC rule or module version from the protobuf version, and do not
invent a universal `grpc_library` API to fill that gap.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[prost-rules]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/prost.bzl
[prost-runtime]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/BUILD.bazel
[go-proto]: https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/def.bzl
[go-plugins]: https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/BUILD.bazel
[go-compiler]: https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/compiler.bzl
[go-proto-test]: https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/tests/bcr/proto/BUILD.bazel
