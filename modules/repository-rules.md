---
title: "Fetch repositories with tracked inputs"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["modules/extensions-and-generated-repositories.md"]
claim_ids: ["modules.repo-definition", "modules.repo-direct", "modules.repo-inputs", "modules.repo-download", "modules.repo-watch", "modules.repo-environment", "modules.repo-process", "modules.repo-names", "modules.repo-metadata", "modules.repo-return"]
last_verified: "2026-11-05"
---

# Fetch repositories with tracked inputs

Use this page when creating an external source tree, exposing a pinned tool
archive, or reviewing an extension's repository rules. Prefer a maintained
repository rule with a suitable contract before introducing a custom one.
Repository fetching and build actions have different APIs and input tracking;
do not put ordinary generated build outputs in repository setup.
[Repository-rule API][repo-api], [repository context][repo-context]

## Define the repository boundary

A `repository_rule()` definition has an implementation and an attribute schema.
Its implementation receives `repository_ctx`; it creates or exposes the external
repository's files. The implicit `name` attribute must not be redeclared.
Label attributes used by repository rules must refer to source files, not
generated build artifacts. [Definition API][repo-api]

An extension can call the exported repository rule. A `MODULE.bazel` file can
instead obtain a callable proxy with `use_repo_rule()`. That proxy defines
repositories visible to the current module and supplies a `dev_dependency`
attribute for root-only development scope. A non-module data or tool archive does
not need to be misrepresented as a versioned Bazel module.
[Direct invocation API][globals]

## Make refetch inputs intentional

| Input or operation | Contract to account for |
| --- | --- |
| Rule attributes and implementation | Participate in the repository definition and refetch decision. |
| `repository_ctx.getenv(name)` | Records the named environment variable; a changed value invalidates the repository. |
| File reads with watching | Track the watched input for invalidation. |
| `watch(path)` | Tracks existence, type, and file contents; watching a directory does not recursively watch its children. |
| `watch_tree(path)` | Tracks files/directories recursively under an external input directory. |
| Network data or arbitrary subprocess observations | Must be controlled or explicitly accounted for; Bazel does not infer reproducibility from a successful fetch. |

[Fetch implementation][repo-fetch], [base context API][external-context],
[recursive watching API][repo-context]

Prefer `getenv()` over the deprecated `repository_rule(environ = ...)` parameter.
Do not use an ambient environment lookup as an unrecorded configuration channel.
`--repo_env` can supply repository environment values, but it is not an action
environment declaration. [Definition API][repo-api], [tracked getenv][external-context], [repository environment][repo-guide]

Watch methods also have scope restrictions. A repository cannot watch paths
inside the repository currently being created. `read()`'s `watch` setting and
related APIs distinguish `"yes"`, `"no"`, and `"auto"`; check the method's contract
when reading files that should trigger refetching. `watch_tree()` requires a
directory. [Watching APIs][external-context], [tree API][repo-context]

## Pin downloads and inspect subprocess results

`download()` and `download_and_extract()` accept `sha256` or `integrity` to verify
the expected bytes. Their API documents omission as a security and reproducibility
risk. Our recommendation is to require a checked-in digest for release artifacts
and use stable, reviewable source identities; a URL alone is insufficient evidence
that the bytes will stay the same. [Download API][external-context]

`repository_ctx.execute()` runs a command and returns an `exec_result` containing
its result. Its `environment` map overrides selected variables and can remove a
variable with `None`; it is not a declaration of build-action inputs. Inspect
return codes and stderr before generating files from the result. Pin the program
and all inputs that determine output when claiming reproducibility.
[Execution API and implementation][external-context]

## Use names according to their contract

`repository_ctx.name` is the canonical repository name. Its format is not a stable
API. `repository_ctx.original_name` exposes the name supplied when instantiating
the rule; use it when that original name is required rather than parsing canonical
names. Repository mapping handles labels across repository boundaries.
[Name APIs][repo-context], [mapping guidance](repository-mapping.md)

## Return honest reproducibility metadata

Prefer explicit `repository_ctx.repo_metadata(...)` from a custom implementation.
`reproducible = True` promises identical contents for identical attributes,
implementation, watched files, environment values, and other tracked inputs even
when untracked conditions change. It enables eligibility for repository-contents
caching across projects; it does not guarantee a cache hit, and local repository
rules are not cached that way. [Metadata contract][repo-context],
[cache eligibility][repo-fetch]

When reproducibility is false, `attrs_for_reproducibility` can describe attribute
changes needed to make the same result reproducible. It cannot accompany
`reproducible = True`. [Metadata construction][repo-context]

Do not treat returning `None` as proof of reproducibility. In Bazel 9.3.1,
`RepositoryFetchFunction` classifies that default return as nonreproducible.
Explicit metadata is the source of the reproducibility declaration. This resolves
a contradiction in the repository-rule guide against the actual implementation.
[Return-value handling][repo-fetch]

Continue with [overrides and patches](overrides-and-patches.md) for a targeted
upstream modification, or [vendoring](lockfile-and-vendor.md) for a maintained
local copy of selected external repositories.

## Evidence boundary

Verified against Bazel 9.3.1 source and the cited upstream test definitions.
Those tests were inspected, not executed here. No new integration fixture or
platform compatibility result is claimed. See the [module claim ledger](../verification/modules.md).

[repo-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/repository/RepositoryModuleApi.java
[repo-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/starlark/StarlarkRepositoryContext.java
[globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[repo-fetch]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/RepositoryFetchFunction.java
[external-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/starlark/StarlarkBaseExternalContext.java

[repo-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/repo.md
