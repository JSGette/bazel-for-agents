---
title: "Use regex in Starlark deliberately"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"re.bzl": "0.4.1"}
platforms_verified: []
required_flags: []
prerequisites: ["starlark/dialect-and-contexts.md"]
claim_ids: ["regex.api", "regex.syntax", "regex.anchors", "regex.reuse"]
last_verified: "2026-11-05"
---

# Use regex in Starlark deliberately

`re.bzl` is a regex library. It is unrelated to remote execution or REAPI. Our
recommendation is to prefer ordinary string operations for simple matching and
introduce regex when the pattern is clearer and bounded.

## Load the public API

Load `re` from `@re.bzl//:re.bzl`. The exported struct provides `compile`,
`search`, `match`, `fullmatch`, `findall`, `finditer`, `split`, `sub`, and flag
constants. `search` scans for a match; `match` starts at the supplied position;
`fullmatch` requires the entire selected range to match.
[Public exports][regex-public], [implementation][regex-core].

`compile` creates a reusable object with `search`, `match`, and `fullmatch`
methods. Successful matches expose group and span operations; unsuccessful
matches return `None`. Reuse a compiled pattern for repeated checks rather than
rebuilding it at each call. [Compile and match APIs][regex-core].

## Verify the exact syntax and anchor behavior

The library implements a subset of RE2-style syntax with a Python-like API. It
is not a drop-in implementation of Python's `re`; backreferences and lookarounds
are not supported. Read the pinned syntax and compiler behavior for the pattern
you actually need. [Syntax scope][regex-readme], [compiler][regex-compiler].

In particular, `$` matches the end of text, not the position before a final
newline, unless multiline mode supplies line-anchor behavior. The upstream
anchor tests cover these distinctions. Use `fullmatch` for whole-value validation
when that expresses the requirement more directly. [Anchor tests][regex-anchors].

Our recommendation is to add focused assertions for empty input, newlines,
escaping, optional groups, and relevant Unicode strings before depending on a
pattern. Do not assume byte, code-point, or grapheme semantics from a Python test.

## Keep work in the appropriate build phase

This API operates on supplied strings. It does not supply filesystem reads or
run a process. Use the file-context capabilities described in
[dialect and contexts](../../starlark/dialect-and-contexts.md) to obtain data, or
use a declared action when parsing belongs to build execution.
[Pure Starlark API][regex-core].

No throughput or complexity benchmark was run for this page. Do not turn the
upstream README's performance description into a measured property of this
reference or of a project's configuration workload.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[regex-public]: https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re.bzl
[regex-core]: https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/private/re.bzl
[regex-readme]: https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/README.md
[regex-anchors]: https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/tests/test_anchors.bzl
[regex-compiler]: https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/private/compiler.bzl
