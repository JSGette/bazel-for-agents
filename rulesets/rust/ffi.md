---
title: "Link Rust and native libraries"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/targets.md"]
claim_ids: ["rust.ffi.link-deps", "rust.ffi.outputs", "rust.ffi.exec-target", "rust.ffi.bindgen-facade"]
last_verified: "2026-11-05"
---

# Link Rust and native libraries

Use this when Rust consumes C/C++ libraries, C/C++ consumes Rust, or binding
generation introduces an extra compiler tool.

## Put native libraries on the linkage interface

For direct rules 0.75.0, prefer `link_deps` for native libraries. The rule separates
Rust `deps`, `proc_macro_deps`, and native linkage. For non-proc-macro targets, a CcInfo-only target passed
through ordinary `deps` produces a warning in the inspected implementation.
The `rust_proc_macro` rule does not expose `link_deps` and is excluded from that
warning.
`link_deps` accepts `CcInfo` or the Rust crate provider.
[Dependency validation and attributes][rust-rules].

The facade's pinned fork also exposes `link_deps`; its implementation is a
separately reviewed source, not proof that every direct-rule option behaves
identically. Its Cargo annotations can add `link_deps` to generated crates.
[Facade rules][rs-fork-rules], [annotations][rs-crates].

Our recommendation is to use a native dependency's declared provider interface
instead of injecting a machine-specific library search path. Check headers,
link flags, shared-library runtime availability, and target ABI as one interface.
The Rust rule's native edge is provider-based. [Direct attributes][rust-rules].

## Export the artifact the consumer expects

Direct rules provide `rust_static_library` for a static native library and
`rust_shared_library` (a Rust `cdylib`) for a dynamic library intended for foreign consumers. These
rules return `CcInfo`. `rust_dylib_library` is a distinct Rust dynamic-library
rule; do not choose it merely because the desired filename is a shared object.
[Exports][rust-defs], [rule implementations][rust-rules].

Bazel's providers describe build linkage; they do not establish an application ABI.
Our recommendation is to review exported symbols, ownership, error handling, and
runtime deployment in the language boundary itself, then validate a real consumer
binary for each required target platform.

## Distinguish the two platform roles

Proc-macros are execution-configured dependencies; target libraries are part of
the artifact being linked. The direct toolchain API separately describes execution
and target triples and constraints. A cross build needs compatible native target
inputs as well as a compiler that can run on the execution platform.
[Proc-macro edge][rust-rules], [toolchain parameters][rust-tools].

For binding generation, inspect the exact integration before adding Clang or a
bindgen plugin. The facade exposes a `rules_rust_bindgen` provisioning extension;
this page does not establish the compatibility of an independently selected
bindgen release, libclang, SDK, or target sysroot.
[Facade provisioning][rs-bindgen].

Continue to [build scripts](build-scripts.md) for native crate configuration and
[Prost](../protobuf/prost.md) for generated Rust protocol types.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-crates]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl
[rs-fork-rules]: https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/rust/private/rust.bzl
[rs-bindgen]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust_bindgen.bzl
[rust-tools]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl
[rust-defs]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/defs.bzl
[rust-rules]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl
