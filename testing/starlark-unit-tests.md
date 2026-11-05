---
title: "Test pure Starlark helpers"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {"rules_testing": "0.9.0", "bazel_skylib": "1.9.2"}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/dialect-and-contexts.md", "starlark/mutability-and-freezing.md"]
claim_ids: ["testing.unit.scope", "testing.unit.suite", "testing.unit.assertions", "testing.unit.skylib"]
last_verified: "2026-11-05"
---

# Test pure Starlark helpers

Use a unit test for a helper whose contract can be checked from ordinary Starlark
values: argument normalization, label transformations with an explicit context,
collection operations, or string construction. Use an
[analysis test](analysis-tests.md) for configured targets, providers, and actions.

## Choose the testing API already used by the project

For new rule libraries using `rules_testing` 0.9.0, the public entry points are
`@rules_testing//lib:unit_test.bzl` and
`@rules_testing//lib:test_suite.bzl`. `unit_test` accepts `name`, `impl`, and
optional `attrs`. Its implementation wraps the analysis-test machinery with a stub
target; “unit” describes the subject under test, not a separate Starlark
interpreter outside Bazel. [Unit-test implementation][rt-unit]

`test_suite` has the following interface at this release: [Source][rt-suite]

| Parameter | What belongs there |
| --- | --- |
| `tests` | Setup functions that accept `name` and create the named test target. |
| `basic_tests` | Assertion functions that receive a single `env` argument. |
| `test_kwargs` | Extra keyword arguments passed through to setup/unit-test creation. |

The suite creates the tests and a `native.test_suite` collecting them. There is no
`custom_tests` parameter in this release's implementation; a copied documentation
example using that spelling is not an alternative API. Use `tests` for custom
setup functions. [Source][rt-suite]

The callback's `env.expect` supplies assertion subjects, while `env.fail()` records
a failure for reporting. Prefer the assertion framework over an unconditional
`fail()` when you want several contract failures reported together.
[Environment and result construction][rt-analysis], [assertion subjects][rt-expect]

## Keep pure-helper assertions about observable behavior

Our recommendation: test empty input, repeated values, relevant ordering,
normalization, and boundary cases that could change the helper's result. Assert
the returned value or precise rejection behavior, not the helper's incidental
choice of intermediate list or loop.

Do not mutate imported constants to arrange a test. Make test input values fresh
and explicit; the [freezing rules](../starlark/mutability-and-freezing.md) also apply
to test code. Keep a pure-helper test independent of a real compiler or SDK unless
that external component is part of the behavior being tested.

For malformed input that intentionally calls Starlark `fail()`, choose a harness
that can observe the failing phase. `env.fail()` records assertion failures; it is
not an exception-catching construct for arbitrary helper evaluation. The
[rule integration](rule-integration-tests.md) page describes when a separate
Bazel invocation is the appropriate boundary. [Assertion environment][rt-analysis]

## Keep Skylib's API distinct

`bazel_skylib` 1.9.2 also exposes `unittest` and `asserts` from
`@bazel_skylib//lib:unittest.bzl`. Its `unittest.make`, `suite`, `begin`, and `end`
workflow is a separate API. Do not combine a Skylib test environment with
`rules_testing` method names merely because both test Starlark.
[Skylib exports and implementations][sk-unit]

Our recommendation: follow the repository's chosen framework unless changing it
is part of the task. Neither source inspection here nor the registry version
inventory is an executed compatibility result for the project's module graph.

## Evidence boundary

The APIs below were inspected at the exact releases in the metadata. No new
ruleset integration or test execution is claimed. See the
[claim ledger](../verification/starlark-actions-testing.md) for source identities
and dependency-resolution limitations.

[rt-unit]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/unit_test.bzl
[rt-suite]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/test_suite.bzl
[rt-analysis]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/analysis_test.bzl
[rt-expect]: https://github.com/bazelbuild/rules_testing/blob/db007bfee840cebcb6f955b80973ba866de38947/lib/private/expect.bzl
[sk-unit]: https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/unittest.bzl
