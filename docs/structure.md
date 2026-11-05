# Approved repository structure

This is the approved coverage plan. The [README](../README.md) indexes the pages
currently available; planned topics are not implementation instructions.
The initial baseline is Bazel 9.3.1. Later releases require their own evidence.
The initial technical findings and limitations are in [evidence.md](evidence.md).

## File layout

The topic files in the tree below are published as source-verified guidance or
as task checklists composing that guidance. Executed fixtures cover sets, a
producer/consumer rule pair, and target/load visibility; their records remain
separate from the wider source review. Exhaustive snippets, integration graphs,
and remote CI are deferred to [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
The future automation directories are not implemented placeholders.

```text
README.md                          # task-oriented index and coverage status
AGENTS.md                          # how to select and apply context
.bazelversion                      # exact baseline for verification fixtures
versions/
  baseline.json                    # Bazel and protocol reference identity
  rulesets.json                    # observed/source-reviewed identities; integration gaps
core/
  labels-and-targets.md
  files-and-packages.md
  aspects.md
  visibility.md                    # targets, .bzl loads, macro export boundaries
  phases-and-graphs.md
  rule-contract.md
  providers.md
  outputs-and-runfiles.md
starlark/
  dialect-and-contexts.md
  collections.md
  mutability-and-freezing.md
  depsets.md
  symbolic-macros.md
actions/
  declaring-actions.md
  arguments-and-param-files.md
  inputs-tools-environment.md
  directories-and-symlinks.md
  hermeticity-and-reproducibility.md
modules/
  dependencies-and-version-selection.md
  extensions-and-generated-repositories.md
  repository-rules.md
  repository-mapping.md
  lockfile-and-vendor.md
  overrides-and-patches.md
configuration/
  rc-and-invocations.md
  platforms-and-constraints.md
  select-and-build-settings.md
  transitions.md
toolchains/
  consuming.md
  defining-and-registering.md
  resolution.md
  execution-groups.md
  cross-compilation.md
rulesets/
  README.md                        # task routes, inventory, and verification status
  go/{setup,targets,dependencies,cgo}.md
  gazelle/{generation,directives}.md
  cc/{setup,targets,linking}.md
  python/{setup,targets,dependencies,native-extensions}.md
  rust/{choosing-integration,setup,targets,dependencies,build-scripts,ffi}.md
  protobuf/{setup,code-generation,grpc,prost}.md
  shell/{setup,targets,runfiles}.md
  packaging/{file-mappings,archives,metadata}.md
  foreign-cc/{setup,toolchains,hermeticity}.md
  llvm/{setup,sysroots,cross-compilation}.md
  gcc/{setup,cross-compilation}.md
  apple/{setup,platforms}.md
  windows/{toolchain-selection,paths-and-processes}.md
  utilities/{library-selection,multitool,regex,toml,configuration-wrappers}.md
testing/
  starlark-unit-tests.md
  analysis-tests.md
  execution-tests.md
  rule-integration-tests.md
remote/
  caching.md
  execution.md
  reapi-model.md
  capabilities-and-versions.md
  platforms-and-properties.md
  digests-and-transfers.md
  outputs-and-downloads.md
diagnostics/
  query.md
  cquery.md
  aquery.md
  module-resolution.md
  toolchain-resolution.md
  execution-and-cache-misses.md
  profiles-and-build-events.md
recipes/
  add-code-generator.md
  add-language-dependency.md
  cross-compile-a-binary.md
  package-generated-files.md
  make-an-action-remotable.md
examples/                          # small independently runnable fixtures
verification/                      # claim records and execution results
maintenance/
  verification.md
  upgrades.md
templates/
  topic.md
tools/                             # future metadata/link/fixture checks
.github/workflows/                 # future baseline and selected-release checks
```

## Core section coverage

| Section | Questions its narrowly scoped pages should answer |
| --- | --- |
| Core | What are labels, packages, targets, configured targets, artifacts, rules, and actions? How do loading, analysis, and execution relate? What does a rule expose through providers, outputs, and runfiles? |
| Starlark | Which language features and built-ins exist in each Bazel evaluation context? How do `set`, `dict`, `list`, and `depset` differ? What freezes, when, and why? How should symbolic macros define and forward attributes? |
| Actions | How are outputs declared and producing actions registered? How are tools and their runtime files supplied? When should `Args` and parameter files be used? What belongs in inputs, environment, and execution requirements? |
| Modules | How do declared and resolved versions differ? How do extensions produce repositories? How do repository mappings affect labels? How are lockfiles, vendoring, overrides, and patches maintained? |
| Configuration | How are platforms and constraints modeled? When does `select()` resolve? When are build settings or transitions justified? What is the analysis-cost impact? |
| Toolchains | How do type, implementation, declaration, and registration relate? How are target and execution constraints matched? How does precedence work in this exact baseline? How do execution groups and cross-compilation affect selection? |
| Testing | What can language, analysis, action-execution, and integration tests each establish? How are failures, providers, action arguments, and runfiles tested? |
| Remote | How do remote caching and execution differ? What do CAS, Action Cache, Action, Command, and input trees represent? Which protocol capabilities does the selected Bazel client actually use? |
| Diagnostics | Which graph does each query command inspect? How should an agent identify the cause of a missing target, wrong toolchain, undeclared input, or cache miss? |
| Recipes | What is the shortest verified sequence for a common task? Which canonical topic pages provide the explanation? |

## Initial ruleset coverage

Begin with Go and Gazelle, C/C++, Python, Rust, protobuf/gRPC/prost, shell,
packaging, foreign C/C++ builds, and compiler toolchains. Include analysis testing
and Starlark utilities alongside rule authoring. Exact candidate versions and
priority are in the [inventory](../rulesets/README.md).

For each ruleset, split setup, ordinary targets, dependency integration, and
specialized cases. Verify the module name, `load()` labels, extension symbols,
toolchain setup, and public providers from that ruleset's exact release. Include
only the sections that apply; do not force all rulesets into an identical tree.

Treat Rust integration choices explicitly rather than blending APIs from different
projects. Treat native interoperability as its own task: cgo, Rust FFI, Python
native extensions, and compiler/sysroot selection deserve separate examples.
Add Java, JavaScript, Android, and other ecosystems only after the initial scope
has validated coverage or a concrete task establishes a need.

## REAPI coverage boundaries

Pin the protocol release and commit independently from Bazel. Track four pieces
of evidence: protocol definition, Bazel client implementation, advertised server
capabilities, and a successful integration test. A field existing in the newest
protocol is insufficient evidence that a particular client/server pair uses it.

Begin with the action/CAS/cache model, capability negotiation, execution platform
properties, digest functions, transfer behavior, and output materialization.
Keep backend-specific configuration out of the generic core. Remote Asset API and
other adjacent APIs can get separate pages when validated use cases justify them.

## Page design and retrieval

Aim for one decision per page, generally 60–150 lines of guidance excluding
evidence. This is an editorial target, not a hard limit. Every page should name
its task, prerequisites, verified versions, preferred pattern, boundaries,
verification boundary, and sources. Runnable fixtures additionally need commands
and observed assertions. Front matter should make status machine-readable.

Do not create a catalog of obsolete examples. Teach the current pattern directly.
Mention a tempting mistake only when it prevents a likely error, without embedding
an obsolete implementation that an agent might reuse.

Keep nested `AGENTS.md` files for genuine local authoring constraints, if needed.
Do not use them as containers for all technical content. The root index and
explicit prerequisite links should control how much context an agent reads.

## Coverage boundaries and follow-up

The fundamentals, initial language paths, native interoperability, packaging,
remote model, and diagnostic sections now have source-reviewed guidance. The
[README](../README.md) and [ruleset index](../rulesets/README.md) route every page.
Task checklists compose those pages without claiming end-to-end execution.

Executable assertions for the expanded coverage, resolved ruleset integration
graphs, additional platforms, BuildBuddy orchestration, and recurring upgrade
checks are tracked in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
C++/Python gRPC release selection, supply-chain metadata/SBOM integrations, and
eBPF-specific rules remain explicit coverage gaps. Do not infer guidance for
those areas from an adjacent language or compiler chapter.

The source reference should let an agent identify the correct modern APIs and
reason about a build's graphs and contracts. Passing behavior for a particular
project still requires that project's exact resolved dependencies and tests.
