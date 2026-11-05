# Starlark, actions, and testing: source evidence

Inspected on 2026-11-05. All claims below are **source-verified**, except that the
existing foundations record referenced below contains its own narrower runtime
coverage. This expansion ran no new fixtures, upstream tests, or ruleset builds.

## Exact source identities

- Bazel 9.3.1: `fee2bf2d1c14bc2096068a4d46f1842472092044`.
- rules_testing 0.9.0 tag: `db007bfee840cebcb6f955b80973ba866de38947`.
- bazel_skylib 1.9.2 tag: `3de43ed45e1c7923d53c4db56ca3de3e46601580`.
- Registry snapshot: `9bc19aec3357f320fc262ab71a8d054af6b6a74d`.

The release commits were resolved from their upstream tags and their source was
inspected directly. Registry source metadata identifies the published archives:
[rules_testing source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_testing/0.9.0/source.json),
[bazel_skylib source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_skylib/1.9.2/source.json).
The rules_testing archive has a registry patch correcting its module version;
its upstream MODULE.bazel still declares `0.0.1`. The library API evidence here
comes from the resolved release commit, not that unpatched manifest version.

No fixture resolved a new transitive module graph for these library versions.
Their source manifests declare minimum dependencies, not the graph selected in a
consumer module. No platform, rc configuration, toolchain, or runtime compatibility
is certified by these source-only pages.

## Claims

Each record identifies a bounded statement and the inspected symbol. Page prose
links the same exact sources beside related factual claims. Editorial choices
are labeled as repository recommendations rather than measured results.

### starlark.freeze.evaluation

Values created under a Starlark evaluation become immutable when its mutability closes; loaded modules are frozen before import.

Page: [starlark/mutability-and-freezing.md](../starlark/mutability-and-freezing.md).
Evidence: [Mutability class contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/Mutability.java).

### starlark.freeze.iteration

An actively iterated mutable container cannot itself be mutated; iteration does not temporarily freeze its elements.

Page: [starlark/mutability-and-freezing.md](../starlark/mutability-and-freezing.md).
Evidence: [Mutability iterator-count contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/Mutability.java).

### starlark.freeze.copy

list, dict, and set constructors create new containers; copying a container does not recursively copy its contents.

Page: [starlark/mutability-and-freezing.md](../starlark/mutability-and-freezing.md).
Evidence: [list(), dict(), set() implementations](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/MethodLibrary.java).

### starlark.freeze.macro

Symbolic macros cannot mutate their arguments and use a separate evaluation context.

Page: [starlark/mutability-and-freezing.md](../starlark/mutability-and-freezing.md).
Evidence: [executeMacroImplementation; macro-guide Restrictions](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/MacroClass.java).

### starlark.depset.structure

Depsets are immutable nested aggregations; direct and transitive components preserve shared subgraphs.

Page: [starlark/depsets.md](../starlark/depsets.md).
Evidence: [Depset class and fromDirectAndTransitive](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java).

### starlark.depset.elements

Nonempty depsets require a single Starlark element type; lists and dictionaries are rejected as elements.

Page: [starlark/depsets.md](../starlark/depsets.md).
Evidence: [checkElement, checkType](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java).

### starlark.depset.order

The four traversal orders differ, incompatible nondefault orders cannot merge, and duplicate or mixed-order traversal has limits.

Page: [starlark/depsets.md](../starlark/depsets.md).
Evidence: [class documentation, toListForStarlark, fromDirectAndTransitive](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java).

### starlark.depset.identity

Depset equality is not content equality; to_list returns a copy without duplicates and boolean emptiness is constant-time.

Page: [starlark/depsets.md](../starlark/depsets.md).
Evidence: [class documentation, truth, toListForStarlark](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java).

### starlark.depset.args

Args accepts depsets and postpones their expansion until command-line construction for execution.

Page: [starlark/depsets.md](../starlark/depsets.md).
Evidence: [CommandLineArgsApi class documentation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### starlark.macro.availability

macro is enabled by default at Bazel 9.3.1 and definitions must be exported before instantiation.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [macro(), MacroFunction.call; language-options experimental_enable_first_class_macros](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java).

### starlark.macro.attributes

Symbolic macro attributes are typed, name and visibility are implicit, and label strings resolve in the caller context.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [Attributes; MacroClass.instantiateAndAddMacro](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md).

### starlark.macro.configurable

Configurable non-None values are wrapped in selectors; inherited optional attributes default to None.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [executeMacroImplementation, shouldForceDefaultToNone](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/MacroClass.java).

### starlark.macro.naming

Created names must match the macro name or its underscore, dot, or dash prefix; violations cannot be built or depended on.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [Naming conventions](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md).

### starlark.macro.restrictions

Symbolic macros cannot return values, mutate arguments, call glob/package, or inspect existing_rules unless finalizers.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [Restrictions; MacroClass.executeMacroImplementation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md).

### starlark.macro.visibility

Exporting a target forwards the macro visibility; internal target visibility is based on the macro definition context.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [Visibility and macros](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md).

### starlark.macro.finalizers

Finalizers execute after nonfinalizer targets; ordinary macros cannot instantiate a finalizer.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [MacroFunction.call; MacroClass.isFinalizer](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java).

### starlark.macro.evaluation

Bazel 9.3.1 does not promise demand-driven lazy expansion of symbolic macros.

Page: [starlark/symbolic-macros.md](../starlark/symbolic-macros.md).
Evidence: [MacroFunction.call expansion logic; macro-guide Laziness](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java).

### actions.args.lazy

Args retains depsets and applies argument transformations during command-line construction for execution.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [class documentation, add_all, add_joined](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### actions.args.tokens

add handles single values, add_all emits separate arguments, and add_joined emits a joined argument.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [add, add_all, add_joined](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### actions.args.mapping

map_each runs after directory expansion; it is top-level by default and may filter or expand arguments.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [add_all processing order, map_each, allow_closure](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### actions.args.params

Parameter-file format defaults to shell; explicit formats and spill thresholds are independent choices.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [use_param_file, set_param_file_format](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### actions.args.dependencies

Passing File values through arguments does not replace declaring input/tool dependencies.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [run inputs, tools, arguments](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.args.shell

run_shell indexes flattened argument values, so unknown Args lengths make subsequent indices unpredictable.

Page: [actions/arguments-and-param-files.md](../actions/arguments-and-param-files.md).
Evidence: [run_shell arguments and command](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.inputs.contract

run has separate inputs, outputs, executable, tools, and arguments interfaces; tools are implicitly inputs.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [run and TOOLS_ARG_DOC](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.inputs.runfiles

Direct FilesToRunProvider entries and supported ctx.executable files carry tool runfiles; arbitrary paths do not encode that dependency.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [TOOLS_ARG_DOC; action-impl run and registerStarlarkAction](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.inputs.exec

Executable tool attributes need an explicit configuration, and execution tools should use the execution configuration.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [attr.label executable and cfg](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java).

### actions.environment.defaults

use_default_shell_env defaults false; enabling it includes default action environment and explicit env overrides it.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [registerStarlarkAction environment branch; actions API defaults](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java).

### actions.resources.local

resource_set accepts a dictionary or top-level callback and estimates local scheduling resources.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [run resource_set; action-impl parseResourceSetFromDict](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.inputs.unused

unused_inputs_list promises that changes to listed unused files cannot affect outputs.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [run unused_inputs_list](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.inputs.platform

toolchain identifies the action toolchain. An explicit exec_group selects the platform; when automatic groups are active, the supplied toolchain type must be declared by that group.

Page: [actions/inputs-tools-environment.md](../actions/inputs-tools-environment.md).
Evidence: [run toolchain and exec_group](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

Additional implementation evidence: [determineExecGroup](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java).

### actions.directory.declaration

declare_directory produces a directory artifact whose expanded contents are regular files and directories.

Page: [actions/directories-and-symlinks.md](../actions/directories-and-symlinks.md).
Evidence: [declare_directory](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.directory.expansion

Args can expand directory files at execution time; directory contents are not ordinary analysis-time Starlark values.

Page: [actions/directories-and-symlinks.md](../actions/directories-and-symlinks.md).
Evidence: [add_all expand_directories; actions declare_directory](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java).

### actions.directory.mapping

The API is experimental and gated by experimental_allow_map_directory, default true in 9.3.1. [Flag definition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java), [implementation gate](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java).

map_directory expands built input directories and calls a top-level function to create actions into output directories.

Page: [actions/directories-and-symlinks.md](../actions/directories-and-symlinks.md).
Evidence: [map_directory and MAP_DIRECTORY_IMPLEMENTATION_DOC](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.symlink.file

symlink with target_file uses a declared file or directory output matching the target type and tracks the referent.

Page: [actions/directories-and-symlinks.md](../actions/directories-and-symlinks.md).
Evidence: [symlink target_file contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.symlink.path

Unresolved symlink declaration is gated by allow_unresolved_symlinks, default true in 9.3.1. [Flag definition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java), [implementation gate](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java).

symlink with target_path uses declare_symlink, preserves path text without resolving it, and can be dangling.

Page: [actions/directories-and-symlinks.md](../actions/directories-and-symlinks.md).
Evidence: [declare_symlink, symlink target_path and target_type](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### actions.hermetic.inputs

Undeclared files and changing host tools can invalidate incremental and cached build assumptions.

Page: [actions/hermeticity-and-reproducibility.md](../actions/hermeticity-and-reproducibility.md).
Evidence: [Reasons for sandboxing; hermeticity Identifying non-hermeticity](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/docs/sandboxing.md).

### actions.hermetic.sandbox

Sandboxing constrains actions according to strategy; local execution is unsandboxed and sandboxing does not hide all host reads.

Page: [actions/hermeticity-and-reproducibility.md](../actions/hermeticity-and-reproducibility.md).
Evidence: [Sandboxing overview and strategies](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/docs/sandboxing.md).

### actions.hermetic.nondeterminism

Timestamps, nondeterministic tools, host binaries, and source-tree writes are documented sources of non-hermetic behavior.

Page: [actions/hermeticity-and-reproducibility.md](../actions/hermeticity-and-reproducibility.md).
Evidence: [Identifying non-hermeticity](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/basics/hermeticity.md).

### actions.hermetic.environment

Explicit tool/input/environment declarations are separate from scheduling and platform selection.

Page: [actions/hermeticity-and-reproducibility.md](../actions/hermeticity-and-reproducibility.md).
Evidence: [run parameter contracts](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### testing.unit.scope

rules_testing unit_test tests generic Starlark helpers and wraps the analysis-test machinery.

Page: [testing/starlark-unit-tests.md](../testing/starlark-unit-tests.md).
Evidence: [unit_test](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/unit_test.bzl).

### testing.unit.suite

rules_testing test_suite has tests, basic_tests, and test_kwargs parameters; there is no custom_tests parameter.

Page: [testing/starlark-unit-tests.md](../testing/starlark-unit-tests.md).
Evidence: [test_suite signature and implementation](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/test_suite.bzl).

### testing.unit.assertions

Test callbacks use env.expect for assertions or env.fail to record failures.

Page: [testing/starlark-unit-tests.md](../testing/starlark-unit-tests.md).
Evidence: [_begin_analysis_test and _end_analysis_test](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/analysis_test.bzl).

### testing.unit.skylib

bazel_skylib unittest exposes make, suite, begin, end and asserts; it is a distinct API from rules_testing.

Page: [testing/starlark-unit-tests.md](../testing/starlark-unit-tests.md).
Evidence: [unittest and asserts exports](https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/unittest.bzl).

### testing.analysis.entry

rules_testing exports analysis_test from lib/analysis_test.bzl; its callback receives env and the target value.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [analysis_test export; rt-analysis implementation](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/analysis_test.bzl).

### testing.analysis.subjects

TargetSubject exposes default outputs, runfiles, providers, and action selection through the testing aspect.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [TargetSubject methods](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/target_subject.bzl).

### testing.analysis.actions

ActionSubject exposes argv, inputs, environment, mnemonic, and supported builtin action properties.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [ActionSubject public struct](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/action_subject.bzl).

### testing.analysis.failure

expect_failure enables allow_analysis_failures; assertions must still verify target failure messages.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [expect_failure branch; rt-target failures](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/analysis_test.bzl).

### testing.analysis.config

config_settings and per-target settings apply analysis-test transitions to target-under-test dependencies.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [analysis_test parameters and transition construction](https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/analysis_test.bzl).

### testing.analysis.limits

Analysis test rules are restricted, cannot register actions, and report through AnalysisTestResultInfo.

Page: [testing/analysis-tests.md](../testing/analysis-tests.md).
Evidence: [rule analysis_test parameter](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java).

### testing.execution.inputs

Tests consume declared runtime inputs through runfiles; runfiles must not be modified.

Page: [testing/execution-tests.md](../testing/execution-tests.md).
Evidence: [Role of build system; Test interaction with filesystem](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/reference/test-encyclopedia.md).

### testing.execution.paths

TEST_TMPDIR and TEST_UNDECLARED_OUTPUTS_DIR have distinct scratch and retained-output purposes.

Page: [testing/execution-tests.md](../testing/execution-tests.md).
Evidence: [Initial conditions; filesystem interaction](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/reference/test-encyclopedia.md).

### testing.execution.exit

The test runner determines success from successful process completion within its timeout.

Page: [testing/execution-tests.md](../testing/execution-tests.md).
Evidence: [Role of test runner](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/reference/test-encyclopedia.md).

### testing.execution.shards

Sharded runners use TEST_TOTAL_SHARDS, TEST_SHARD_INDEX, and TEST_SHARD_STATUS_FILE.

Page: [testing/execution-tests.md](../testing/execution-tests.md).
Evidence: [Test sharding](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/reference/test-encyclopedia.md).

### testing.execution.cache

cache_test_results defaults auto; test caching and reruns depend on options and prior outcomes.

Page: [testing/execution-tests.md](../testing/execution-tests.md).
Evidence: [cache_test_results option](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/test/TestConfiguration.java).

### testing.integration.boundary

Analysis tests inspect configured targets and cannot replace loading or real-tool execution checks.

Page: [testing/rule-integration-tests.md](../testing/rule-integration-tests.md).
Evidence: [rule analysis_test contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java).

### testing.integration.fixture

Existing foundations fixture separately checks action structure, generated contents, optional outputs, and a provider rejection.

Page: [testing/rule-integration-tests.md](../testing/rule-integration-tests.md).
Evidence: [existing fixture](../examples/foundations/verify.py), [execution record](foundations.md).

### testing.integration.cache

A test rerun policy is separate from build action execution and must be recorded when interpreting a result.

Page: [testing/rule-integration-tests.md](../testing/rule-integration-tests.md).
Evidence: [cache_test_results; actions execution contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/test/TestConfiguration.java).

## Review findings

- `resource_set` at Bazel 9.3.1 accepts dictionaries as well as callbacks. Its
  local-scheduling meaning is separate from remote platform properties.
- `map_directory` is a supported API in the inspected release. Ordinary analysis
  cannot be described as directly reading generated directory contents.
- The `rules_testing` 0.9.0 unit-test guide contains `custom_tests` in an example,
  but `lib/test_suite.bzl` accepts `tests`, `basic_tests`, and `test_kwargs`. The
  implementation is the source for this reference.
- `expect_failure` enables analysis failure observation; the test still needs
  an assertion on the intended failure. It is not an automatic passing condition.
- Symbolic macro naming and encapsulation are useful now; demand-driven lazy
  macro expansion is not claimed at this baseline.

Executable claim coverage and BuildBuddy are deferred in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

## Aspects

These additional claims use the same Bazel 9.3.1 source commit and source-only
scope. Page: [core/aspects.md](../core/aspects.md).

### core.aspects.graph

An aspect adds analysis applications along selected dependency edges, can register
actions, and returns providers. The implementation receives target and ctx.

Evidence: [aspect API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java),
[StarlarkAspectFactory.createAspect](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/StarlarkAspectFactory.java).

### core.aspects.application

An aspect can be attached to dependency attributes or selected at the command line.
Attribute propagation and toolchain propagation have distinct parameters.

Evidence: [aspect application guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/aspects.md),
[attr_aspects and toolchains_aspects API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java).

### core.aspects.providers

required_providers uses advertised providers with all-within-group and any-group
semantics. Ordinary duplicate providers are rejected when aspect values merge.

Evidence: [AspectDefinition.satisfies](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/AspectDefinition.java),
[MergedConfiguredTarget.of](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/configuredtargets/MergedConfiguredTarget.java).

### core.aspects.composition

required_aspect_providers governs other-aspect provider visibility; requires lists
aspects that must propagate before the current one. provides promises returned
types. These are distinct from base-rule applicability.

Evidence: [aspect parameter definitions](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java).

### core.aspects.parameters

The constructor accepts bool, int, and string public parameters. Rule-propagated
and command-line applications use different parameter-extraction paths.

Evidence: [StarlarkRuleClassFunctions.aspect validation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java),
[StarlarkDefinedAspect parameter extractors](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/StarlarkDefinedAspect.java).

### core.aspects.default-files

Aspect DefaultInfo files are merged with a dependency's default files. For the
non-top-level merge, other DefaultInfo fields are rejected. This supersedes the
release guide's blanket prohibition on aspect DefaultInfo.

Evidence: [MergedConfiguredTarget.of](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/configuredtargets/MergedConfiguredTarget.java),
[mergesFileProvider, aspectDefaultInfoWithNonArtifacts, aspectDefaultInfoSomethingElseThanFiles, aspectEmptyDefaultInfo](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/starlark/StarlarkDefinedAspectsTest.java).

### core.aspects.output-groups

Same-named output groups contributed by the rule and aspect combine their files.
Both the guide and OutputGroupInfo.merge's comment retain obsolete disjointness
wording; implementation and the exact-release regression test agree on merging.

Evidence: [OutputGroupInfo.merge implementation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/OutputGroupInfo.java),
[duplicateOutputGroups test](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/starlark/StarlarkDefinedAspectsTest.java).

### core.aspects.generating-rules

apply_to_generating_rules defaults false. When enabled it follows output targets
to their generating rules. It cannot be combined with nonempty required_providers
or a propagation predicate.

Evidence: [aspect API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java),
[constructor guards](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java).
