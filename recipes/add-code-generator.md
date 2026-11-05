---
title: "Add a code generator"
status: "source-verified"
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/providers.md", "toolchains/consuming.md", "actions/inputs-tools-environment.md", "diagnostics/aquery.md"]
claim_ids: []
last_verified: "2026-11-05"
---

# Add a code generator

This is a task checklist and reading path. Follow the exact version and evidence
boundaries in the linked pages; this page adds no independently verified API
claims and is not a runnable integration fixture.

## 1. Define the generated API

Decide which artifact(s) the consumer needs and how dependencies discover them. Use a custom provider for the semantic interface, `DefaultInfo` for requested defaults, and output groups for optional products.

Read [providers](../core/providers.md) and
[declaring actions](../actions/declaring-actions.md).

## 2. Separate generator and generated target

Model the generator as a tool that runs on the execution platform. Its output may be consumed by a rule for a different target platform. Select the tool through the appropriate declared toolchain or exec-configured dependency.

Read [consuming](../toolchains/consuming.md) and
[cross compilation](../toolchains/cross-compilation.md).

## 3. Declare the complete action

Declare source inputs, tool runtime files, outputs, arguments, and environment. Use structured arguments and the tool’s supported parameter-file format. A path in an argument alone does not declare a file dependency.

Read [inputs tools environment](../actions/inputs-tools-environment.md) and
[arguments and param files](../actions/arguments-and-param-files.md).

## 4. Expose and inspect the result

Return the intended providers, build the requested output, and inspect the resulting action. Add an execution assertion for generated contents and analysis assertions for provider/action contracts where appropriate.

Read [aquery](../diagnostics/aquery.md) and
[analysis tests](../testing/analysis-tests.md).

## Completion evidence

Record the source change, selected dependency graph, Bazel version, relevant
platforms and flags, and the assertions actually observed. Preserve gaps rather
than inferring a wider compatibility result. Executable recipe coverage and CI
are follow-up work in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
