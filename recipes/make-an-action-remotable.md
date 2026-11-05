---
title: "Make an action suitable for remote execution"
status: "source-verified"
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["diagnostics/aquery.md", "actions/hermeticity-and-reproducibility.md", "remote/capabilities-and-versions.md", "remote/execution.md"]
claim_ids: []
last_verified: "2026-11-05"
---

# Make an action suitable for remote execution

This is a task checklist and reading path. Follow the exact version and evidence
boundaries in the linked pages; this page adds no independently verified API
claims and is not a runnable integration fixture.

## 1. Inspect the existing action

Start with the analyzed executable, arguments, inputs, outputs, environment, and execution requirements. Identify machine-local paths and tools that are not represented by the declared contract.

Read [aquery](../diagnostics/aquery.md) and
[inputs tools environment](../actions/inputs-tools-environment.md).

## 2. Close the execution environment

Supply required tools and runtime files, select an appropriate execution platform, and document any intentional worker-image dependency. Match Bazel constraints to the service’s actual property contract.

Read [hermeticity and reproducibility](../actions/hermeticity-and-reproducibility.md) and
[platforms and properties](../remote/platforms-and-properties.md).

## 3. Check the service contract

Verify endpoint/instance configuration, capabilities, digest/compression support, and permissions. Keep the protocol reference separate from the capabilities of the exact Bazel client and server.

Read [capabilities and versions](../remote/capabilities-and-versions.md) and
[digests and transfers](../remote/digests-and-transfers.md).

## 4. Record actual execution evidence

Compare output assertions locally and remotely with controlled configuration. Distinguish remote execution from cached results and fallback, and verify local output availability for downstream consumers. This checklist does not itself establish remote compatibility.

Read [execution](../remote/execution.md) and
[outputs and downloads](../remote/outputs-and-downloads.md).

## Completion evidence

Record the source change, selected dependency graph, Bazel version, relevant
platforms and flags, and the assertions actually observed. Preserve gaps rather
than inferring a wider compatibility result. Executable recipe coverage and CI
are follow-up work in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
