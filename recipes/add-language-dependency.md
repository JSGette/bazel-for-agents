---
title: "Add a language dependency"
status: "source-verified"
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["modules/dependencies-and-version-selection.md", "rulesets/go/dependencies.md", "diagnostics/module-resolution.md", "modules/lockfile-and-vendor.md"]
claim_ids: []
last_verified: "2026-11-05"
---

# Add a language dependency

This is a task checklist and reading path. Follow the exact version and evidence
boundaries in the linked pages; this page adds no independently verified API
claims and is not a runnable integration fixture.

## 1. Identify the resolver

Distinguish a Bazel module from a Go module, Python distribution, or Rust crate. Read the selected ruleset’s dependency API before editing a manifest; these resolvers do different work.

Read [dependencies and version selection](../modules/dependencies-and-version-selection.md) and
[README](../rulesets/README.md).

## 2. Use the correct language integration

For Go, follow the selected Go/Gazelle module integration. For Python, choose the pip hub and lock format supported by the exact rules release. For Rust, choose rules_rs or direct rules_rust first and keep its generated repository API consistent.

Read [dependencies](../rulesets/go/dependencies.md) and
[dependencies](../rulesets/python/dependencies.md).

## 3. Inspect selection and imports

Check the selected Bazel graph, extension-generated repositories, and apparent repository names. Review language lock changes and module lock changes separately. Native dependencies also need the intended execution/target compiler contract.

Read [module resolution](../diagnostics/module-resolution.md) and
[dependencies](../rulesets/rust/dependencies.md).

## 4. Connect a narrow consumer

Add the dependency to the target that directly uses its exported API. Verify the intended target and relevant tests, then record the resolved graph and platform before describing the combination as tested.

Read [lockfile and vendor](../modules/lockfile-and-vendor.md) and
[rule integration tests](../testing/rule-integration-tests.md).

## Completion evidence

Record the source change, selected dependency graph, Bazel version, relevant
platforms and flags, and the assertions actually observed. Preserve gaps rather
than inferring a wider compatibility result. Executable recipe coverage and CI
are follow-up work in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
