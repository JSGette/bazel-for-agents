---
title: "Declare package files and defaults"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/visibility.md"]
claim_ids: ["core.build-evaluation", "core.glob-package", "core.glob-patterns", "core.glob-generated", "core.glob-empty-default", "core.glob-labels", "core.filegroup", "core.exports-files", "core.package-defaults", "core.repo-defaults"]
last_verified: "2026-11-05"
---

# Declare package files and defaults

Use this page when maintaining source lists, grouping data files, introducing a
nested package, or choosing package/repository defaults. Start from the owning
package and the consumer's required file/provider interface rather than a broad
filesystem scan. This is the reference's authoring recommendation.

## Treat BUILD evaluation as target declaration

A build file evaluates statements in sequence. Values must exist before use;
calling a rule declares a target rather than executing its compiler or generator.
Ordinary rule declarations can refer to targets declared later in the same
package because their dependency labels are resolved as build graph edges.
[BUILD evaluation][build-files]

Keep reusable computation in `.bzl` functions and keep the build file focused on
its target declarations. The [dialect page](../starlark/dialect-and-contexts.md)
covers file-context restrictions; the [phase page](phases-and-graphs.md) explains
when analysis creates the actions. A `glob()` evaluates while the package is
loaded, before generated build outputs exist. [Glob contract][functions]

## Use globs within a known package boundary

`glob()` returns a sorted, mutable list of package-relative paths matching at
least one include pattern and no exclude pattern. Directories are excluded by
default. Its search stays within the current package: a nested directory with
its own build file is a subpackage, and files under it are excluded even by a
recursive pattern. [API][native-api], [package limitations][functions]

| Pattern element or change | Consequence |
| --- | --- |
| `*` within one path segment | Matches within that segment, not across `/`. |
| `**` as a complete path segment | Matches zero or more path segments, still stopping at subpackages. |
| Adding a nested `BUILD.bazel` | Can remove that subtree from a parent's glob results. |
| Adding a generated file to `bazel-bin` | Does not add it to a source glob. |

[Pattern syntax and package boundaries][functions]

Our recommendation is to name the intended source or data suffixes and directory
scope. A bare `*` or `**` can include build files and other unintended sources;
the upstream `glob_simple` test explicitly includes `BUILD` in its match set.
For a small, curated interface, an explicit file list may communicate ownership
more clearly. [Glob test assertions][glob-tests]

At the default Bazel 9.3.1 settings, `allow_empty` is **False**. Each include
pattern must match something, and the final result after exclusions must also be
nonempty. Use `allow_empty = True` only when absence is intentional; prefer fixing
a typo or unexpected package boundary when it is not.
[Actual default][language-options], [default handling][native-impl],
[argument contract][native-api]

The generated function-reference template still shows `allow_empty=True` in its
signature. The implementation and default flag value establish the baseline
behavior above; do not reproduce the stale signature. No flag change is needed
to obtain the default described here. [Template][functions], [implementation][native-impl]

## Add generated inputs through their producing targets

A source glob never discovers generated artifacts. Reference the producer target
explicitly in the consumer's appropriate label attribute. Whether that means its
default files, a named output group, or a semantic provider depends on the
consumer contract. [Glob limitations][functions],
[outputs and providers](outputs-and-runfiles.md)

The strings returned by `glob()` are interpreted as labels when supplied to label
attributes. A rule with the same name as a matched source path can shadow that
source file. Avoid such name collisions rather than assuming that a glob result
forces source-file interpretation. [Shadowing behavior][functions]

## Give file collections an explicit interface

`filegroup` gathers files from its `srcs` targets under one target label. By
default it gathers their files to build; `output_group` can select an output group
instead. It does not forward arbitrary language-specific providers, so wrapping
a language library in a filegroup is not a substitute for depending on the
library's semantic interface. [Rule attributes][filegroup-rule],
[provider construction][filegroup-impl]

Prefer an explicit filegroup over treating a source directory as an opaque
input: the filegroup identifies the member files for dependency tracking.
Generated directory artifacts have a separate action contract; this guidance
concerns source file collections. [Filegroup guidance][filegroup-rule]

Use `exports_files` when another package intentionally needs direct file labels
instead of a collection target. It declares those source-file targets. Specify
the desired visibility: omitting it exports publicly, independently of the
package's default visibility. See [visibility](visibility.md) for access policy.
[Export API][native-api], [exported target tests][exports-tests]

## Set defaults at the right scope

`package()` declares package metadata and is allowed at most once per build file.
Place it after loads and before targets. Relevant fields include
`default_visibility`, `default_testonly`, and `default_package_metadata`.
These are defaults with attribute-specific rules; `features`, for example, is
merged rather than a universal replacement of each target's feature list.
[Package API][package-call], [argument handling][package-args]

Package default visibility applies to top-level targets/macros that do not supply
their own visibility, with symbolic-macro rules described on the visibility page.
It does not govern `exports_files`. Keep public exports deliberate rather than
assuming one package default describes every access decision.
[Default-visibility contract][functions], [visibility](visibility.md)

For repository-wide defaults, `REPO.bazel` supports `repo()` with the same argument
family as `package()`. It also serves as a repository boundary marker.
`REPO.bazel` does not support `load()` statements and is not the module dependency
manifest. Use [MODULE.bazel](../modules/dependencies-and-version-selection.md)
for dependency declarations. [Repository metadata][overview],
[REPO evaluation][repo-file]

## Evidence boundary

This page is source-verified against Bazel 9.3.1. Upstream test assertions were
inspected, not executed here. There is no new runnable fixture or platform claim.
See [package/file claims](../verification/modules.md#package-files-and-defaults)
for the inspected APIs and known stale-documentation correction.

[build-files]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-files.md
[functions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/docgen/templates/be/functions.vm
[native-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkNativeModuleApi.java
[native-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/StarlarkNativeModule.java
[language-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java
[glob-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/packages/NativeGlobTest.java
[exports-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/packages/ExportsFilesTest.java
[filegroup-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/filegroup/FilegroupRule.java
[filegroup-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/filegroup/Filegroup.java
[package-call]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/PackageCallable.java
[package-args]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/PackageArgs.java
[repo-file]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/RepoFileFunction.java
[overview]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/overview.md
