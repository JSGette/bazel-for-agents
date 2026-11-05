# Module and package claim evidence

Verified on 2026-11-05 against Bazel **9.3.1**, immutable commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`.

All claims below are **source-verified**. Platform/ruleset coverage is empty;
no extra flags are required for the ordinary guidance. A flag-gated API is
explicitly identified rather than included in the default path. The upstream
integration tests were inspected as source, not run in this repository.
Claim-level executable fixtures and remote CI remain follow-up work in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

Pages: [dependencies](../modules/dependencies-and-version-selection.md),
[extensions](../modules/extensions-and-generated-repositories.md),
[repository rules](../modules/repository-rules.md),
[mappings](../modules/repository-mapping.md),
[lockfiles and vendoring](../modules/lockfile-and-vendor.md),
[overrides](../modules/overrides-and-patches.md).

## Evidence method and corrections

Read the pinned module/extension/lockfile/vendor guides, the manifest and
repository APIs, selection/mapping/fetch implementations, and the relevant
upstream integration-test assertions. When documentation and implementation
differ, use the implementation for baseline guidance:

- `compatibility_level` and `max_compatibility_level` are no-ops in
  `ModuleFileGlobals`, even though selection comments and some parameter prose
  still discuss compatibility levels.
- The repository guide says a `None` return signifies reproducibility;
  `RepositoryFetchFunction` actually classifies the default return as
  `NONREPRODUCIBLE`. Prefer explicit `repo_metadata`.
- Reproducible extension **results** and persistent **facts** have different
  public-lockfile behavior. `testFactsInReproducibleExtension` and
  `testFactsVersionDiscardedOnMismatch` cover this distinction and schema changes.
- The pinned repository guide mentions an `execute(..., watch=...)` parameter;
  the actual `execute` signature has no such parameter. The page uses the actual
  method API and does not imply automatic subprocess-input watching.

No upstream examples with unrelated old release versions were copied. Editorial
recommendations about dependency ownership, explicit metadata, digest pinning,
and review order are recommendations, not claimed Bazel requirements or measured
performance benefits.

## Dependencies and selection

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.manifest` | A module manifest declares module identity and direct dependencies; module() is at most once and first when present. | [Source][globals]: module(). |
| `modules.direct-dependency` | bazel_dep declares a direct module dependency and can rename its apparent repository import; transitive imports are not automatically visible. | [Source][globals]: bazelDep(); module guide: Repository names and strict deps. |
| `modules.mvs` | Ordinary selection chooses the maximum discovered module version, rewrites edges, and prunes unreachable modules rather than choosing the registry latest. | [Source][selection]: run(), selection groups; [Module tests][module-tests]: testSimpleDiamond. |
| `modules.direct-check` | check_direct_dependencies compares root direct requested versions against selections and defaults to warning; error makes mismatch fatal. | [Source][options]: checkDirectDependencies option. |
| `modules.dev-dependency` | Development module/extension dependencies are ignored outside the root and when ignore_dev_dependency applies. | [Source][globals]: bazelDep(), useExtension(). |
| `modules.nodep` | repo_name=None makes a conditional nodep request without an apparent import; another path must introduce the module. | [Source][globals]: bazelDep() repoName Optional handling. |
| `modules.registry-order` | Configured registries are searched in order with fallback on missing modules. | [Source][options]: registries option. |
| `modules.bazel-compatibility` | bazel_compatibility constrains the running Bazel version, not dependency selection; checking defaults to error. | [Source][globals]: module() bazel_compatibility; [Options][options]: bazelCompatibilityMode. |
| `modules.compatibility-noop` | compatibility_level and max_compatibility_level are deprecated no-ops; parsed modules receive level zero. | [Source][globals]: module() setCompatibilityLevel(0); bazelDep() DepSpec(...,-1). |
| `modules.include` | Root/non-registry manifests can include same-repository .MODULE.bazel files; bindings remain file-local and labels/dev flags must be literals. | [Source][globals]: include(); [Module syntax][compiled-module]: IncludeSyntaxChecker; [Module tests][module-tests]: testInclude, testRegistryModuleInclude. |

## Extensions

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.extension-order` | Module graph resolution precedes extension evaluation; extension implementations can resolve non-Bazel ecosystems and create repositories. | [Source][extension]: introduction and Extension definition. |
| `modules.extension-tags` | use_extension returns a tag proxy, while tag_class defines tag schemas and module_ctx.modules exposes participating modules in BFS order. | [Source][globals]: useExtension()/ModuleExtensionProxy; [Extension context][context]: getModules(); [Repository API][repo-api]: tagClass(). |
| `modules.extension-imports` | use_repo imports generated repositories; keyword keys are local names and values are exported names. It adds imports rather than registering toolchains. | [Source][globals]: useRepo(). |
| `modules.extension-identity` | The .bzl label and exported extension name identify ordinary shared usage; re-exporting under another file separates identity. | [Source][extension]: Extension identity. |
| `modules.extension-lazy` | Extension evaluation is lazy; mod deps forces evaluation and mod show_repo displays definitions. | [Source][extension]: Extension usage; [Module commands][mod]: command descriptions. |
| `modules.extension-dev` | Extension usage has root-only development scope, and is_dev_dependency exposes a tag's development status. | [Source][context]: isDevDependency(); globals: useExtension(). |
| `modules.extension-metadata` | Direct/development repository metadata drives tidy checks; both lists must be supplied together, disjoint, with at most one all value. | [Source][context]: extensionMetadata(). |
| `modules.extension-reproducibility` | Reproducible extension metadata promises stable repository specifications, not stable fetched contents; hidden state can cache evaluation. | [Source][context]: extensionMetadata() reproducible; [Extension evaluation][extension-eval]: reproducible result handling. |
| `modules.extension-facts` | Facts persist across evaluations/code changes, support reproducible extensions, may be shallowly merged, and are discarded on facts_version mismatch. | [Source][context]: facts/extensionMetadata(); [Repository API][repo-api]: facts_version; [Lockfile tests][lock-tests]: testFactsInReproducibleExtension, testFactsVersionDiscardedOnMismatch. |
| `modules.extension-platform` | os_dependent/arch_dependent identify host-dependent extension evaluation, and getenv/watched reads track other inputs. | [Source][repo-api]: moduleExtension(); [External context][external-context]: getenv/read/watch. |
| `modules.extension-isolation` | use_extension(isolate=True) is gated by experimental_isolated_extension_usages. | [Source][globals]: useExtension() parameter annotation. |

## Repository rules

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.repo-definition` | repository_rule has an attribute schema, an implicit name, and a repository_ctx implementation; its labels cannot depend on generated artifacts. | [Source][repo-api]: repositoryRule(). |
| `modules.repo-direct` | use_repo_rule creates a module-local repository-rule proxy with an implicit dev_dependency attribute. | [Source][globals]: useRepoRule(), RepoRuleProxy.call(). |
| `modules.repo-inputs` | Repository refetching tracks definitions and recorded inputs rather than inferring every external observation. | [Source][repo-fetch]: compute(), fetchRepo(), recordedInputValues. |
| `modules.repo-download` | Download APIs accept sha256/integrity verification; omission does not establish reproducible artifact identity. | [Source][external-context]: download(), downloadAndExtract(). |
| `modules.repo-watch` | watch tracks existence/type/file contents but not directory descendants; watch_tree is recursive and requires an eligible directory outside the output repository. | [Source][external-context]: watchForStarlark(), readFile(); [Repository context][repo-context]: watchTree(). |
| `modules.repo-environment` | getenv records environment inputs; repository_rule.environ is deprecated. repo_env supplies repository environment configuration. | [Source][repo-api]: repositoryRule() environ; [External context][external-context]: getEnvironmentValue(); [Repository guide][repo-guide]: refetch inputs. |
| `modules.repo-process` | execute returns command results and allows per-variable environment overrides/removal; it is a repository operation rather than a declared build action. | [Source][external-context]: execute(). |
| `modules.repo-names` | repository_ctx.name is canonical; original_name exposes the original requested name when supplied. | [Source][repo-context]: getName(), getOriginalName(). |
| `modules.repo-metadata` | repo_metadata declares reproducibility and optional corrective attributes; True is cache eligibility, excludes local repositories, and cannot include corrective attributes. | [Source][repo-context]: repoMetadata(); [Repository fetch][repo-fetch]: reproducibility/cache handling. |
| `modules.repo-return` | The default/None repository-rule result is classified NONREPRODUCIBLE in 9.3.1. | [Source][repo-fetch]: fetchRepo() return-value switch. |

## Repository mapping

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.mapping-context` | Apparent names resolve using the referencing repository's mapping, while canonical names identify repositories within a build. | [Source][overview]: Canonical and apparent repo names; mapping: computeInternal(). |
| `modules.mapping-direct` | Module repository mappings include direct imports, not arbitrary transitive module names. | [Source][mapping]: computeForBazelModuleRepo(); [Module guide][module]: strict deps. |
| `modules.mapping-renames` | bazel_dep.repo_name renames an import; use_repo and override_repo/inject_repo keyword maps use different alias directions. | [Source][globals]: bazelDep(), useRepo(), overrideRepo(), injectRepo(). |
| `modules.mapping-generated` | Generated repositories see the hosting module's imports and extension siblings; Label construction can resolve conflicts in the extension context. | [Source][extension]: Repository names and visibility. |
| `modules.mapping-canonical` | Canonical naming syntax is not a supported API; Label.repo_name retrieves the canonical name from a resolved Label. | [Source][module]: Repository names and strict deps. |
| `modules.mapping-inspection` | mod dump_repo_mapping exposes mappings and mod show_repo shows repository definitions. | [Source][mod-command]: dumpRepoMappings(), SHOW_REPO command handling. |
| `modules.mapping-runfiles` | The module guide directs runtime lookup through rlocationpath/runfiles libraries rather than constructed canonical directories. | [Source][module]: Repository names and strict deps: runfiles guidance. |

## Lockfiles and vendoring

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.lock-content` | The public lockfile records registry hashes and extension inputs/specifications, not repository source trees or action results. | [Source][lock]: Lockfile Contents; [Extension evaluation][extension-eval]: evaluation state. |
| `modules.lock-modes` | lockfile_mode supports update(default), refresh, error, and off; error does not ban all extension or fetch network access. | [Source][options]: lockfileMode; [Lockfile guide][lock]: Lockfile Usage. |
| `modules.lock-lazy` | Lock state reflects evaluated extensions and can have OS/architecture-specific entries; mod deps forces all extension evaluation. | [Source][lock]: Module Extensions; [Extension guide][extension]: Extension usage. |
| `modules.lock-hidden` | An unspecified hidden output-base lockfile caches extension state, including reproducible evaluations. | [Source][lock]: Hidden lockfile; [Extension evaluation][extension-eval]: reproducible result persistence. |
| `modules.lock-reproducible-facts` | Reproducible extension result omission does not omit persistent public facts. | [Source][lock-tests]: testFactsInReproducibleExtension. |
| `modules.vendor-scope` | vendor_dir stores selected external repositories/registry files; vendor target scope depends on the analysis configuration. | [Source][vendor]: Vendor external dependencies for given targets; Vendor registry files. |
| `modules.vendor-exclusions` | Local and configure repositories are excluded from vendoring. | [Source][vendor-tests]: testIgnoreFromVendoring. |
| `modules.vendor-pin` | VENDOR.bazel ignore excludes a repository; pin keeps its current vendored content until unpinned. | [Source][vendor]: Configure vendor mode; [Vendor tests][vendor-tests]: testBuildingWithPinnedRepo. |
| `modules.vendor-stale` | Stale unpinned vendored repositories can refetch, while nofetch can make missing/stale content fail. | [Source][vendor-tests]: testBuildingOutOfDateVendoredRepo, testBuildingVendoredRepoWithNoFetch. |
| `modules.vendor-subcommands` | The tools_for_bazel_subcommands target includes subcommand tools outside the ordinary user target graph, tested upstream for mod tidy offline. | [Source][vendor-tests]: testVendorToolsForBazelSubcommands. |
| `modules.vendor-symlinks` | Vendoring rewrites symlinks into the external area, not arbitrary outside absolute links; Windows symlink vendoring requires windows_enable_symlinks. | [Source][vendor]: Vendor symlinks. |

## Overrides

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `modules.override-root` | Only root module overrides take effect and may affect transitive dependencies; override is not an apparent-name import. | [Source][module]: Overrides; Repository names and strict deps. |
| `modules.override-single` | Single-version overrides independently support version, registry, and patches. | [Source][globals]: singleVersionOverride(). |
| `modules.override-multiple` | Allowed multiple versions must occur before selection; requests select a higher-or-equal allowed version or fail if still unsatisfied. | [Source][selection]: computeAllowedVersionSets(), computeSelectionGroup(), graph validation. |
| `modules.override-nonregistry` | Archive/Git/local overrides obtain a module from replacement source outside normal registry version selection. | [Source][globals]: archiveOverride(), gitOverride(), localPathOverride(); [Module guide][module]: Non-registry overrides. |
| `modules.override-patches` | Root patch labels apply in list order; root-provided patches can affect MODULE.bazel processing. | [Source][globals]: singleVersionOverride(), convertAndValidatePatchLabel(); [Override tests][overrides-tests]: testSingleVersionOverrideWithPatch. |
| `modules.override-patch-commands` | Single-version patch_cmds are Bash on Linux/macOS after patches and cannot affect module resolution through manifest edits. | [Source][globals]: singleVersionOverride() patch_cmds. |
| `modules.override-generated` | override_repo replaces an existing extension repository with one visible to root; it is ignored outside root and with ignore_dev_dependency. | [Source][globals]: overrideRepo(). |
| `modules.inject-generated` | inject_repo adds a new extension-side repository binding from root; it has the same root/development scope. | [Source][globals]: injectRepo(). |

## Package files and defaults

Additional page: [files and packages](../core/files-and-packages.md).

| Claim ID | Bounded statement | Primary source and inspected symbol |
| --- | --- | --- |
| `core.build-evaluation` | BUILD statements evaluate in order and declare rule targets; target dependencies can refer to later declarations. | [BUILD files][build-files], sequential evaluation and rule declaration order. |
| `core.glob-package` | glob returns sorted mutable package-relative paths and excludes subpackages; directories are excluded by default. | [Native API][native-api], glob; [function reference][functions], glob limitations. |
| `core.glob-patterns` | Star matches within segments, double star spans complete segments, and a new package boundary changes recursive matching. | [Function reference][functions], glob syntax and package limitations. |
| `core.glob-generated` | glob observes sources during package evaluation, not generated artifacts. | [Function reference][functions], glob limitations. |
| `core.glob-empty-default` | At baseline defaults, allow_empty is False; each include and the final excluded result must be nonempty. | [Flag default][language-options], DISALLOW_EMPTY_GLOB_DEFAULT; [implementation][native-impl], glob(); [API][native-api], allow_empty. |
| `core.glob-labels` | Glob strings used as label attributes can resolve to a same-named rule rather than the source file. | [Function reference][functions], glob shadowing caveat. |
| `core.filegroup` | filegroup forwards selected dependency artifacts under one label, optionally from an output group, rather than arbitrary semantic providers. | [Rule][filegroup-rule], srcs/output_group; [implementation][filegroup-impl], create(). |
| `core.exports-files` | exports_files declares source targets; omitted visibility is public independently of package default visibility. | [API][native-api], exportsFiles; [tests][exports-tests], registered source targets. |
| `core.package-defaults` | package() is at most once and supports package defaults; features merge and visibility has top-level/macro boundaries. | [Callable][package-call], packageCallable(); [arguments][package-args], mergeWith/processParam; [reference][functions], default_visibility. |
| `core.repo-defaults` | REPO.bazel is a boundary/metadata file with repo() package-style parameters and no load support. | [Overview][overview], REPO.bazel; [implementation][repo-file], readAndParseRepoFile/evalRepoFile. |

The function-reference template's displayed glob signature says
`allow_empty=True`, but the pinned implementation uses
`DISALLOW_EMPTY_GLOB_DEFAULT = "true"`, making the actual default **False**.
The page follows the implementation. It does not assume
`incompatible_no_implicit_file_export` defaults true: that flag is false at this
baseline, so explicit exports are presented as authoring guidance rather than a
claim that implicit export is disabled.

## Limits

These pages establish API/source semantics at the exact baseline. They do not
prove a particular ruleset graph resolves, a custom extension is reproducible,
a machine is offline-capable, or an override is API-compatible. There are no
new execution results, expected command outputs, or cross-platform integration
claims in this ledger. Existing foundational fixtures retain their own records.

[module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/module.md
[globals]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java
[selection]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/Selection.java
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/RepositoryOptions.java
[module-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_module_test.py
[extension]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/extension.md
[context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleExtensionContext.java
[repo-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/repository/RepositoryModuleApi.java
[repo-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/starlark/StarlarkRepositoryContext.java
[external-context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/starlark/StarlarkBaseExternalContext.java
[repo-fetch]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/repository/RepositoryFetchFunction.java
[lock]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/lockfile.md
[lock-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_lockfile_test.py
[extension-eval]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/SingleExtensionEvalFunction.java
[vendor]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/vendor.md
[vendor-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_vendor_test.py
[vendor-command]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/commands/VendorCommand.java
[overview]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/overview.md
[mapping]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/RepositoryMappingFunction.java
[mapping-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_repo_mapping_test.py
[mod]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/mod-command.md
[mod-command]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/commands/ModCommand.java
[overrides-tests]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/py/bazel/bzlmod/bazel_overrides_test.py
[compiled-module]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/CompiledModuleFile.java

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

[repo-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/repo.md
