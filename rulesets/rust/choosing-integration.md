---
title: "Choose a Rust integration"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: []
claim_ids: ["rust.integration.facade", "rust.integration.apis", "rust.integration.dependencies"]
last_verified: "2026-11-05"
---

# Choose a Rust integration

Choose the integration already used by the project before adding a Rust target.
Our recommendation is to keep one coherent toolchain, Cargo resolution, and rule
provider family within a Rust dependency closure.

## Identify the public surface

| Decision | `rules_rs` 0.2.1 | Direct `rules_rust` 0.75.0 |
| --- | --- | --- |
| Basic target loads | Individual files under `@rules_rs//rs`, such as `:rust_library.bzl` | `@rules_rust//rust:defs.bzl` |
| Rust toolchains | `toolchains` from `@rules_rs//rs/toolchains:module_extension.bzl` | `rust` from `@rules_rust//rust:extensions.bzl` |
| Compiler version attribute | `toolchains.toolchain(version = ...)` | `rust.toolchain(versions = ...)` |
| Cargo dependencies | `crate` from `@rules_rs//rs:extensions.bzl` | `crate` from `@rules_rust//crate_universe:extensions.bzl` |
| Cargo manifest inputs | `cargo_toml`, `cargo_lock`, `platform_triples` | `manifests`, `cargo_lockfile`, `supported_platform_triples`; optional rendering `lockfile` |

These are API comparisons, not interchangeable setup fragments.
[Rule facade][rs-wrapper], [rules_rs toolchains][rs-toolchains],
[rules_rs Cargo][rs-crates], [direct toolchains][rust-tools],
[direct Cargo][rust-cargo].

## Understand what the facade owns

`rules_rs` is not a version alias for the BCR `rules_rust` module. Its extension
fetches a checksum-pinned archive from the `hermeticbuild/rules_rust` fork at
`2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733`; the `rs` wrappers load that repository.
Its module also declares its own native/tooling dependencies.
[Provisioning][rs-fork], [module manifest][rs-module].

A separately declared `bazel_dep` on `rules_rust` selects a module through module
resolution; it does not replace the archive created by that extension. Inspect
which repository a label resolves to before combining generated code or custom
provider consumers. This recommendation follows the actual separate provisioning
paths in the [facade][rs-fork] and [direct module][rust-module].

## Decide from requirements

Prefer the project's existing integration. For a new integration, assess Cargo
manifest workflow, required execution/target triples, native ABI, registry access,
and ownership of compiler updates. The facade provides its own Cargo closure and
toolchain APIs; direct rules expose Crate Universe and upstream toolchain APIs.
Choose deliberately rather than mixing whichever snippets are easiest to find.
[Cargo APIs][rs-crates], [Crate Universe APIs][rust-cargo].

Keep three version decisions separate in review: ruleset release, Rust compiler
and edition, and resolved crate versions. The first two are visibly separate
module/tag fields in both [rules_rs][rs-module] and [direct rules][rust-tools].
This repository has not established a performance or compatibility advantage for
either integration.

Continue to [setup](setup.md), then [targets](targets.md) and
[dependencies](dependencies.md). Read [Prost](../protobuf/prost.md) before choosing
Rust protobuf integration.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-module]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/MODULE.bazel
[rs-fork]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust.bzl
[rs-wrapper]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rust_library.bzl
[rs-toolchains]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/module_extension.bzl
[rs-crates]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl
[rust-module]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/MODULE.bazel
[rust-tools]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl
[rust-cargo]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl
