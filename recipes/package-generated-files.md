---
title: "Package generated files"
status: "source-verified"
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/outputs-and-runfiles.md", "rulesets/packaging/file-mappings.md", "rulesets/packaging/archives.md", "testing/execution-tests.md"]
claim_ids: []
last_verified: "2026-11-05"
---

# Package generated files

This is a task checklist and reading path. Follow the exact version and evidence
boundaries in the linked pages; this page adds no independently verified API
claims and is not a runnable integration fixture.

## 1. Choose the consumer contract

Request generated outputs through providers or the target’s explicit output contract. Avoid scanning the output tree for filenames whose production has not been declared.

Read [outputs and runfiles](../core/outputs-and-runfiles.md) and
[file mappings](../rulesets/packaging/file-mappings.md).

## 2. Define destination paths

Use file mappings to define install paths and layout independently of source paths. Specify meaningful ownership, modes, and timestamp policy for the chosen package format.

Read [file mappings](../rulesets/packaging/file-mappings.md) and
[metadata](../rulesets/packaging/metadata.md).

## 3. Choose archive composition rules

Select tar, zip, or a system-package rule. Distinguish embedding an archive as a file from unpacking dependency archives into a result, and decide how duplicate paths should fail.

Read [archives](../rulesets/packaging/archives.md) and
[metadata](../rulesets/packaging/metadata.md).

## 4. Check the artifact contract

Assert archive member paths, contents, permissions, and relevant format metadata. Check repeatability under controlled inputs if reproducibility is part of the promise; the existence of an archive alone is insufficient evidence.

Read [execution tests](../testing/execution-tests.md) and
[hermeticity and reproducibility](../actions/hermeticity-and-reproducibility.md).

## Completion evidence

Record the source change, selected dependency graph, Bazel version, relevant
platforms and flags, and the assertions actually observed. Preserve gaps rather
than inferring a wider compatibility result. Executable recipe coverage and CI
are follow-up work in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
