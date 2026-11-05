---
title: "Resolve Cargo dependencies"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_rs": "0.2.1", "rules_rust": "0.75.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/rust/choosing-integration.md"]
claim_ids: ["rust.cargo.rs-inputs", "rust.cargo.rs-helpers", "rust.cargo.direct-inputs", "rust.cargo.annotations"]
last_verified: "2026-11-05"
---

# Resolve Cargo dependencies

Preserve the project's selected Cargo integration and its lockfiles. Our
recommendation is to review dependency resolution separately from generated BUILD
changes and compiler/toolchain changes.

## `rules_rs`: resolve a Cargo workspace

Its `crate` extension is in `@rules_rs//rs:extensions.bzl`.
`from_cargo` requires `cargo_toml`, `cargo_lock`, and `platform_triples`; `name`
selects the generated hub. The platform list must cover the union of execution
and target triples involved in the build. Lockfile validation is enabled by
default. [Tag definitions][rs-crates].

The generated hub's `defs.bzl` exports `aliases`, `all_crate_deps`, `crate_name`,
`edition`, and `lint_config`. Dependency selection is package-sensitive:
`all_crate_deps` distinguishes normal, development, and build dependencies and
accepts an explicit `package_name`. Do not transplant a helper call between
packages without checking which manifest member it selects.
[Generated helper definitions][rs-crates].

`crate.config` supplies root-controlled shared Cargo configuration; a
`from_cargo(cargo_config = ...)` can supply closure-specific configuration.
Registry credentials are an explicit integration choice. Keep them out of
committed manifests and generated files. The extension's Git policy also has an
explicit `allow_git_cli` setting, with `RULES_RS_ALLOW_GIT` as the declared
environment override. [Configuration and fetch policy][rs-crates].

## Direct `rules_rust`: Crate Universe

Load `crate` from `@rules_rust//crate_universe:extensions.bzl`.
`from_cargo` takes `manifests` and `cargo_lockfile`; `from_specs` works from
`crate.spec` tags. `supported_platform_triples` controls generated platform
coverage. The `lockfile` attribute is a separate reproducible-rendering lockfile,
not another spelling for Cargo's lockfile. [Extension API][rust-cargo].

For a non-root module, a rendering lockfile is required and trusted as supplied;
the extension does not repin it in the consuming project's read-only dependency
cache. For the root, repinning and Cargo-lockfile overwrite behavior have
explicit controls. Review generated lock changes deliberately and preserve the
project's chosen policy. [Generation and repinning implementation][rust-cargo].

Use generated `aliases`/dependency helpers and inspect the generated hub before
hardcoding crate labels. The default direct-rule alias template uses per-crate
subpackages. Do not assume the facade's root-package aliases or Cargo attribute
names apply to Crate Universe. [Rendering configuration][rust-cargo],
[facade hub generation][rs-crates].

## Add native or generated inputs through annotations

Both integrations expose `annotation` tags with crate/version/repository scope.
Their fields can add features, build-script data/tools/environment, and native
linkage dependencies, but the accepted fields are integration-specific. Use an
annotation instead of editing a generated external BUILD file.
[Facade annotations][rs-crates], [direct annotations][rust-cargo].

Continue to [build scripts](build-scripts.md) when a crate discovers a compiler,
header, native library, or generated source during its build.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[rs-crates]: https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl
[rust-cargo]: https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl
