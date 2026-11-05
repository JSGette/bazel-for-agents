---
title: "Model Rust libraries, binaries, and tests"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/choosing-integration.md"]
claim_ids: ["rust.targets.loads", "rust.targets.inputs", "rust.targets.deps", "rust.targets.tests"]
last_verified: "2026-11-05"
---

# Model Rust libraries, binaries, and tests

Use a Rust target to describe a crate's compilation interface. Keep Cargo
resolution separate from the target's declared sources and dependency edges.

## Choose the rule and load surface

Direct rules export `rust_library`, `rust_binary`, `rust_test`, `rust_proc_macro`,
`rust_static_library`, and `rust_shared_library` through
`@rules_rust//rust:defs.bzl`. The `rules_rs` facade exposes individual wrappers for
its normal library, binary, test, and proc-macro rules under `@rules_rs//rs`.
Follow [the public exports][rust-defs] and [facade wrapper][rs-wrapper]; inspect
additional facade exports rather than guessing an equivalent filename.

## Declare the crate interface

| Attribute | Meaning at the inspected implementation |
| --- | --- |
| `srcs`, `crate_root` | Rust source inputs and the entry source passed to rustc; specify `crate_root` when inference would be ambiguous. |
| `edition` | Per-crate edition, otherwise the toolchain's edition. |
| `crate_features` | Feature strings translated into rustc configuration flags. |
| `compile_data` | Files needed at compilation, including files embedded by source macros. |
| `data` | Files needed at compilation and runtime; these can enter runfiles. |
| `deps` | Rust library/build information dependencies. |
| `proc_macro_deps` | Procedural macros; the direct rules configure this edge for execution. |
| `link_deps` | Native linkage dependencies; see [FFI](ffi.md). |

[Direct attributes][rust-rules], [facade implementation attributes][rs-fork-rules].

Our recommendation is to put compile-only embedded assets in `compile_data` so
the runtime closure reflects actual runtime requirements. Keep crate features
explicit; do not infer that a manually declared rule reads its local Cargo
manifest. The rule consumes these [declared attributes][rust-rules].

## Keep procedural macros on their own edge

A proc-macro executes as part of compilation. In direct rules, the
`proc_macro_deps` attribute has `cfg = "exec"`; passing a proc-macro through
`deps`, or a non-proc-macro through `proc_macro_deps`, triggers validation errors.
That distinction matters when the target architecture differs from execution.
[Dependency validation and transition][rust-rules].

## Test the intended compilation unit

`rust_test(crate = ...)` targets the inline tests of another Rust crate. Separate
integration-test source files can form their own test target with normal crate
dependencies. Read the selected rule's `crate`, `srcs`, `deps`, and data attributes
rather than treating a Cargo test invocation as a declaration of Bazel targets.
[Test rule implementation][rust-rules].

The direct public surface also exports documentation, documentation tests,
Clippy, Rustfmt, and rust-analyzer helpers. These are separate targets/aspects;
choose them according to the repository's check policy. Their export here is not
a claim that they run automatically during every Rust build.
[Public helper exports][rust-defs].

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-wrapper]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rust_library.bzl
[rs-fork-rules]: https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/rust/private/rust.bzl
[rust-defs]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/defs.bzl
[rust-rules]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl
