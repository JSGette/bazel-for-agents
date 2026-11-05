---
title: "Declare modules and understand selected versions"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md"]
claim_ids: ["modules.manifest", "modules.direct-dependency", "modules.mvs", "modules.direct-check", "modules.dev-dependency", "modules.nodep", "modules.registry-order", "modules.bazel-compatibility", "modules.compatibility-noop", "modules.include"]
last_verified: "2026-11-05"
---

# Declare modules and understand selected versions

Use this page when adding a Bazel module or investigating why its selected version
differs from the manifest. Keep three separate identities in review: the Bazel
module version, the language/compiler version it configures, and any dependency
versions resolved by its extensions. Module resolution selects Bazel modules;
[extensions](extensions-and-generated-repositories.md) perform their own work afterward.
[Module resolution][module], [extension evaluation][extension]

## Read the manifest as a dependency declaration

`MODULE.bazel` describes the module and its direct module dependencies. If
`module()` is present, it must precede other directives and occur at most once.
The root module may omit it; a reusable module needs its published identity.
`bazel_dep()` declares a direct dependency. Its `repo_name` can set the apparent
repository name used by that dependent; the module name remains the dependency's
resolution identity. [Manifest API][globals]

Declare the modules whose public targets or `.bzl` APIs your project directly
uses. A dependency's transitive modules do not automatically become visible under
their apparent names in your repository. This direct-dependency boundary helps
keep implementation details out of consumers' build files. [Repository visibility][module]

## Distinguish requested and selected versions

For ordinary registry dependencies without overrides, Minimal Version Selection
selects the highest version of a module present in the discovered dependency
graph, rewrites references to the selection, and removes unreachable modules.
It does not search for the newest release published in a registry. A request for
version `1.2` can therefore resolve to `1.4` if another discovered dependency
requests `1.4`, even when `1.9` is published. This example explains the algorithm;
it is not a recommendation for any real module. [Selection implementation][selection],
[diamond dependency test][module-tests]

Consequently, an exact string in `bazel_dep(version = ...)` is a requested version,
not an unconditional pin. Inspect the selected graph before copying APIs from the
requested release. `bazel mod graph` and `bazel mod explain` expose selection and
dependency paths. `--check_direct_dependencies` defaults to `warning`; `error`
turns a mismatch between a root direct request and the selected version into a
resolution failure. [Inspection commands][mod], [flag definition][options]

When discovery encounters a module in multiple configured registries, registry
order matters: Bazel checks earlier registries first and falls back when the
module is missing. Version selection and registry selection are different
questions. [Registry option][options]

## Scope development and conditional dependencies deliberately

| Mechanism | Meaning at the baseline |
| --- | --- |
| `bazel_dep(..., dev_dependency = True)` | Ignored when this module is a dependency; also ignored in the root with `--ignore_dev_dependency`. |
| `use_extension(..., dev_dependency = True)` | Applies the same root-only development scope to that extension usage. |
| `bazel_dep(..., repo_name = None)` | A *nodep* declaration: honored only if the module enters the graph by another dependency path; it does not create an apparent repository import. |

These are module-system decisions, not a classification of build targets as
production or test targets. Put a reusable ruleset's own test-only dependencies
in development scope; keep dependencies needed by its consumers in ordinary
scope. The latter sentence is this reference's recommendation.
[Directive semantics][globals]

## Declare the actual Bazel compatibility contract

`module(bazel_compatibility = ...)` records constraints on the Bazel version
running the build. It does not select dependency versions. Compatibility checking
defaults to `error` through `--check_bazel_compatibility`.
[Manifest API][globals], [checking option][options]

At Bazel 9.3.1, `module(compatibility_level = ...)` and
`bazel_dep(max_compatibility_level = ...)` are deprecated no-ops. The implementation
sets the module's internal compatibility level to zero and ignores the requested
maximum. Do not use these attributes to promise API compatibility or to control
resolution. Audit selected APIs and use a deliberate [override](overrides-and-patches.md)
only when needed. [Actual parameter implementation][globals]

## Split a large root manifest without hiding ownership

`include()` can divide a root manifest into files ending in `.MODULE.bazel`.
The included label must start with `//`, stay within the module's repository, and
name a file whose name does not start with `.`. Registry modules cannot use
`include()`; root modules and modules supplied by non-registry overrides can.
[Include API][globals], [root/override/registry tests][module-tests]

Included directives contribute to the same manifest, but variable bindings stay
local to each file. An extension proxy variable in one file is not a shared
variable in another. `include` takes a literal label and an optional literal
`dev_dependency` boolean, and is a top-level directive. Prefer splits by coherent
dependency family while retaining a clear root entry point.
[Include semantics][globals], [syntax enforcement][compiled-module]

Continue with [extensions](extensions-and-generated-repositories.md), or use
[repository mappings](repository-mapping.md) when a dependency exists but its
label cannot be resolved.

## Evidence boundary

Verified against Bazel 9.3.1 source and the cited upstream test definitions.
Those tests were inspected, not executed here. No new integration fixture or
platform compatibility result is claimed. See the [module claim ledger](../verification/modules.md).

[module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/module.md
[extension]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/extension.md
[globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[selection]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/Selection.java
[module-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_module_test.py
[mod]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/mod-command.md
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/RepositoryOptions.java
[compiled-module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/CompiledModuleFile.java
