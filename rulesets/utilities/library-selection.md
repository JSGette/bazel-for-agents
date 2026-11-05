---
title: "Choose a Starlark utility library"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"bazel_lib": "3.7.2", "bazel_skylib": "1.9.2", "bazel_features": "1.54.1"}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/collections.md"]
claim_ids: ["utilities.skylib", "utilities.bazel-lib", "utilities.directory-path", "utilities.features"]
last_verified: "2026-11-05"
---

# Choose a Starlark utility library

Start with the current Bazel language and builtins. Our recommendation is to add
a library when its supported interface expresses a real need, and load the
narrowest public entry point that provides it.

## Select by responsibility

| Need | Reviewed library and public interface |
| --- | --- |
| Path-string operations | `bazel_skylib` 1.9.2: `paths` from `@bazel_skylib//lib:paths.bzl`. |
| Combining configuration conditions | `selects` from `@bazel_skylib//lib:selects.bzl`, including `with_or` and `config_setting_group`. |
| Typed build-setting targets | Common rules and `BuildSettingInfo` from `@bazel_skylib//rules:common_settings.bzl`. |
| Copying files/directories into a generated tree | `bazel_lib` 3.7.2: `copy_to_directory` from `@bazel_lib//lib:copy_to_directory.bzl`. |
| Passing a path inside a tree artifact | `DirectoryPathInfo` / `directory_path` from `@bazel_lib//lib:directory_path.bzl`. |
| An explicit generated parameter-file target | `params_file` from `@bazel_lib//lib:params_file.bzl`. |
| Inspecting a supported Bazel capability predicate | `bazel_features` 1.54.1: `bazel_features` from `@bazel_features//:features.bzl`. |

[Skylib paths][skylib-paths], [configuration helpers][skylib-selects],
[settings][skylib-settings], [copy rule][lib-copy], [directory interface][lib-path],
[parameter files][lib-params], [feature predicates][features].

## Keep library helpers distinct from language types

Use the builtin `set()` for local unique collections and `depset` for transitive
artifact propagation; see [collections](../../starlark/collections.md). A utility
library's continued export of a helper is not a reason to reproduce its internal
implementation or replace a current builtin.

Skylib's common setting rules return `BuildSettingInfo.value`. That is the
library's provider contract, distinct from a custom provider a project might use
for its own settings. [Provider and setting definitions][skylib-settings].

## Know when a helper introduces execution tools

`copy_to_directory` is an action-producing rule with a dedicated toolchain.
`bazel_lib`'s module provisions and registers its supporting toolchains. This is
more than a pure string manipulation library; include those resolved tool versions
in integration evidence. [Rule][lib-copy], [module toolchains][lib-module].

`directory_path` returns `DirectoryPathInfo(directory, path)` after checking that
`directory` is a tree artifact. It does not declare an independent `File` for the
nested path. Consumers must understand that provider.
[Provider and implementation][lib-path-impl].

For action arguments, prefer the consuming rule's `ctx.actions.args()` interface
when appropriate; choose a separate parameter-file target only when that file is
itself a useful declared build product. The library rule has its own path-variable
and newline semantics. [Parameter-file API][lib-params].

## Use feature detection for a specific capability

`bazel_features` contains per-feature predicates and exported globals. Its module
creates the supporting repositories. A true predicate is a statement about that
feature's implementation rule, not a certificate that an arbitrary ruleset graph
works on Bazel 9.3.1. [Predicates][features], [module][features-module].

Our recommendation for this modern-only reference is to avoid speculative
compatibility branches. Verify the selected Bazel baseline directly and add a
capability check only when the supported range or API actually requires one.

Continue to [prebuilt tools](multitool.md), [regex](regex.md),
[TOML](toml.md), or [configuration wrappers](configuration-wrappers.md).

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[lib-copy]: https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/copy_to_directory.bzl
[lib-path]: https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/directory_path.bzl
[lib-params]: https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/params_file.bzl
[lib-module]: https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/MODULE.bazel
[skylib-settings]: https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/rules/common_settings.bzl
[skylib-paths]: https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/paths.bzl
[skylib-selects]: https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/selects.bzl
[features]: https://github.com/bazel-contrib/bazel_features/blob/6f5b91edb290af78d50ea12c8c2db44d46f1fcde/features.bzl
[features-module]: https://github.com/bazel-contrib/bazel_features/blob/6f5b91edb290af78d50ea12c8c2db44d46f1fcde/MODULE.bazel
[lib-path-impl]: https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/private/directory_path.bzl
