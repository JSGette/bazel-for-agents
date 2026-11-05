---
title: "Test configured providers and registered actions"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {"rules_testing": "0.9.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/providers.md", "actions/declaring-actions.md", "testing/starlark-unit-tests.md"]
claim_ids: ["testing.analysis.entry", "testing.analysis.subjects", "testing.analysis.actions", "testing.analysis.failure", "testing.analysis.config", "testing.analysis.limits"]
last_verified: "2026-11-05"
---

# Test configured providers and registered actions

Use an analysis test to check the configured contract of a rule without relying on
the contents produced by its tool: providers, default outputs, runfiles, selected
inputs, or registered action parameters. Use an
[execution test](execution-tests.md) when file contents or runtime behavior matter.

## Arrange a target, then inspect its analyzed value

In `rules_testing` 0.9.0, load `analysis_test` from
`@rules_testing//lib:analysis_test.bzl`. The function takes a named `target` or
`targets` collection and an `impl` callback. With a single target, the callback
receives `env` and the configured target. [Public export][rt-export],
[implementation][rt-analysis]

A list supplied to `target` creates a label-list attribute; a dictionary creates a
label-keyed dictionary. The separate `targets` parameter creates named target
attributes and passes their values as a struct. Choose the shape that makes the
comparison explicit. [Target construction][rt-analysis]

Our recommendation: arrange minimal helper targets and mark them `manual` so broad
build patterns do not independently attempt to build deliberately invalid or
analysis-only subjects. The framework's `util.helper_target` supports this setup.
[Helper implementation][rt-util]

## Assert the interface a consumer relies on

`env.expect.that_target(target)` provides subjects for default outputs, runfiles,
provider presence, and provider values. Custom provider-specific subject factories
can be passed to `analysis_test`; ordinary provider access is also available in
the callback. [Target subject][rt-target], [factory registration][rt-analysis]

Select a producing action with `action_generating()` using its output's short path,
or use `action_named()` when one action with that mnemonic is expected. These
methods require the framework's testing aspect and reject ambiguous matches.
Deeper dependencies require suitable aspect propagation. [Action selection][rt-target]

An action subject exposes `argv`, `inputs`, `env`, `mnemonic`, and supported
properties such as write content or template substitutions. Built-in actions need
not have an `argv`. Assert a stable semantic contract, such as a required input or
flag, rather than a complete dump of unrelated implementation details.
[Action subject implementation][rt-action]

These assertions inspect registered actions; they do not execute the compiler or
read arbitrary generated file contents. Bazel analysis-test implementations may
not register actions and must report `AnalysisTestResultInfo` instead.
[Bazel analysis-test contract][rule-api]

## Assert expected failures explicitly

`expect_failure = True` configures the subject with
`//command_line_option:allow_analysis_failures`. It enables observing an analysis
failure; it is not a complete assertion by itself. Use the target's `failures()`
subject to verify the intended diagnostic and reject accidental success.
[Configuration][rt-analysis], [failure subject][rt-target]

Do not use this mechanism as a general catch-all for syntax errors, loading
failures, or tool execution failures. Those occur outside the analyzed provider
failure interface; use a [separate invocation](rule-integration-tests.md) for the
appropriate boundary.

## Exercise configurations deliberately

`config_settings` changes settings for the target under test and its dependencies
through an analysis-test transition. Named targets can customize their settings
through the `attrs` template interface. Label-valued settings should be constructed
in the intended repository context rather than left to resolve in the testing
library's context. [Configuration API][rt-analysis]

Bazel limits transitive dependencies for analysis-test targets. Keep arrangements
small and avoid turning an analysis test into an entire product build. The library
also marks its analysis tests incompatible when coverage is enabled, because
coverage can require executing the subject's dependencies. [Bazel contract][rule-api],
[library implementation][rt-analysis]

## Evidence boundary

The APIs below were inspected at the exact releases in the metadata. No new
ruleset integration or test execution is claimed. See the
[claim ledger](../verification/starlark-actions-testing.md) for source identities
and dependency-resolution limitations.

[rt-export]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/analysis_test.bzl
[rt-analysis]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/analysis_test.bzl
[rt-util]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/util.bzl
[rt-target]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/target_subject.bzl
[rt-action]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/action_subject.bzl
[rule-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
