---
title: "Locate a target and its defining package"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: []
claim_ids: [core.repository, core.module, core.module-manifest, core.package, core.build-file, core.extension, core.target, core.label-parts, core.label-context, core.repository-mapping, core.generated-artifact]
last_verified: "2026-11-05"
---

# Locate a target and its defining package

Use this page when finding a build target, adding a dependency label, or deciding
which file to edit. Recommendations below use `BUILD.bazel` consistently; Bazel
also accepts `BUILD`. If both exist, `BUILD.bazel` wins. [Build files][build-files]

## Identify the boundary and file

A **repository** is a source directory tree with a boundary marker. The repository
containing the current Bazel invocation is the **main repository**.
[Repositories][repositories]

A **module** is a versioned Bazel project with dependencies on other modules.
Its `MODULE.bazel` is both its manifest and a repository boundary marker; it
describes module metadata and direct module dependencies. [Module definition][module],
[repository markers][repositories]

| File | Read or edit it for |
| --- | --- |
| `MODULE.bazel` | Module metadata and dependencies. [Source][module] |
| `BUILD.bazel` | A package's targets and their attributes. [Source][build-files] |
| `.bzl` | Reusable rules, functions, and constants imported with `load()`. [Source][build-files] |

A **package** begins at a directory containing a build file. It includes that
directory's descendants up to, but excluding, any nested package. Adding a build
file in a subdirectory therefore creates a new package boundary. Identify the
owning package before forming a file label. [Package definition][repositories]

## Identify the target

A **target** is a named build entity in a package. Common kinds are rule targets
and file targets. Calling a rule in a build file creates a rule target; its
attributes can refer to source files or other targets. [Targets][repositories],
[rule instantiation][rules]

A **label** identifies a target. Its components are repository, package, and
target name. For labels written in a build file: [Label syntax][labels]

| Form | Meaning |
| --- | --- |
| `:target` | Target in this package. |
| `//path/to/package:target` | Target in that package of the current repository. |
| `//:target` | Target in the current repository's root package. |
| `@repo//path/to/package:target` | Target through an apparent repository name. |
| `@@repo//path/to/package:target` | Target through a canonical repository name. |

`//` does not universally mean the main repository: inside another repository,
it refers to that repository. An apparent repository name is interpreted through
the referencing repository's mapping; a canonical name identifies the repository
unambiguously within the build. Our recommendation is to use the documented
apparent names and avoid constructing generated canonical names.
[Label context][labels], [repository mappings][external]

When a label omits `:target`, Bazel uses the package path's final component as the
target name. That abbreviation does not mean “all targets in this package.” Prefer
explicit `:target` spelling when clarity matters. [Label abbreviations][labels]

## Keep files and labels distinct

In analysis, a `File` represents either a source artifact or a generated artifact.
Outputs created by `ctx.actions.declare_file()` during analysis have no labels;
their producing target exposes them through providers. Do not infer an output
label from a file's name. [Files and declaring outputs][rules]

In the [foundation fixture](../examples/foundations/BUILD.bazel), `//:greeting`
is a rule target and `//:message.tpl` identifies its source template. The
[rule implementation](../examples/foundations/defs.bzl) declares `greeting.txt`
as an output artifact. A consumer depends on `//:greeting` and obtains the output
through `GreetingInfo`; it does not address that artifact as a separate target.

## Verify and continue

The [foundation verification record](../verification/foundations.md) contains the
exact environment, dependency query, configured output query, and observed results.
The [claim record](../verification/core-labels-phases.md) distinguishes source
definitions from the fixture's narrower execution coverage. Repository-mapping
and nested-package behavior are source-verified here, not separate runtime tests.

Next read [phases and graphs](phases-and-graphs.md) to distinguish a target's
declaration from its configured analysis and producing actions.

[repositories]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-ref.md
[module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/module.md
[build-files]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-files.md
[labels]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/labels.md
[external]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/overview.md
[rules]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md
