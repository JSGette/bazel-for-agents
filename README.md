# Bazel for Agents

Focused, evidence-backed instructions for agents working with **Bazel 9.3.1+**.
This project exists to give agents the relevant, version-correct build knowledge
they need to complete a task. Its central hypothesis is that curated instructions
can reduce mistakes caused by obsolete or mixed-version Bazel knowledge.

## Why this repository exists

Research provides a reason to test that hypothesis:

| Research | Finding | Our design response |
| --- | --- | --- |
| [LibEvoBench](https://arxiv.org/html/2606.25402v1), 2026 | On Python API tasks, relevant method descriptions improved API-calling accuracy by 10–20 percentage points. Adding a version constraint to that context did not produce further measurable gains. | Supply concrete APIs, semantics, and examples for the exact version; a version number alone is insufficient guidance. |
| [DocPrompting](https://arxiv.org/abs/2207.05987v3), ICLR 2023 | Retrieving relevant documentation improved Python and Bash code generation, including execution-based evaluation. | Organize small pages by task so an agent can retrieve the instructions it needs. |
| [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), TACL 2024 | On retrieval and question-answering tasks, models' performance depended on where relevant information appeared in long contexts. | Keep the routing instructions short and load technical pages selectively. |
| [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988v3), 2026 | Repository context files did not generally improve coding-task success and increased inference cost by over 20% on average. | Treat instructions as a hypothesis to evaluate; remove redundant guidance and measure cost as well as correctness. |

These are motivations, not measured results for this repository. The studies
cover different models and tasks; LibEvoBench supplied descriptions directly and
used no thinking budget. Our proposed evaluation compares ordinary project
context, an explicit Bazel version instruction, version-matched upstream docs,
and this reference under matched task and tool budgets. Measure build/test
success, version-specific errors, time, and tokens. Track modern idiom adoption
separately from correctness. No agent-performance evaluation has been run here.

The editorial scope is modern Bazel, current stable rulesets, and current remote
execution APIs. Each technical claim is bounded by the version and environment
actually verified. See [AGENTS.md](AGENTS.md) for how to use the reference.

## Choose the task, then load its pages

**Status: source-verified fundamentals and ruleset API guidance are available.**
Bazel semantics are checked against immutable **9.3.1** sources. Ruleset pages
identify exact reviewed releases; they are **not a tested dependency combination**.
The [existing fixtures](verification/foundations.md) provide limited runtime
coverage, with additional [set](verification/starlark-set.md) and
[visibility](verification/core-visibility.md) records. New source-only pages say
what has not been run. Read metadata together with the evidence boundary.

BuildBuddy and exhaustive claim-to-snippet verification are deferred to
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

### Core and Starlark

| Task | Read |
| --- | --- |
| Identify repositories, packages, labels, and targets | [Labels and targets](core/labels-and-targets.md) |
| Select source files and define package boundaries | [Files, globs, and packages](core/files-and-packages.md) |
| Understand loading, analysis, execution, and their graphs | [Phases and graphs](core/phases-and-graphs.md) |
| Define attributes and a rule implementation | [Rule contract](core/rule-contract.md) |
| Pass information between rules | [Providers](core/providers.md) |
| Choose default outputs, output groups, and runfiles | [Outputs and runfiles](core/outputs-and-runfiles.md) |
| Control dependency and extension-load access | [Visibility](core/visibility.md) |
| Traverse targets with additional analysis | [Aspects](core/aspects.md) |
| Use the right language features for the evaluation context | [Dialect and contexts](starlark/dialect-and-contexts.md) |
| Choose collections and understand their lifetime | [Collections](starlark/collections.md), [mutability and freezing](starlark/mutability-and-freezing.md) |
| Propagate transitive data without repeated flattening | [Depsets](starlark/depsets.md) |
| Provide a reusable target-declaration API | [Symbolic macros](starlark/symbolic-macros.md) |

For a first custom rule, read phases → rule contract → providers → declaring
actions, following the [foundation fixture](examples/foundations/defs.bzl).

### Actions

| Task | Read |
| --- | --- |
| Declare a producing action | [Declaring actions](actions/declaring-actions.md) |
| Construct arguments and response files | [Arguments and parameter files](actions/arguments-and-param-files.md) |
| Supply tools, runtime files, inputs, and environment | [Inputs, tools, and environment](actions/inputs-tools-environment.md) |
| Work with tree artifacts, directory mapping, and links | [Directories and symlinks](actions/directories-and-symlinks.md) |
| Make the execution contract complete and repeatable | [Hermeticity and reproducibility](actions/hermeticity-and-reproducibility.md) |

### Dependencies and repositories

| Task | Read |
| --- | --- |
| Declare modules and explain selected versions | [Dependencies and version selection](modules/dependencies-and-version-selection.md) |
| Configure extensions and import generated repositories | [Extensions](modules/extensions-and-generated-repositories.md) |
| Materialize a repository with tracked inputs | [Repository rules](modules/repository-rules.md) |
| Resolve apparent and canonical repository names | [Repository mapping](modules/repository-mapping.md) |
| Maintain resolution state and vendored sources | [Lockfiles and vendoring](modules/lockfile-and-vendor.md) |
| Replace a dependency or apply a patch deliberately | [Overrides and patches](modules/overrides-and-patches.md) |

### Configuration and toolchains

| Task | Read |
| --- | --- |
| Understand effective invocation configuration | [Rc files and invocations](configuration/rc-and-invocations.md) |
| Model execution and target environments | [Platforms and constraints](configuration/platforms-and-constraints.md) |
| Choose configurable attribute values | [Select and build settings](configuration/select-and-build-settings.md) |
| Change configuration across dependency edges | [Transitions](configuration/transitions.md) |
| Request toolchain interfaces in a rule | [Consuming toolchains](toolchains/consuming.md) |
| Supply and register implementations | [Defining and registering](toolchains/defining-and-registering.md) |
| Explain compatibility, priority, and optional-toolchain selection | [Resolution](toolchains/resolution.md) |
| Give actions distinct execution requirements | [Execution groups](toolchains/execution-groups.md) |
| Build for a different target environment | [Cross-compilation](toolchains/cross-compilation.md) |

### Language rules and supporting rulesets

The [ruleset index](rulesets/README.md) links every ruleset page and records
candidate release evidence. Start with the relevant family:

| Family | Entry points |
| --- | --- |
| Go and Gazelle | [Setup](rulesets/go/setup.md), [dependencies](rulesets/go/dependencies.md), [BUILD generation](rulesets/gazelle/generation.md), [cgo](rulesets/go/cgo.md) |
| C/C++ | [Setup](rulesets/cc/setup.md), [targets](rulesets/cc/targets.md), [linking](rulesets/cc/linking.md) |
| Python | [Setup](rulesets/python/setup.md), [dependencies](rulesets/python/dependencies.md), [native extensions](rulesets/python/native-extensions.md) |
| Rust | [Choose the integration](rulesets/rust/choosing-integration.md), [dependencies](rulesets/rust/dependencies.md), [build scripts](rulesets/rust/build-scripts.md), [FFI](rulesets/rust/ffi.md) |
| Protobuf and RPC | [Setup](rulesets/protobuf/setup.md), [code generation](rulesets/protobuf/code-generation.md), [gRPC](rulesets/protobuf/grpc.md), [Prost](rulesets/protobuf/prost.md) |
| Shell | [Setup](rulesets/shell/setup.md), [targets](rulesets/shell/targets.md), [runfiles](rulesets/shell/runfiles.md) |
| Packaging | [File mappings](rulesets/packaging/file-mappings.md), [archives](rulesets/packaging/archives.md), [metadata](rulesets/packaging/metadata.md) |
| Foreign native builds | [Setup](rulesets/foreign-cc/setup.md), [toolchains](rulesets/foreign-cc/toolchains.md), [hermeticity](rulesets/foreign-cc/hermeticity.md) |
| Compilers and operating systems | [LLVM](rulesets/llvm/setup.md), [GCC](rulesets/gcc/setup.md), [Apple](rulesets/apple/setup.md), [Windows](rulesets/windows/toolchain-selection.md) |
| Starlark libraries and prebuilt tools | [Library selection](rulesets/utilities/library-selection.md), [multitool](rulesets/utilities/multitool.md), [regex](rulesets/utilities/regex.md) |

### Testing and diagnostics

| Task | Read |
| --- | --- |
| Test pure Starlark helpers | [Unit tests](testing/starlark-unit-tests.md) |
| Assert providers, actions, and expected analysis failures | [Analysis tests](testing/analysis-tests.md) |
| Assert generated contents and runtime behavior | [Execution tests](testing/execution-tests.md) |
| Exercise loading, resolution, and invocation boundaries | [Rule integration tests](testing/rule-integration-tests.md) |
| Inspect the right graph | [query](diagnostics/query.md), [cquery](diagnostics/cquery.md), [aquery](diagnostics/aquery.md) |
| Explain dependency or toolchain selection | [Module diagnosis](diagnostics/module-resolution.md), [toolchain diagnosis](diagnostics/toolchain-resolution.md) |
| Explain action failures and reuse | [Execution and cache misses](diagnostics/execution-and-cache-misses.md) |
| Understand time and structured build results | [Profiles and build events](diagnostics/profiles-and-build-events.md) |

### Remote builds

| Task | Read |
| --- | --- |
| Understand CAS, Action Cache, actions, commands, and results | [REAPI model](remote/reapi-model.md) |
| Share results or execute on workers | [Caching](remote/caching.md), [execution](remote/execution.md) |
| Distinguish protocol release, client support, and server features | [Capabilities and versions](remote/capabilities-and-versions.md) |
| Describe worker requirements | [Platforms and properties](remote/platforms-and-properties.md) |
| Understand content identity and transport | [Digests and transfers](remote/digests-and-transfers.md) |
| Control local artifact availability | [Outputs and downloads](remote/outputs-and-downloads.md) |

### Common task checklists

These compose the reference pages; they are not end-to-end tested recipes:
[add a code generator](recipes/add-code-generator.md),
[add a language dependency](recipes/add-language-dependency.md),
[cross-compile a binary](recipes/cross-compile-a-binary.md),
[package generated files](recipes/package-generated-files.md), and
[make an action suitable for remote execution](recipes/make-an-action-remotable.md).

## Reference and maintenance

| Need | Read |
| --- | --- |
| Understand the structure and scope | [Structure](docs/structure.md) |
| Check exact source identities and coverage | [Bazel/protocol baseline](versions/baseline.json), [ruleset versions](versions/rulesets.json) |
| Find source and execution evidence | [Evidence index](docs/evidence.md) |
| Write or review guidance | [Verification policy](maintenance/verification.md), [topic template](templates/topic.md) |
| Refresh a release deliberately | [Upgrades](maintenance/upgrades.md) |

## Design commitments

- Keep `AGENTS.md` small and use this README as the routing index.
- Give each topic one canonical home; cross-link instead of duplicating advice.
- Store examples as runnable fixtures and quote or extract their tested source.
- Keep evidence and version metadata separate from the short instruction body.
- Publish only verified guidance in the task index. Keep research gaps visible
  to maintainers without presenting them as agent instructions.
- Make upgrades deliberate: discover a release, verify its APIs, test fixtures,
  then update the recommendation and its evidence together.
