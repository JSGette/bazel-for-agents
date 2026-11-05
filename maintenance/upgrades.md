# Refresh reference versions deliberately

This is the repository's maintenance procedure. Version discovery, source review,
and integration validation are separate steps; changing a version string does
not complete an upgrade.

## Establish identities

1. Discover the current stable upstream release and non-yanked registry entry.
   Record differences, including registry patches and prereleases excluded from
   selection. Keep an observation date and immutable source identity.
2. For Bazel, record the release commit and official binary checksum. Update the
   exact reference only after reviewing the relevant API and behavior changes.
3. For a ruleset, inspect its registry `source.json`, archive integrity, patches,
   module manifest, exported `.bzl` APIs, toolchain setup, and tests. A ruleset's
   release number is not its compiler, interpreter, SDK, or dependency-lock version.
4. For REAPI, record protocol identity separately from the Bazel client range,
   requested features, server capabilities, and interoperability results.

See [version metadata](../versions/baseline.json),
[ruleset identities](../versions/rulesets.json), and
[protocol boundaries](../remote/capabilities-and-versions.md).

## Review affected guidance

Find pages using the changed module/API and their claim records. Check exported
load labels, extension symbols and attributes, defaults, provider contracts,
configuration behavior, and release-specific restrictions. Prefer implementation
and tests when prose conflicts with them. Update adjacent task routes when a
public entry point changes; do not leave two incompatible setup paths unlabeled.

Retain exact versions on unaffected pages. Evidence at one release does not
prove a whole version range. Keep the currently verified reference available
until a replacement has its own evidence; do not silently downgrade a dependency
to make a sample pass.

## Validate the actual claim

For source-only guidance, record what changed and the inspected source. For an
executable example, run its behavioral assertions at the exact selected Bazel
version and capture the resolved dependency graph, flags, configuration, platform,
and result. Upstream CI using a floating selector is supporting evidence, not a
substitute for that exact run. A passing build does not alone establish output
contents, runtime compatibility, performance, or reproducibility.

Update documentation, version metadata, fixtures/locks where applicable, and
verification records together. Report untested integration or platform gaps
explicitly. The [verification policy](verification.md) defines the publication
boundary; automated orchestration is tracked in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
