---
title: "Choose the correct Starlark evaluation context"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/phases-and-graphs.md"]
claim_ids: ["starlark.context.build", "starlark.context.bzl", "starlark.context.module", "starlark.syntax.import", "starlark.syntax.control", "starlark.numeric.int", "starlark.numeric.float"]
last_verified: "2026-11-05"
---

# Choose the correct Starlark evaluation context

## Use this when

Choose where to put build declarations or reusable logic, or diagnose syntax that
looks like Python but fails in Bazel. This page covers the Bazel 9.3.1 dialect and
file contexts; it is not a complete language reference.

## Put declarations and logic in their appropriate files

| Context | Purpose and relevant boundary | Evidence |
| --- | --- | --- |
| `MODULE.bazel` | Declare the module and its direct module dependencies. It does not accept `load()` statements or function definitions. | [Module context][module] |
| `BUILD.bazel` | Declare package targets by calling rules or loaded macros. Function definitions and `for`/`if` statements are rejected; comprehensions and conditional expressions are permitted. | [BUILD context][build] |
| `.bzl` top level | Define reusable functions, rules, providers, and constants; load exported symbols from other `.bzl` files. Top-level `for`/`if` statements are rejected. | [Extension context][bzl] |
| A rule implementation in `.bzl` | Execute analysis logic with its `ctx` argument and register actions through `ctx.actions`. It is invoked during analysis, not while declaring the rule's target in `BUILD.bazel`. | [Rule contract](../core/rule-contract.md) |

Our recommendation: keep target declarations readable, move reusable computation
into `.bzl` functions, and keep module dependency declarations in `MODULE.bazel`.
Do not copy an expression into another file context merely because both accept
Starlark syntax.

`load()` imports named symbols from a `.bzl` file identified by a label. Its
arguments are string literals and the statement must be at file top level.
Symbols whose names start with `_` cannot be loaded from another file.
[Evidence][bzl]

## Use Starlark syntax explicitly

Bazel's parser rejects Python `import`, `class`, `while`, `try`, and `raise`.
For supported extension imports, use `load()`; report a rule validation error
with `fail()`. The parser's diagnostics explicitly direct users to `load()` and
`fail()` for the relevant unsupported constructs. [Evidence][syntax]

Within `.bzl` functions, `for` and `if` statements are available; their top-level
restriction is checked separately. This is why a loop can belong in a helper
function while the same statement is rejected at file top level. [Evidence][control]

Do not infer the current language from older summaries. At this exact baseline:

- Integers support arbitrary magnitude and exact arithmetic. [Evidence][int]
- Floating-point values and the `float()` built-in exist. [Evidence][float]
- The core `set()` type is enabled by default; its flag and collection boundaries
  are covered in [collections](collections.md).

These language capabilities do not imply that every Bazel attribute accepts each
type. Check the selected rule's attribute contract before passing a value.
See [rule attributes](../core/rule-contract.md).

## Minimal verified example

The [set fixture](../examples/starlark-set/) separates the three file roles:
`MODULE.bazel` declares the module, `BUILD.bazel` loads and instantiates a rule,
and `probe.bzl` defines the implementation. The implementation performs set
operations and registers a file-writing action.

The [execution record](../verification/starlark-basics.md#executed-fixture)
contains the exact command and the resulting four-line file. It exercises this
particular `.bzl`/BUILD/module arrangement. The rejected constructs and numeric
semantics above were checked in source, not individually runtime-tested here.

## Evidence and next task

All source evidence is pinned to the Bazel 9.3.1 release commit. The
[claim ledger](../verification/starlark-basics.md) distinguishes source inspection
from execution. Continue to [collection selection](collections.md) or the
[rule contract](../core/rule-contract.md).

[build]: ../verification/starlark-basics.md#starlarkcontextbuild
[bzl]: ../verification/starlark-basics.md#starlarkcontextbzl
[module]: ../verification/starlark-basics.md#starlarkcontextmodule
[syntax]: ../verification/starlark-basics.md#starlarksyntaximport
[control]: ../verification/starlark-basics.md#starlarksyntaxcontrol
[int]: ../verification/starlark-basics.md#starlarknumericint
[float]: ../verification/starlark-basics.md#starlarknumericfloat
