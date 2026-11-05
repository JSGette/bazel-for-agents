---
title: "Define typed loading-time APIs with symbolic macros"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/visibility.md", "starlark/dialect-and-contexts.md"]
claim_ids: ["starlark.macro.availability", "starlark.macro.attributes", "starlark.macro.configurable", "starlark.macro.naming", "starlark.macro.restrictions", "starlark.macro.visibility", "starlark.macro.finalizers", "starlark.macro.evaluation"]
last_verified: "2026-11-05"
---

# Define typed loading-time APIs with symbolic macros

Use a symbolic macro to expose a typed, reusable interface that instantiates rules
or other macros during package loading. Use a [rule](../core/rule-contract.md) when
you need configured dependencies, providers, or action registration.

## Define the public interface

Define the macro with `macro()` in a `.bzl` file and bind it to an exported global
name before instantiating it. In Bazel 9.3.1,
`--experimental_enable_first_class_macros` defaults to `true`; its explicit
configuration can still disable the construct. [Definition and call checks][rule-functions],
[option default][language-options]

Declare attributes with `attr` types. `name` and `visibility` are implicit and must
be accepted by the implementation; do not redeclare them in `attrs`. Label-valued
arguments convert strings relative to the macro call site. The implementation
creates targets; it does not return an analysis result. [API model][macro-guide],
[implementation][macro]

`inherit_attrs` accepts a rule or macro symbol, or `"common"` for common rule
attributes. Only public attributes are inherited. Explicit `attrs` entries
override inherited entries, and an entry set to `None` removes an inherited
attribute. Non-mandatory inherited attributes default to `None`, so normalize that
case before adding values. An implementation inheriting attributes must accept
`**kwargs`. [Attribute inheritance][macro-guide], [construction][rule-functions]

## Treat configurable values as selectors

A configurable attribute's non-`None` value is presented as a selector even when
the caller supplied a literal. Forward it to an inner rule, or use operations
supported by selectors. Do not inspect it as though a target configuration had
already selected a branch. Use `configurable = False` for attributes that control
loading-time structure and must reject `select()`. [Conversion][macro],
[select semantics][macro-guide]

Our recommendation: keep the macro's structural choices small and explicit.
Resolve configuration-dependent implementation choices in a rule rather than
attempting to evaluate a selector inside a macro.

## Name and expose targets deliberately

Created targets and submacros must use the macro's own name or that name followed
by `_`, `.`, or `-` and a suffix. A declaration violating this schema can exist but
cannot be built or used as a dependency. Prefer `_` for predictable names and avoid
collisions with unrelated package targets. [Naming contract][macro-guide]

Forward the macro's `visibility` to targets that form its public interface.
Targets without forwarded visibility are internal to the macro; the caller's
package default visibility does not automatically export them. Macro visibility
is checked with respect to the definition context, with specific delegation rules
for passed dependencies. Follow [visibility](../core/visibility.md), rather than
assuming that every generated target belongs to the caller's access scope.
[Visibility semantics][macro-guide]

## Respect loading-time restrictions

Symbolic macros cannot mutate their arguments, return a value, call `glob()` or
`native.package()`, or call `native.existing_rules()` as ordinary macros. Pass
explicit input labels into the macro; expand a package glob at the call site if
needed. [Restrictions][macro-guide], [evaluation context][macro]

A `finalizer = True` macro runs after non-finalizer targets have been defined and
may inspect `native.existing_rules()`. That view contains non-finalizer rules;
introspection does not bypass dependency visibility. A non-finalizer symbolic
macro cannot instantiate a finalizer. Reserve finalizers for package-wide tasks
that actually require that later view. [Finalizers][macro-guide], [call guard][rule-functions]

Do not promise that symbolic macros make a package demand-lazy. The 9.3.1
implementation still includes eager ordinary-macro expansion and separately
defers finalizers; the release guide explicitly describes demand-driven lazy
expansion as unavailable. Choose symbolic macros for their interface and
encapsulation, not an unmeasured performance claim. [Implementation][rule-functions],
[release guide][macro-guide]

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[rule-functions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java
[language-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java
[macro-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/macros.md
[macro]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/MacroClass.java
