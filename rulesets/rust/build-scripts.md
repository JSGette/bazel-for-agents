---
title: "Declare Cargo build-script inputs"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/dependencies.md"]
claim_ids: ["rust.buildscript.stages", "rust.buildscript.outputs", "rust.buildscript.annotations", "rust.buildscript.rs-paths"]
last_verified: "2026-11-05"
---

# Declare Cargo build-script inputs

Treat a Cargo build script as a tool built for execution and then run to produce
information for Rust compilation. Our recommendation is to make each file, tool,
and configuration input visible to the Bazel action.

## Separate compilation from execution

The direct public `cargo_build_script` is exported from
`@rules_rust//cargo:defs.bzl`; the facade wrapper is
`@rules_rs//rs:cargo_build_script.bzl`. Both implementations separate building the
script binary from running it. [Direct public export][rust-cargo-public],
[direct wrapper][rust-buildscript], [facade wrapper][rs-buildscript].

| Input | Put it in the appropriate interface |
| --- | --- |
| Rust build dependencies | `deps`, and `proc_macro_deps` where appropriate. |
| Files embedded while compiling the build script | `compile_data`. |
| Files read when the build script runs | `data`. |
| Executables invoked by the running script | `tools`. |
| Environment for compilation of the script | `rustc_env` / `rustc_env_files`. |
| Environment for running the script | `build_script_env` / `build_script_env_files`. |
| Native dependency build metadata | `link_deps`, with `links` identifying the produced native library metadata where applicable. |

[Direct attribute semantics and forwarding][rust-buildscript],
[facade fork semantics][rs-fork-buildscript].

The build-script action emits output-directory content and files carrying compiler
flags/environment/link metadata; dependent Rust rules consume build information.
A script's successful execution is therefore only part of validation: inspect the
resulting compile and link actions as well. [Build action outputs][rust-buildaction].

## Annotate generated crates

For externally generated crates, use the selected integration's annotation fields
for `build_script_data`, `build_script_tools`, `build_script_env`, and related
inputs. Direct Crate Universe additionally exposes controls such as
`build_script_use_cc_toolchain`. Check the exact tag definition instead of
copying an attribute from the other integration.
[Direct annotations][rust-cargo], [facade annotations][rs-crates].

Our recommendation for scripts using native compilers or package discovery is to
supply declared tools and dependency paths, then inspect the action's execution
platform and environment. Do not assume that a local system installation will be
present on an execution worker.

## Keep host-path discovery explicit

The facade's fork exposes
`allow_build_script_to_detect_nonhermetic_paths`, defaulting to false, for scripts
emitting absolute host-system paths in selected Cargo directives. The facade
annotation can opt into it. Treat that as a loss of an input boundary that needs
project-specific justification, not a routine fix for missing native dependencies.
[Facade attribute][rs-fork-buildscript], [annotation][rs-crates].

This option is documented for the facade's pinned fork only. Do not infer that
the direct rules release has the same attribute. Continue to [FFI](ffi.md).

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-crates]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl
[rs-buildscript]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/cargo_build_script.bzl
[rs-fork-buildscript]: https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/cargo/private/cargo_build_script_wrapper.bzl
[rust-cargo]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl
[rust-cargo-public]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/defs.bzl
[rust-buildscript]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/private/cargo_build_script_wrapper.bzl
[rust-buildaction]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/private/cargo_build_script.bzl
