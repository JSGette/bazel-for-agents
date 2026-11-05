# Go, Gazelle, and Python source evidence

Reviewed on 2026-11-05. All records below are **source-verified** against exact
release source. Bazel editorial baseline: **9.3.1**. `platforms: []`, `flags: []`,
`fixture: null`, `commands: []`, `expected: null`, `observed: null` apply to each
claim: no ruleset integration, compiler installation, or application was run.
The source archives were downloaded and their SHA-256 integrity values matched
the immutable registry source records. Source inspection is not graph resolution.

## Source identities

| Module | Release | Upstream commit | BCR source record |
| --- | --- | --- | --- |
| `rules_go` | `0.65.0` | `fb591bc876354b939ef767887e772c15f679a283` | [Archive and patches](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_go/0.65.0/source.json) |
| `gazelle` | `0.54.0` | `ed9d0f2d159457270694ce66803ef471b5ac3be3` | [Archive and patches](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/gazelle/0.54.0/source.json) |
| `rules_python` | `2.4.6` | `943362ffab1a2e8488f50b8554256f9330d3837e` | [Archive and patches](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_python/2.4.6/source.json) |

The registry applies a module-version patch to each archive. The manifest edges
are recorded below as declared requirements, not recommendations to select those
versions and not a resolved transitive graph. The registry manifests and source
patches must accompany a future integration result.

- `rules_go` non-development direct requirements: `bazel_features 1.36.0`, `bazel_skylib 1.8.1`, `platforms 1.1.0`, `rules_proto 7.0.2`, `protobuf 29.0`, `rules_shell 0.3.0`, `rules_cc 0.1.5`, `package_metadata 0.0.5`, `gazelle 0.51.3`.
  [Registry manifest](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_go/0.65.0/MODULE.bazel).
- `gazelle` non-development direct requirements: `bazel_features 1.9.1`, `bazel_skylib 1.5.0`, `platforms 1.1.0`, `protobuf 3.19.6`, `rules_cc 0.0.17`, `rules_go 0.59.0`, `rules_license 1.0.0`, `package_metadata 0.0.5`, `rules_shell 0.2.0`.
  [Registry manifest](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/gazelle/0.54.0/MODULE.bazel).
- `rules_python` non-development direct requirements: `bazel_features 1.21.0`, `bazel_skylib 1.8.2`, `package_metadata 0.0.7`, `platforms 0.0.11`, `rules_cc 0.2.17`, `toml.bzl 0.4.1`, `protobuf 29.0-rc2`.
  [Registry manifest](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_python/2.4.6/MODULE.bazel).

<a id="go-setup"></a>

## Choose a Go SDK and rule entry points

Page: [rulesets/go/setup.md](../rulesets/go/setup.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `go.setup.modules` | The module identities are rules_go and gazelle; their source APIs export the rule and extension entry points listed here. | [Go exports](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/def.bzl); [Gazelle extension](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/extensions.bzl) |
| `go.setup.sdk` | go_sdk provides download, from_file, host and nogo tags; from_file reads one Go manifest and gives its toolchain directive precedence over its go directive. | [SDK extension](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl); [Version parser](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/go_mod.bzl) |
| `go.setup.registration` | rules_go registers the generated go_toolchains repository; SDK declarations are processed in module order and root declarations receive earlier priority. | [Module](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/MODULE.bazel); [Extension implementation](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl) |
| `go.setup.nogo` | Only the root module nogo tag is honored; include/exclude scopes select checked packages. | [nogo handling](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl) |

<a id="go-targets"></a>

## Model Go packages, binaries, tests, and runtime data

Page: [rulesets/go/targets.md](../rulesets/go/targets.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `go.targets.package` | go_library declares package sources, direct GoInfo dependencies and an importpath; embed compiles compatible sources into the same package. | [Library attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl) |
| `go.targets.files` | embedsrcs supplies compile-time Go embed files; data supplies runtime files. | [File attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl) |
| `go.targets.tests` | go_test compiles test sources and supports embedding a package; rundir changes test working-directory behavior with runfiles-related limits. | [Test rule](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/test.bzl) |
| `go.targets.runfiles` | The Go runfiles library supports logical-path lookup, repository mapping and environment propagation to subprocesses. | [Runfiles implementation](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/runfiles/runfiles.go) |

<a id="go-dependencies"></a>

## Resolve Go dependencies through go_deps

Page: [rulesets/go/dependencies.md](../rulesets/go/dependencies.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `go.dependencies.manifests` | go_deps.from_file accepts exactly one go_mod or go_work; each module may have at most one from_file tag. | [Manifest validation](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl) |
| `go.dependencies.selection` | go_deps merges participating module requirements, selects versions, and exposes direct-dependency metadata for use_repo repair. | [Resolution and extension metadata](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl) |
| `go.dependencies.overrides` | Gazelle, module and archive overrides control different parts of Go repository construction. | [Override tags and application](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl) |
| `go.dependencies.environment` | go_deps.config go_env and go_env_inherit affect fetching and the developer Go tool, not Go compilation actions. | [Config attrs](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/bzlmod/go_deps.bzl); [Environment boundary](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/docs/go/core/bzlmod.md) |

<a id="go-cgo"></a>

## Configure cgo, native dependencies, and cross compilation

Page: [rulesets/go/cgo.md](../rulesets/go/cgo.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `go.cgo.attributes` | cgo marks source capability; cdeps and C/C++ option attributes describe native dependencies and compilation. | [cgo attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl) |
| `go.cgo.mode` | Effective pure mode and C++ toolchain availability control cgo; pure=off fails when a required C++ toolchain is unavailable. | [go_context](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/context.bzl) |
| `go.cgo.platform` | goos/goarch attributes transition to rules_go platform labels; go_cross_binary can transition platform and SDK selection. | [Transitions](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/transition.bzl); [Cross wrapper](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/cross.bzl) |
| `go.cgo.instrumentation` | Race and memory-sanitizer instrumentation are rejected in pure mode; static and linkmode control different concerns. | [Mode validation](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/mode.bzl); [Static handling](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/context.bzl) |

<a id="gazelle-generation"></a>

## Generate and review BUILD declarations with Gazelle

Page: [rulesets/gazelle/generation.md](../rulesets/gazelle/generation.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `gazelle.generation.entry` | gazelle and gazelle_binary are exported from def.bzl; default language plugins include Go, proto and visibility. | [Public generator API](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/def.bzl) |
| `gazelle.generation.modes` | The generator exposes update/fix commands and fix/print/diff output modes; diff does not write files. | [Command reference](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md); [Runner attributes](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/def.bzl) |
| `gazelle.generation.index` | Recursion and indexing are separately configurable; lazy indexing needs language-specific search information in nonstandard layouts. | [Lazy indexing](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/README.md); [Index and recursion flags](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md) |

<a id="gazelle-directives"></a>

## Control Gazelle without fighting generated files

Page: [rulesets/gazelle/directives.md](../rulesets/gazelle/directives.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `gazelle.directives.scope` | Gazelle reads top-level BUILD comment directives and generally inherits them into descendants; directive-specific exceptions apply. | [Directive reference](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md) |
| `gazelle.directives.resolution` | prefix, resolve and resolve_regexp configure import identity or explicit import-to-label mappings. | [Resolution directives](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md); [Go prefix](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/language/go/reference.md) |
| `gazelle.directives.ownership` | exclude skips matching inputs/trees, ignore protects the current BUILD file while still allowing descendant updates, and keep protects selected syntax. | [Ownership controls](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md) |
| `gazelle.directives.macros` | map_kind changes newly generated rule kinds; alias_kind teaches indexing/update behavior without forcing new rules to use the alias. | [Macro directives](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md) |

<a id="python-setup"></a>

## Choose Python runtimes and toolchain versions

Page: [rulesets/python/setup.md](../rulesets/python/setup.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `python.setup.exports` | The public rules have individual python/py_*.bzl entry points and python extension is exported from python/extensions/python.bzl. | [Python extension](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/extensions/python.bzl); [Binary export](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/py_binary.bzl) |
| `python.setup.defaults` | python.defaults chooses a default and python.toolchain requests runtimes; the ruleset registers its generated hub toolchains. | [Extension](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl); [Registration](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/MODULE.bazel) |
| `python.setup.version` | Executable targets accept X.Y or X.Y.Z python_version; a matching configured toolchain is required for the request to take effect. | [python_version attribute](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl) |
| `python.setup.overrides` | Python runtime override APIs have global, per-version and per-version/platform scopes. | [Override API](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/extensions/python.bzl); [Override implementation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/python.bzl) |

<a id="python-targets"></a>

## Model Python sources, imports, tests, and runfiles

Page: [rulesets/python/targets.md](../rulesets/python/targets.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `python.targets.files` | Python rules separate srcs, dependency providers, runtime data and propagated import paths. | [Common attributes](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/attributes.bzl) |
| `python.targets.entry` | main refers to a file in srcs; main_module executes a dependency-provided module and is mutually exclusive with main. | [Entry-point attributes](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl) |
| `python.targets.init` | legacy_create_init auto behavior consults module explicit_init_py configuration and flags; implicit creation is a configurable policy. | [Init policy](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl) |
| `python.targets.runfiles` | Python runfiles Rlocation applies repository mappings and EnvVars propagates runfiles discovery to child processes. | [Runfiles APIs](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/runfiles/runfiles.py) |
| `python.targets.precompile` | precompile and related attributes control bytecode generation, invalidation and source retention; pyc_collection controls dependency bytecode inclusion. | [Precompile attributes](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/attributes.bzl); [pyc_collection](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/py_executable.bzl) |

<a id="python-dependencies"></a>

## Resolve Python packages, hubs, and platform variants

Page: [rulesets/python/dependencies.md](../rulesets/python/dependencies.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `python.dependencies.hubs` | pip.parse configures concrete hubs and Python versions; a unified pypi repository routes package dependencies and pypi is reserved as a concrete hub name. | [Hub API](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl) |
| `python.dependencies.locks` | The parser supports requirements files and uv_lock metadata; uv_lock is handled by implementation despite a stale requirements-only documentation statement. | [Lock parser](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/parse_requirements.bzl); [uv_lock attribute](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl) |
| `python.dependencies.platforms` | target_platforms controls evaluated package variants; requirements_by_platform maps lock files to named pip platforms and defaults otherwise evaluate the host placeholder. | [Platform expansion](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/hub_builder.bzl); [Requirements mapping](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/pip_repository_attrs.bzl) |
| `python.dependencies.labels` | Hub package aliases expose library/data/metadata/wheel targets; console entry points have a dedicated rule. | [Hub target interface](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/docs/pypi/use.md) |
| `python.dependencies.sources` | download_only disables source wheel builds; wheel build-file modifications and distribution patches use distinct extension APIs. | [download_only](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/attrs.bzl); [whl_mods and override](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/pypi/extension.bzl) |

<a id="python-native-extensions"></a>

## Connect Python runtimes to C and C++ extensions

Page: [rulesets/python/native-extensions.md](../rulesets/python/native-extensions.md).

| Claim ID | Bounded statement | Exact evidence |
| --- | --- | --- |
| `python.native.headers` | current_py_cc_headers and current_py_cc_headers_abi3 resolve headers through the Python C/C++ toolchain; missing ABI3 headers fail. | [Header providers](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/current_py_cc_headers.bzl) |
| `python.native.extension` | Experimental py_extension builds a shared library, wraps its output with Python naming and PyInfo, and separates static from dynamic dependencies. | [Extension macro](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_macro.bzl); [Wrapper](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_rule.bzl) |
| `python.native.abi` | In the inspected implementation py_limited_api controls the abi3 output filename but does not add Py_LIMITED_API to compilation or prove ABI compliance. | [Arguments/compilation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_macro.bzl); [Filename selection](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_rule.bzl) |
| `python.native.libs` | current_py_cc_libs forwards the selected Python C/C++ toolchain libraries and linking metadata; it is distinct from header selection. | [Library forwarding](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/current_py_cc_libs.bzl) |

## Source discrepancies kept out of recommendations

- The Go quick-start documentation contains sample ruleset/SDK versions different
  from the inspected release; this reference uses release identities and source
  APIs instead of those sample pins.
- Python's lock overview still says requirements.txt is the only format. The
  2.4.6 extension and parser explicitly implement `uv_lock`.
- Python's introductory example still chooses concrete `hub_name = "pypi"`.
  The 2.4.6 API reserves that name for the unified hub and marks that use deprecated.
- A Python `.abi3` filename is not evidence that compilation was restricted to
  the stable ABI. The inspected `py_limited_api` flow only changes filename selection.

These discrepancies are bounded source-review findings. Executable claim coverage
and BuildBuddy integration are tracked in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
