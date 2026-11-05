---
title: "Parse and emit TOML in Starlark"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"toml.bzl": "0.5.0"}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/dialect-and-contexts.md"]
claim_ids: ["toml.api", "toml.errors", "toml.encode", "toml.scope"]
last_verified: "2026-11-05"
---

# Parse and emit TOML in Starlark

Use `toml.bzl` when a repository or module extension needs structured TOML data.
The reviewed release is 0.5.0. Our recommendation is to parse once at the boundary
that owns the input and pass structured values to the rest of the configuration.

## Use the explicit public interface

Load `toml` from `@toml.bzl//:toml.bzl`. The struct exports `decode`, `encode`,
`datetime_to_string`, and constructors for local/offset date and time values.
Temporal values have dedicated structured representations; do not assume every
value returned by decoding is a JSON scalar.
[Public exports][toml-public], [temporal constructors][toml-datetime].

`decode` accepts the TOML string, an optional `default`, an optional
`datetime_formatter`, `max_depth` (128 by default), and `expand_values`.
The last option requests the library's typed test-format representation rather
than ordinary decoded values. [Decoder signature and implementation][toml-decode].

## Make invalid input behavior intentional

With the default `default = None`, parsing errors call `fail`. Supplying a
non-`None` default causes errors to return that default. Passing `None` explicitly
does not enable a nullable fallback. If configuration is required, our
recommendation is to preserve a visible error rather than silently replacing a
broken manifest with an empty dictionary. [Error handling][toml-decode].

Choose an input-size/depth policy appropriate to the repository task. A parser
running during repository/module work adds work there; it is not a cacheable
ordinary build action simply because it is called from a `.bzl` file. See
[phases](../../core/phases-and-graphs.md) and use a declared execution action when
that is the intended stage.

## Emit structured output deliberately

`encode` requires a dictionary at the root. It accepts `max_tables`, defaulting
to 1,000,000, and fails on unsupported scalar values or exhausted structural
limits. Review the encoded output as generated data, without assuming preservation
of comments, original formatting, or lexical spelling from an input file.
[Encoder][toml-encode].

For repository rules, separate obtaining/watching the source file from parsing
its text; parsing is not a substitute for declaring the repository's inputs.
This is an architectural recommendation, not an additional filesystem capability
of the TOML library.

The release declares a pinned external TOML test suite. It was inspected but not
executed here. This page makes no local conformance or performance claim.
[Test dependency declaration][toml-module].

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[toml-public]: https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml.bzl
[toml-decode]: https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/decode.bzl
[toml-encode]: https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/encode.bzl
[toml-datetime]: https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/datetime.bzl
[toml-module]: https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/MODULE.bazel
