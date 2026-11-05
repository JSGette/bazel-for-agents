---
title: "Configure Rust toolchains"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/choosing-integration.md"]
claim_ids: ["rust.setup.rs-tags", "rust.setup.rs-selection", "rust.setup.direct", "rust.setup.host-cargo"]
last_verified: "2026-11-05"
---

# Configure Rust toolchains

Use this after [choosing the integration](choosing-integration.md). Our
recommendation is to record a compiler version and edition explicitly, then check
the execution/target pairs the project actually needs.

## Configure `rules_rs`

Use the `toolchains` extension from
`@rules_rs//rs/toolchains:module_extension.bzl`. Its `toolchain` tag has `name`,
`version`, `edition`, `rustfmt_version`, `rust_analyzer_version`,
`extra_rustc_flags`, and `extra_exec_rustc_flags`. The default generated repository
name is `default_rust_toolchains`. Expose that repository before referring to its
toolchain targets. The release's default compiler is an implementation choice,
not this reference's recommendation for a current Rust release.
[Tag definitions and repository generation][rs-toolchains].

For a shared repository name, a root-module declaration controls the whole
configuration. Without one, dependency declarations select maxima for compiler,
edition, Rustfmt, and rust-analyzer; conflicting flags and incomparable compiler
channels fail. Conflicting root declarations also fail. Do not assume that the
first dependency's tag wins. [Selection implementation][rs-toolchain-selection].

The separate `host_cargo` tag accepts existing Cargo executable files for the
machine running repository setup. It is root-only and selects host OS/architecture
independently of the target being compiled. Do not substitute a build output for
an executable required before ordinary build actions can run.
[Host Cargo attributes and selection][rs-toolchains].

## Configure direct `rules_rust`

Use `rust` from `@rules_rust//rust:extensions.bzl`. Its `toolchain` tag uses a
`versions` list, an `edition`, and optional target/flag settings. Root tags replace
the module's default toolchain declarations; an empty `versions` list suppresses
default toolchain generation by creating an empty hub. The module registers the
`rust_toolchains` hub. [Extension implementation][rust-tools],
[module registration][rust-module].

`repository_set` is the more specific interface for execution triples, target
triples, matching constraints, and component settings. Use it only when the
ordinary `toolchain` tag cannot express the project requirement; verify the exact
pair instead of assuming that a downloaded target standard library proves the
linker and runtime are available. [Repository-set attributes][rust-tools].

## Review before building

Record compiler, edition, Cargo used for resolution, formatter/analyzer versions,
and required execution/target triples. Inspect root overrides and generated
repositories before diagnosing a version mismatch. These settings can be selected
independently in [rules_rs][rs-toolchain-selection] and
[direct toolchains][rust-tools].

For cross compilation, continue to [native linking](ffi.md). Cargo dependency
platform coverage is a separate decision covered in [dependencies](dependencies.md).

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-toolchains]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/module_extension.bzl
[rs-toolchain-selection]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/toolchain_config.bzl
[rust-module]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/MODULE.bazel
[rust-tools]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl
