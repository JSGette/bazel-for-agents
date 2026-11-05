# Using Bazel for Agents

This repository curates guidance for Bazel 9.3.1 and newer. Read this file and
`README.md` first, then load only the pages relevant to the current task.

## Using the guidance in another project

1. Inspect the project's Bazel version, module manifest, resolved dependencies,
   configuration, and local agent instructions before choosing guidance.
2. Read `versions/baseline.json`. Match the page's exact Bazel, ruleset, flags,
   and platform coverage to the project. A newer version is not automatically
   covered by evidence for an older version.
3. Use the task index in `README.md`. Follow a page's prerequisites only as
   needed; do not ingest the entire repository as context.
4. Use only verified statements as implementation guidance. A proposed topic
   is a writing plan. A source-verified example has not necessarily been run.
5. Use modern module-based setup. Do not supply WORKSPACE setup, migration
   recipes, compatibility shims for older Bazel releases, or historical examples.
6. When local requirements differ from a page's evidence, state the mismatch
   and verify the relevant behavior. Do not silently upgrade the project or
   invent a fallback based on remembered older Bazel behavior.
7. Preserve project conventions where compatible with the task. This reference
   does not authorize dependency upgrades or unrelated build rewrites.

## Contributing guidance

- Follow `maintenance/verification.md` and `templates/topic.md`.
- Keep each page focused on one decision or task. Give the preferred working
  pattern first, its boundaries second, and primary evidence beside the claims.
- Distinguish Bazel semantics, ruleset APIs, and this repository's recommendations.
- Prefer exact release source and tests. Resolve contradictory documentation
  against implementation and executable probes; do not copy upstream examples
  indiscriminately.
- Every factual claim needs evidence at the declared baseline. Every recommended
  executable example needs a fixture, command, observed result, and environment.
- Record latest stable releases separately from tested selections. Exclude
  prereleases and yanked versions from default recommendations.
- For ruleset source reviews, an exact exported API is evidence about that
  release, not a tested dependency graph. Read the page's verification boundary
  before choosing versions or claiming platform compatibility.
- Never describe a flag as unnecessary, stable, enabled, or removed without
  checking the pinned version's implementation or command help.
- Keep missing verification explicit. Do not turn an untested claim into a
  recommendation to make a page appear complete.
- Keep the content generic: no organization-specific names, repository layouts,
  private endpoints, build wrappers, or internal conventions.

`README.md` indexes the published guidance; `docs/structure.md` describes its
scope. Executable coverage and BuildBuddy integration are follow-up work in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1). Source-only guidance
is explicitly marked; do not treat it as a passing integration test.
