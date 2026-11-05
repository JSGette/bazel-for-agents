# Core labels and phases: claim evidence

Verified on 2026-11-05 against Bazel **9.3.1**, commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`.
The [release-tag reference](https://api.github.com/repos/bazelbuild/bazel/git/ref/tags/9.3.1)
was checked to establish this identity. Primary sources below use the immutable
commit. No claim here extends to every later Bazel version.

Pages: [labels and targets](../core/labels-and-targets.md),
[phases and graphs](../core/phases-and-graphs.md).

## Source-verified claims

These are definitional claims. They have no required runtime platform or ruleset,
and no claim of comprehensive execution coverage. The relevant source section is
listed for each independently checkable statement.

| Claim ID | Statement | Exact source and relevant section |
| --- | --- | --- |
| `core.repository` | A repository is a marked directory tree; the invocation's repository is the main repository. | [Repositories][repositories], “Repositories”. |
| `core.module` | A module is a versioned Bazel project with dependencies on other modules. | [Modules][module], introductory definition. |
| `core.module-manifest` | A module uses `MODULE.bazel` at its root for metadata and direct dependencies. | [Modules][module], introductory definition. |
| `core.package` | A build-file directory defines a package excluding nested packages. | [Repositories][repositories], “Packages”. |
| `core.build-file` | Build files define package targets; `BUILD.bazel` takes precedence over `BUILD`. | [Build files][build-files], introduction. |
| `core.extension` | `.bzl` extensions export symbols imported with `load()`. | [Build files][build-files], “Loading an extension”. |
| `core.target` | Common target kinds are files and instantiated rules. | [Repositories][repositories], “Targets”; [Rules][rules], “Target instantiation”. |
| `core.label-parts` | Labels identify targets using repository/package/name components and documented abbreviations. | [Labels][labels], syntax and abbreviation examples. |
| `core.label-context` | Repository-relative labels refer to the repository in which they are interpreted. | [Labels][labels], current-repository versus main-repository explanation. |
| `core.repository-mapping` | Apparent repository names resolve through a repository-specific mapping to canonical names. | [External dependencies][external], canonical/apparent repository name definitions. |
| `core.generated-artifact` | A `File` is a source or generated artifact; outputs declared during analysis have no labels. | [Rules][rules], “Files” and “Declaring outputs”. |
| `core.loading` | Loading evaluates required build/extension files and instantiates targets. | [Evaluation model][phases], loading phase. |
| `core.analysis` | Rule implementation runs during analysis, returns providers, and registers actions. | [Rules][rules], “Implementation function”. |
| `core.execution` | Execution produces needed outputs and runs tests; unused actions need not run. | [Evaluation model][phases], execution and demand-driven work. |
| `core.configured-target` | One target label can have multiple configured instances in a build graph. | [cquery][cquery], “Target pattern evaluation”. |
| `core.query` | `query` uses the post-loading graph and does not resolve configuration-dependent branches. | [Query reference][query], “Additional query reference”. |
| `core.cquery` | `cquery` inspects configured analysis results. | [cquery][cquery], introduction and “Configurations”. |
| `core.aquery` | `aquery` exposes post-analysis actions, artifacts, and their relationships. | [aquery][aquery], introduction. |
| `core.cache-reuse` | Existing outputs or remote cache hits can avoid executing a required action. | [Remote caching][cache], “How a build uses remote caching”. |

## Runtime coverage

The [foundation record](foundations.md) owns the exact platform, flags, rc loading,
commands, expected/observed outputs, and limitations for the shared fixture.
That fixture covers local target lookup, analysis, provider exchange, output
selection, action inspection, and generated contents. It does not test all label
forms, nested package boundaries, repository mappings, configuration transitions,
conditional dependency selection, or remote caching. Definitions for those cases
remain source-verified.

Editorial instructions such as preferring explicit labels and starting diagnosis
at the relevant phase are this repository's recommendations, not claimed Bazel
requirements. The diagram describes a conceptual dependency between phases;
it does not assert a global scheduling barrier or cache invalidation policy.

[repositories]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-ref.md
[module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/module.md
[build-files]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-files.md
[labels]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/labels.md
[external]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/overview.md
[rules]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md
[phases]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/concepts.md
[query]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/language.md
[cquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/cquery.md
[aquery]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/query/aquery.md
[cache]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/remote/caching.md
