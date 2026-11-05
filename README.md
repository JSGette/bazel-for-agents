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

## Start with the foundations

**Status: foundational guidance available; broader coverage planned.** All pages
below cite Bazel 9.3.1 sources. Their executable examples have verification records;
those records distinguish tested behavior from source-only assertions.

| Task | Read |
| --- | --- |
| Understand repositories, packages, labels, and targets | [Labels and targets](core/labels-and-targets.md) |
| Understand when code runs and which graph to inspect | [Phases and graphs](core/phases-and-graphs.md) |
| Define a rule's attributes and implementation | [Rule contract](core/rule-contract.md) |
| Pass information between dependent rules | [Providers](core/providers.md) |
| Choose default outputs, optional outputs, and runtime files | [Outputs and runfiles](core/outputs-and-runfiles.md) |
| Control dependency and load access | [Visibility](core/visibility.md) |
| Produce a file with a declared action | [Declaring actions](actions/declaring-actions.md) |
| Understand the Bazel Starlark dialect and file contexts | [Dialect and contexts](starlark/dialect-and-contexts.md) |
| Choose a list, dictionary, set, or depset | [Collections](starlark/collections.md) |

For a first custom rule, read phases → rule contract → providers → declaring
actions, following the [foundation fixture](examples/foundations/defs.bzl).

## Reference and maintenance

| Need | Read |
| --- | --- |
| Understand the approved structure and remaining topics | [Structure](docs/structure.md) |
| Check the reference versions | [Baseline](versions/baseline.json) |
| See claims checked during the initial investigation | [Evidence](docs/evidence.md) |
| Choose initial language and toolchain coverage | [Ruleset inventory](rulesets/README.md) |
| Write or review a guidance page | [Verification policy](maintenance/verification.md), [topic template](templates/topic.md) |

Module resolution, toolchain resolution, individual rulesets, and remote execution
remain planned sections. The [ruleset inventory](rulesets/README.md) records
candidate releases; it is not a tested combination of dependencies.

## Design commitments

- Keep `AGENTS.md` small and use this README as the routing index.
- Give each topic one canonical home; cross-link instead of duplicating advice.
- Store examples as runnable fixtures and quote or extract their tested source.
- Keep evidence and version metadata separate from the short instruction body.
- Publish only verified guidance in the task index. Keep research gaps visible
  to maintainers without presenting them as agent instructions.
- Make upgrades deliberate: discover a release, verify its APIs, test fixtures,
  then update the recommendation and its evidence together.
