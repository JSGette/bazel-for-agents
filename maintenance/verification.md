# Verification policy

This policy is the quality gate for published guidance. It applies to all
Bazel semantics, command-line flags, ruleset APIs, version claims, and examples.

## Baseline and source identity

- Minimum editorial baseline: Bazel 9.3.1. Record exact versions tested; do not
  equate a minimum supported version with proof for every later version.
- Prefer primary sources at an immutable commit: implementation, tests, release
  notes, API definitions, then documentation. Discovery links may point to a
  release index; the evidence for a claim should pin the content inspected.
- Resolve contradictions by examining the implementation and a focused probe.
  A versioned documentation URL is not sufficient by itself when it is stale.
- Record observed stable releases separately from the project's tested selection.
  Ruleset integration verification must include its transitive resolved module
  graph. Source review of an individual release establishes its exported API,
  not that the release resolves unchanged or works with every other candidate.
- Record REAPI identity separately from Bazel, and protocol support separately
  from actual client/server interoperability.

## Claim records

Maintain one record per independently checkable factual claim. A page can use
multiple claim IDs. Record:

```yaml
id: starlark.set.constructor
status: source-verified # proposed | source-verified | runtime-verified
statement: "A precise, bounded claim goes here."
bazel: "9.3.1"
rulesets: {}
platforms: []
flags: []
configuration_inputs: [] # rc loading and relevant non-secret environment
sources: []            # exact URL/revision plus relevant symbol or lines
fixture: null
commands: []
expected: null
observed: null
verified_at: null
limitations: []
```

`source-verified` means the cited source supports the assertion. `runtime-verified`
means the named fixture also exercised it in the recorded environment. Neither
status grants coverage beyond the claim's scope. A planned topic is not a claim.

For page metadata, `bazel_verified` and `rulesets_verified` identify versions
whose relevant sources or behavior were checked; `status` and the evidence record
say which kind of check occurred. They are not compatibility declarations.
Ruleset-only source reviews use `bazel_baseline: "9.3.1"` and an empty
`bazel_verified` list when Bazel itself was not part of that review.
`platforms_verified: []` means no platform execution is claimed.

Source-only pages can publish definitions, API contracts, and task guidance with
exact citations and explicit boundaries. Do not fill them with untested runnable
recipes. Runtime verification remains necessary for copyable executable examples
and actual integration claims. Existing executable fixtures keep their results;
exhaustive claim-to-snippet coverage and remote CI are tracked in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

## Publication gate

1. List the factual assertions and identify each primary source.
2. Check exact symbols, signatures, defaults, flags, and context restrictions.
3. Write a minimal fixture for executable guidance; validate expected behavior,
   not merely a successful command exit. Test failure behavior where it explains
   an important boundary.
4. Record Bazel, OS/architecture, ruleset versions, resolved dependencies, flags,
   effective rc loading, relevant non-secret environment, commands, output, and
   limitations. Prefer controlled configuration for probes. Keep transient caches
   outside the repo.
5. Review for unsupported generalizations and unintended historical assumptions.
6. Publish the page in the task index only when all its factual claims are sourced
   and its recommended runnable examples pass. Keep unverified research separate.

Do not demand execution for purely definitional claims. Do require execution for
copyable examples and for claims whose practical behavior depends on integration.

## Selecting and refreshing rulesets

Discover the latest stable upstream release and the available non-yanked registry
entry. Record both if they differ, including registry patch versions. Inspect
release notes, exported APIs, module requirements, and the upstream test matrix.
Then run the relevant fixture with the exact Bazel baseline. Passing upstream CI
on a floating `9.x` selector is useful evidence, not proof of a local 9.3.1 run.

Do not downgrade silently to make an example pass. Record a compatibility gap,
fix the integration if justified, or withhold the recommendation. Never label a
candidate version as tested just because it is the newest one found.

## Future automation

The first automation should check evidence metadata, internal links, missing
sources, snippet/fixture drift, and the exact-baseline fixture suite. Add a second
lane for the newly selected stable Bazel release when it differs from the floor.
Ruleset upgrades should update fixture locks and claim evidence in the same change.
No recurring automation or remote workflow is installed. BuildBuddy, CI runners,
claim-to-assertion coverage, and reporting are follow-up work in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1); they are not a
prerequisite for publishing bounded source-reviewed fundamentals now.
