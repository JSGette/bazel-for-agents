---
title: "Set up protobuf rules and compiler selection"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"protobuf": "36.2"}
platforms_verified: []
required_flags: []
prerequisites: []
claim_ids: ["protobuf.setup.loads", "protobuf.setup.compiler", "protobuf.setup.roles", "protobuf.setup.versions"]
last_verified: "2026-11-05"
---

# Set up protobuf rules and compiler selection

Use the `protobuf` module as the source of protobuf's public Bazel rules. The
reviewed candidate is 36.2. Keep its release separate from the language-specific
runtime and plugin versions selected elsewhere in the project.

## Load the explicit public API

`proto_library` is exported from `@protobuf//bazel:proto_library.bzl`.
`ProtoInfo` is exported from `@protobuf//bazel/common:proto_info.bzl`. These names
assume the root module uses the apparent repository name `protobuf`; use the
project's actual mapping when it chooses a different name.
[Rule export][proto-library], [provider export][proto-info-public],
[module identity][proto-module].

The module's own source uses its internal `com_google_protobuf` repository name.
Do not copy that spelling into a consumer without checking the consumer's direct
module declaration. [Module declaration][proto-module].

## Inspect the compiler selection

In protobuf 36.2, `@protobuf//bazel/flags:prefer_prebuilt_protoc` defaults to true.
The module registers prebuilt toolchains and then source-based toolchains as a
fallback. Do not assume every build compiles protoc from source, or that an
arbitrary downloaded protoc on `PATH` is the tool used by the action.
[Flag default][proto-flags], [module registrations][proto-module],
[source toolchains][proto-toolchains].

For a custom compiler, the public `proto_toolchain` macro is in
`@protobuf//bazel/toolchains:proto_toolchain.bzl`. It creates an implementation
and a suffixed toolchain registration target, with execution/target constraints.
The compiler attribute is executable and uses execution configuration.
[Macro][proto-compiler-macro], [implementation][proto-compiler-rule].

Our recommendation is to inspect the resolved toolchain and generated action
before overriding compiler selection. Record why a custom compiler is needed,
its provenance, and the exact execution platform it supports.

## Review versions as an integration

The protobuf module declares dependencies on language rules, C/C++ dependencies,
and supporting libraries. Those manifest entries are dependency requests, not a
resolved compatibility report for this repository's full candidate set.
[Exact manifest][proto-module].

Review compiler, generator plugin, generated-code API, and linked runtime together.
Do not infer cross-language compatibility from one numeric version comparison.
Validate generation and a consuming binary or test in each language before
calling the combination tested.

Continue to [code generation](code-generation.md), [gRPC](grpc.md), and
[Rust Prost](prost.md) according to the consumer language.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[proto-module]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/MODULE.bazel
[proto-library]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/proto_library.bzl
[proto-info-public]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/common/proto_info.bzl
[proto-flags]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/flags/BUILD
[proto-toolchains]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/toolchains/BUILD.bazel
[proto-compiler-rule]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_toolchain_rule.bzl
[proto-compiler-macro]: https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/toolchains/proto_toolchain.bzl
