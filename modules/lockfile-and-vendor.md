---
title: "Maintain lockfiles and selected vendored dependencies"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["modules/dependencies-and-version-selection.md", "modules/extensions-and-generated-repositories.md"]
claim_ids: ["modules.lock-content", "modules.lock-modes", "modules.lock-lazy", "modules.lock-hidden", "modules.lock-reproducible-facts", "modules.vendor-scope", "modules.vendor-exclusions", "modules.vendor-pin", "modules.vendor-stale", "modules.vendor-subcommands", "modules.vendor-symlinks"]
last_verified: "2026-11-05"
---

# Maintain lockfiles and selected vendored dependencies

Use this page when reviewing dependency changes, making CI reject stale resolution
state, or preparing an offline build. Keep the manifest, public lockfile, fetched
repository contents, and build-action outputs conceptually separate: they serve
different purposes. [Lockfile contents][lock], [vendor model][vendor]

## Review what the lockfile records

`MODULE.bazel.lock` records registry-file hashes and extension-related state,
including generated repository specifications and tracked inputs when applicable.
It is not a copy of downloaded source trees or an action cache. The manifest and
resolution algorithm still determine module selection; the lockfile preserves
inputs and reusable extension results. [Lockfile schema][lock],
[extension evaluation][extension-eval]

Commit the public lockfile together with the dependency change and the project's
exact Bazel selection. Review changes to registry identities, extension inputs,
and repository specifications rather than accepting a lockfile diff only because
it is machine-generated. This is the reference's maintenance recommendation.

| `--lockfile_mode` | Baseline behavior |
| --- | --- |
| `update` | Default; reuse current information and write missing or changed information. |
| `refresh` | Also refresh mutable registry information, such as yanked versions and previously missing modules. |
| `error` | Require the needed lockfile information to be current; fail rather than updating it. |
| `off` | Neither read nor update the public lockfile. |

[Option definition][options], [mode behavior][lock], [mode tests][lock-tests]

`error` is a consistency mode, not a general network sandbox. Reproducible
extensions may still be evaluated and make network requests, and fetching/building
has its own inputs and transport. A lockfile by itself does not establish that an
arbitrary build is fully offline or hermetic. [Error-mode boundary][lock],
[reproducible extension evaluation][extension-eval]

## Account for lazy and platform-specific extensions

A normal build need not evaluate every declared extension. Lockfile extension
entries can reflect extensions evaluated in current or earlier invocations;
entries for extensions no longer used are removed. `bazel mod deps` forces
extension evaluation. OS- or architecture-dependent extensions can have distinct
recorded evaluations. [Extension coverage][lock], [extension evaluation][extension]

Bazel also maintains a hidden lockfile under the output base. Its format is
unspecified and it is a performance optimization. Reproducible extension results
can be reused there even though their ordinary result entries are omitted from
the public lockfile. Persistent extension **facts** can still be stored publicly
for reproducible extensions. [Hidden lockfile][lock], [evaluation implementation][extension-eval],
[facts tests][lock-tests]

Resolve manifest conflicts first, then regenerate appropriate extension state
with the pinned Bazel version and review the result. Do not hand-edit generated
repository specifications as a substitute for fixing their extension inputs.
This is the reference's recommendation; source guidance also distinguishes simple
registry-map merges from extension-state conflicts. [Merge guidance][lock]

## Vendor the configurations that need to work offline

`--vendor_dir` selects a directory of maintained external repository contents.
The `vendor` command can select named repositories or analyze target patterns
under the supplied build configuration to identify their external dependencies.
Vendoring also preserves fetched registry files under the vendor directory.
[Vendor modes][vendor], [command implementation][vendor-command]

Prefer a named target/configuration scope over fetching every possible repository
unless complete-graph vendoring is intentional. A changed target set, configuration,
dependency selection, or Bazel version may require refreshing the vendor set.
Local and `configure = True` repository rules are excluded, so machine-provided
SDKs or configuration can still require a separate environment contract.
[Scope and exclusions][vendor], [exclusion tests][vendor-tests]

`VENDOR.bazel` controls two distinct policies using canonical repository identities
obtained from Bazel:

| Directive | Meaning |
| --- | --- |
| `ignore()` | Exclude the repository from vendor mode. |
| `pin()` | Keep using its current vendored contents; subsequent vendor operations do not refresh it until unpinned. |

Pin intentional local modifications rather than silently editing an ordinary
vendored tree. An unpinned repository whose marker is stale can fall back to a
fetch; with fetching disabled, stale/missing content can fail instead. Successful
vendoring of one target configuration does not establish another configuration's
offline coverage. [Vendor markers and policy][vendor], [stale/pinned tests][vendor-tests]

## Include tool and filesystem boundaries

Some Bazel subcommands have tool dependencies outside the user target graph.
`@bazel_tools//tools:tools_for_bazel_subcommands` is the documented aggregate to
include when preparing such commands for offline use; the upstream regression
test exercises `mod tidy` with fetching disabled after vendoring that target.
[Subcommand tools][vendor], [regression test][vendor-tests]

Vendoring rewrites symlinks pointing into Bazel's external repository area through
a generated `bazel-external` link. Absolute symlinks outside that area are not
rewritten and can retain machine-specific dependencies. Windows vendoring of
symlinks requires `--windows_enable_symlinks`. These are coverage boundaries to
verify on the intended machines, not portability guarantees from this page.
[Symlink behavior][vendor]

Continue with [overrides](overrides-and-patches.md) when the dependency's selected
source must change, rather than only its availability on disk.

## Evidence boundary

Verified against Bazel 9.3.1 source and the cited upstream test definitions.
Those tests were inspected, not executed here. No new integration fixture or
platform compatibility result is claimed. See the [module claim ledger](../verification/modules.md).

[lock]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/lockfile.md
[vendor]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/vendor.md
[extension-eval]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/SingleExtensionEvalFunction.java
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/RepositoryOptions.java
[lock-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_lockfile_test.py
[extension]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/extension.md
[vendor-command]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/commands/VendorCommand.java
[vendor-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_vendor_test.py
