---
title: "Integrate Rust Prost and Tonic"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rust_prost": "0.75.0", "rules_rust": "0.75.0", "rules_rs": "0.2.1"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/choosing-integration.md", "rulesets/protobuf/code-generation.md"]
claim_ids: ["prost.direct.module", "prost.rule.proto", "prost.toolchain.roles", "prost.facade"]
last_verified: "2026-11-05"
---

# Integrate Rust Prost and Tonic

Start by identifying the [Rust integration](../rust/choosing-integration.md).
The direct Prost module and the facade's generated Prost repository share public
symbol names but use different provisioning paths.

## Direct `rules_rust_prost`

The BCR module `rules_rust_prost` 0.75.0 is the `extensions/prost` portion of the
rules_rust release. It declares direct `rules_rust` 0.75.0 and other dependencies,
then registers `//:default_prost_toolchain`.
[Module manifest][prost-module], [registration target][prost-build].

Load `rust_prost_library` and `rust_prost_toolchain` from
`@rules_rust_prost//:defs.bzl`. A `rust_prost_library` takes the mandatory `proto`
attribute, constrained to `ProtoInfo`; it applies generation through an aspect
and returns Rust crate-group information for consumers. It is not a rule with a
`protos` or schema `deps` parameter. [Exports][prost-defs], [rule][prost-rules].

The release's `defs.bzl` narrative says no default toolchain is supplied, but the
actual module registration and BUILD target above do supply one. This guidance
follows the executable declarations. Do not add a duplicate custom toolchain
solely to satisfy that stale narrative.

## Customize the whole generator/runtime set

The toolchain includes `prost_plugin`, `prost_runtime`, `prost_types`, and optional
Tonic plugin/runtime fields. Plugins are executable dependencies in execution
configuration; runtime attributes require Rust crate providers. The default
implementation wires the release's own crate targets.
[Toolchain rule][prost-rules], [default targets][prost-runtime].

To omit Tonic from a custom toolchain, all three Tonic fields must be empty.
`tonic_plugin_flag` has a nonempty default, so omitting only `tonic_plugin` and
`tonic_runtime` does not disable Tonic: the implementation rejects that partial
configuration. [Completeness check and attribute defaults][prost-rules].

`compile_well_known_types` and `include_transitive_deps` are explicit choices;
their rule defaults are true and false respectively. Review them against the
project's well-known-type and import policy. Avoid supplying the deprecated
`proto_compiler` attribute: the implementation obtains protoc through proto
toolchain resolution when that attribute is unset. This is source/API guidance,
not a tested custom toolchain recipe. [Implementation][prost-rules].

Our recommendation is to align generator plugins and runtime crates as one
reviewed change, including application crates that directly depend on Prost or
Tonic. A duplicate crate name in a different generated repository does not by
itself establish a matching provider or generated-code API.

## `rules_rs` facade

The `rules_rust_prost` extension in
`@rules_rs//rs:rules_rust_prost.bzl` generates a repository re-exporting the
facade's pinned fork. Its default toolchain points at the facade's own
`rs/private/prost` runtime/plugin targets, including its Tonic runtime group.
[Generated repository][rs-prost], [runtime wiring][rs-prost-runtime].

Use that provisioning path when the project deliberately selects the facade.
Do not silently replace it with a BCR `bazel_dep` carrying the same apparent
name. Inspect repository mappings and the resolved generator/runtime graph before
combining Rust and generated protocol targets.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-prost]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust_prost.bzl
[rs-prost-runtime]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/private/prost/BUILD.bazel
[prost-module]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/MODULE.bazel
[prost-defs]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/defs.bzl
[prost-rules]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/prost.bzl
[prost-build]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/BUILD.bazel
[prost-runtime]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/BUILD.bazel
