---
title: "Use and design module extensions"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["modules/dependencies-and-version-selection.md"]
claim_ids: ["modules.extension-order", "modules.extension-tags", "modules.extension-imports", "modules.extension-identity", "modules.extension-lazy", "modules.extension-dev", "modules.extension-metadata", "modules.extension-reproducibility", "modules.extension-facts", "modules.extension-platform", "modules.extension-isolation"]
last_verified: "2026-11-05"
---

# Use and design module extensions

Use a module extension when dependency setup needs information from participating
modules, language package resolution, SDK selection, or coordinated repository
generation. Use a direct [repository rule](repository-rules.md) when one local
manifest declaration is sufficient. This is a design recommendation; the two
mechanisms share repository creation machinery. [Extension model][extension],
[`use_repo_rule` API][globals]

## Follow the extension's public API

Bazel resolves the module graph before evaluating its extensions. A call to
`use_extension()` obtains a proxy; method calls on it record tags according to
the extension's `tag_class` schemas. They do not invoke the implementation at
that point. The implementation receives `module_ctx`, reads participating modules
and their tags, and calls repository rules. [Extension model][extension],
[proxy implementation][globals]

Keep the steps distinct:

1. Declare the hosting module as a direct dependency.
2. Refer to the documented `.bzl` file and exported extension symbol.
3. Supply the documented tags and the language lockfiles or SDK selections they
   require.
4. Import the generated repositories your module needs through `use_repo()`.

`use_repo()` makes names visible in the current module. With keyword imports,
the key is the local apparent name and the value is the extension's exported
repository name. It does not itself register a toolchain or declare a build
rule target. Follow the hosting ruleset's separate toolchain-registration contract.
[Import implementation][globals]

Generated repository names are part of the extension's public interface. Avoid
predicting a name from an archive basename or from a toolchain version; inspect
the release's extension tags and emitted repositories. Extensions are evaluated
lazily when their results are needed. `bazel mod deps` can force evaluation of all
extensions, and `bazel mod show_repo` inspects repository definitions.
[Extension usage][extension], [module commands][mod]

## Preserve extension identity

The `.bzl` label and exported symbol used by `use_extension()` identify a normal
extension usage. Re-exporting the same extension object from another file gives
that usage a different identity: tags can be collected and evaluated separately.
Keep one documented public entry point for each extension. [Extension identity][extension]

`use_extension(..., dev_dependency = True)` is ignored for non-root modules and
when the root invocation enables `--ignore_dev_dependency`. An extension author
can inspect whether a tag came from development usage with
`module_ctx.is_dev_dependency(tag)`. Do not let a ruleset's own test dependency
silently become a requirement for every consumer. [Usage API][globals],
[context API][context]

`isolate = True` is not an unconditionally available baseline API: the parameter
requires `--experimental_isolated_extension_usages` in 9.3.1. This reference's
default guidance uses ordinary, shared extension identity. [Parameter gate][globals]

## Design deterministic resolution and useful metadata

`module_ctx.modules` lists modules that use the extension in breadth-first order
from the root. Decide and document conflict resolution deliberately; do not
assume that every extension uses Bazel's module-version selection algorithm for
its language packages. The ordering contract supplies input order, not a language
package policy. [Context API][context], [extension model][extension]

Return `module_ctx.extension_metadata()` with the expected root direct repository
imports when the extension can determine them. `root_module_direct_deps` and
`root_module_direct_dev_deps` drive import diagnostics and `bazel mod tidy` fixes.
When either is specified, both must be supplied; their lists must be disjoint.
One may use the special value `"all"`. [Metadata API][context]

Set `reproducible = True` only if identical usages, tags, and watched inputs always
produce identical repository-rule calls and attributes. This promises stable
**repository specifications**, not that the repository rules themselves produce
reproducible contents. Reproducible extension results can be reused through
Bazel's hidden lockfile; public lockfile facts are a separate mechanism.
[Metadata contract][context], [evaluation implementation][extension-eval]

## Track external inputs and persistent facts

Declare `os_dependent` and `arch_dependent` when extension results depend on the
host OS or architecture. Use tracked input APIs such as `module_ctx.getenv()` and
watched file reads for other inputs. A language target's requested platform is
not interchangeable with the host executing extension evaluation.
[Extension parameters][repo-api], [tracked context inputs][external-context]

`extension_metadata(facts = ...)` persists JSON-like, string-keyed facts for future
evaluations through `module_ctx.facts`; this also works for reproducible
extensions. Reserve it for stable facts whose keys determine their values.
Bazel can shallowly merge facts from evaluations, and facts can outlive extension
code changes. [Facts contract][context], [facts tests][lock-tests]

Use `module_extension(facts_version = ...)` to version incompatible fact schemas.
The value must be nonnegative; when the persisted version differs from the current
one, old facts are discarded before evaluation. Do not assume that changing a
`.bzl` digest clears persisted facts by itself. [Schema API][repo-api],
[version mismatch handling][extension-eval], [schema tests][lock-tests]

Continue with [repository mappings](repository-mapping.md) for generated-repository
visibility and [lockfiles](lockfile-and-vendor.md) for persistence boundaries.

## Evidence boundary

Verified against Bazel 9.3.1 source and the cited upstream test definitions.
Those tests were inspected, not executed here. No new integration fixture or
platform compatibility result is claimed. See the [module claim ledger](../verification/modules.md).

[extension]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/extension.md
[globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleExtensionContext.java
[mod]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/mod-command.md
[repo-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/repository/RepositoryModuleApi.java
[external-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/starlark/StarlarkBaseExternalContext.java
[extension-eval]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/SingleExtensionEvalFunction.java
[lock-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_lockfile_test.py
