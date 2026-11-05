---
title: "Apply scoped configuration with with_cfg.bzl"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"with_cfg.bzl": "1.0.2"}
platforms_verified: []
required_flags: []
prerequisites: []
claim_ids: ["withcfg.api", "withcfg.builder", "withcfg.reset", "withcfg.providers"]
last_verified: "2026-11-05"
---

# Apply scoped configuration with with_cfg.bzl

Use this when a project deliberately wants a variant of a rule built with
specific flags or build settings. The reviewed release is 1.0.2. Our
recommendation is to prefer an ordinary rule attribute when one expresses the
requirement, and use a configuration wrapper when the dependency configuration
must actually change.

## Build the wrapper from the public API

Load `with_cfg` and, when needed, `original_settings` from
`@with_cfg.bzl//:with_cfg.bzl`. `with_cfg` accepts a rule or macro and returns a
builder. [Public export][cfg-public], [builder][cfg-builder].

| Builder operation | Meaning |
| --- | --- |
| `set(setting, value)` | Set a native flag named by a string, or a build setting identified by a `Label`. |
| `extend(setting, value)` | Append list entries unless they are already a suffix. |
| `build()` | Return the wrapper macro and its supporting/reset rule. |
| `clone()` | Create an independently editable builder; reset configuration is not copied. |

Assign the two results of `build()` to names in the defining `.bzl` file. The
supporting rule must have a module-global name; its name is observable in queries
even when it is private.
A builder cannot be modified normally after building it; use `clone` when making
another variant. [Builder contract][cfg-builder].

## Account for dependency scope

The wrapper applies its settings to the target and its transitive dependencies.
It does not mean “change only this command's display name.” Use
`resettable(original_settings_label)` when selected edges should return to their
original settings, and `reset_on_attrs` for automatic reset on named dependency
attributes. The corresponding `original_settings` target is part of that setup.
[Scope and reset API][cfg-builder].

Our recommendation is to inspect the configured dependency graph and test an
actual consumer before introducing a wrapper broadly. Configuration changes can
produce additional configured instances; a wrapper's compact syntax does not
remove the need to understand transitions.

## Preserve the consumer's provider interface

The wrapper forwards a defined set of providers. `extra_providers` allows
additional custom providers to be forwarded. Do not assume an arbitrary rule's
complete custom interface survives wrapping automatically. Check executable/test
classification and implicit targets as well as providers.
[Builder arguments][cfg-builder], [provider policy][cfg-providers].

The library accepts rules and macros, but that is not a promise that every
third-party macro's generated targets, aspects, or custom provider contract has
been tested here. Keep the wrapper local to the intended build variant and verify
both the changed branch and any reset branches.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[cfg-public]: https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg.bzl
[cfg-builder]: https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/with_cfg.bzl
[cfg-providers]: https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/rule_defaults.bzl
