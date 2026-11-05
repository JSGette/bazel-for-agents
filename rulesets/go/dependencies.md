---
title: "Resolve Go dependencies through go_deps"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_go": "0.65.0", "gazelle": "0.54.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/go/setup.md"]
claim_ids: ["go.dependencies.manifests", "go.dependencies.selection", "go.dependencies.overrides", "go.dependencies.environment"]
last_verified: "2026-11-05"
---

# Resolve Go dependencies through go_deps

## Use this when

Add an imported Go module, diagnose an unexpected version, or customize generated
BUILD files for a third-party dependency. Separate the Bazel module graph from
the Go dependency graph managed by Gazelle's `go_deps` extension.

## Manifest ownership and visible repositories

Use the `go_deps` extension exported by `@gazelle//:extensions.bzl`.
Its `from_file` tag accepts exactly one `go_mod` or `go_work`; only one such tag
is permitted per participating Bazel module. `go_work` expands member manifests.
The `module` tag can declare a dependency directly, but its own API recommends
`from_file` when a manifest can express the requirement.
[Manifest parsing and tag definitions](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl).

The extension aggregates requirements across participating Bazel modules. It can
select a higher Go version than one requested by the root and diagnoses direct
version mismatches. A checked-in root manifest alone is therefore not a report
of the resolved Bazel-integrated Go graph. Modules already provided by Bazel
modules receive special resolution handling.
[module_resolutions and direct-version checks](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl);
[MVS test cases](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/tests/bzlmod/go_deps/mvs.bzl).

Import the generated repositories needed directly by this Bazel module with
`use_repo`. The extension returns direct-dependency metadata so `bazel mod tidy`
can repair those declarations. Preserve checksums in `go.sum`; the extension
checks for conflicting sums. Repository names are generated from module paths,
with a `repo_name` override available for collisions.
[metadata, sums and repository naming](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl).

## Choose the right override

| Need | API |
| --- | --- |
| Change Go module version or replacement | Root manifest `replace` handling |
| Adjust generated BUILD rules | `go_deps.gazelle_override` |
| Patch a module or resolve a repository-name collision | `go_deps.module_override` |
| Supply a different archive with digest and layout | `go_deps.archive_override` |
| Change all modules' generation defaults | `go_deps.gazelle_default_attributes` |

These tags belong to the Go extension; they are not Bazel's similarly named
module override functions. Module/archive patching occurs after Gazelle runs.
Specific Gazelle overrides take precedence over global defaults; global defaults
replace the built-in default override selection, so use them sparingly.
[Override processing and tag contracts](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl).

## Fetch configuration and build configuration

Root `go_deps.config` accepts `go_env`, `go_env_inherit`, and direct-dependency
warning/error policy. The environment fields configure fetches and the developer
Go command; they do not configure Go build actions. Keep compiler settings in
the ruleset's build settings and toolchains. Keep credentials outside checked-in
configuration. [Root config processing](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl);
[Environment scope](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/docs/go/core/bzlmod.md).

Repository recommendation: review manifest changes, checksums, `use_repo`
changes, and generated BUILD changes together. Fetch success does not establish
that an external module's generated targets compile on the desired platform.
Continue with [Gazelle directives](../gazelle/directives.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#go-dependencies).
