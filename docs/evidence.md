# Evidence index

Reviewed on **2026-11-05**. The [task index](../README.md) routes readers to
instruction pages; this index routes maintainers to the evidence behind them.
Source review, inspecting an upstream test, and executing a local fixture are
separate kinds of evidence. None establishes unmeasured agent-performance gains.

## Exact reference identities

- **Bazel 9.3.1:** source commit `fee2bf2d1c14bc2096068a4d46f1842472092044`.
  The official binary was checksum-verified and used for the existing fixtures;
  see [binary identity](../verification/starlark-set.md).
- **REAPI v2.12.0:** source commit `9e084d0e43e717128ee72b5be584a7ba33e8006b`.
  The protocol reference and Bazel's declared client range are recorded separately
  in [capabilities and versions](../remote/capabilities-and-versions.md).
- **Rulesets:** release source identity and registry snapshot are recorded in
  [versions/rulesets.json](../versions/rulesets.json) and the ledgers below.
  Reviewed source versions are candidates, not a resolved/tested combination.

See [baseline metadata](../versions/baseline.json) and the
[verification policy](../maintenance/verification.md) for the exact interpretation.

## Source review records

| Coverage | Evidence |
| --- | --- |
| Labels, phases, and graphs | [Core labels and phases](../verification/core-labels-phases.md) |
| Rule implementations and providers | [Rules and providers](../verification/core-rules-providers.md) |
| Outputs, runfiles, and initial action model | [Outputs and actions](../verification/core-outputs-actions.md) |
| Dependency and load visibility | [Visibility](../verification/core-visibility.md) |
| Starlark dialect and collections | [Starlark basics](../verification/starlark-basics.md) |
| Modules, repositories, files, and package boundaries | [Modules](../verification/modules.md) |
| Configuration, rc files, and toolchain resolution | [Configuration and toolchains](../verification/configuration-toolchains.md) |
| Mutability, depsets, macros, advanced actions, testing, and aspects | [Starlark, actions, and testing](../verification/starlark-actions-testing.md) |
| Go, Gazelle, Python | [Language rules](../verification/rulesets-go-python.md) |
| C/C++, shell, packaging, native build tools and platforms | [Native rulesets](../verification/rulesets-native.md) |
| Rust, protobuf, RPC, Prost, and utility libraries | [Rust, protobuf, utilities](../verification/rulesets-rust-proto-utilities.md) |
| Query graphs, logs, profiles, and events | [Diagnostics](../verification/diagnostics.md) |
| REAPI and inspected Bazel remote-client behavior | [Remote](../verification/remote.md) |

## Executed fixtures

| Fixture | Observed scope |
| --- | --- |
| [Starlark set](../verification/starlark-set.md) | Constructor, deduplication, membership, mutation, union, and sorted generated contents. |
| [Foundations](../verification/foundations.md) | Producer/consumer rules, providers, outputs/runfiles metadata, optional output selection, query views, generated contents, and expected provider rejection. |
| [Visibility](../verification/core-visibility.md) | Allowed target/load access and expected failures for denied access. |

The records contain versions, commands, environment, observed results, and limits.
They do not cover all new source-reviewed pages. Exhaustive executable assertions,
ruleset integration graphs, and BuildBuddy CI are follow-up work in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

## Resolving conflicting upstream documentation

Versioned documentation can still be stale. The source reviews found discrepancies
in collection support, repository reproducibility, compatibility-level arguments,
toolchain platform ranking, transition validation, aspect output merging, and
several ruleset examples. The relevant page and ledger cite the implementation or
test that resolves each discrepancy. Reading a test establishes its intended
assertion, not that it passed in this environment.

Teach the verified current behavior directly. Do not reproduce obsolete recipes
in an agent-facing page merely to explain why they are obsolete.
