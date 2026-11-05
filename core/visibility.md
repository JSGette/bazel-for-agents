---
title: "Choose who can depend on targets and load build logic"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: ["linux-x86_64"]
required_flags: []
prerequisites: ["core/labels-and-targets.md"]
claim_ids:
  - core.visibility.target
  - core.visibility.specifications
  - core.visibility.defaults
  - core.visibility.load
  - core.visibility.load-default
  - core.visibility.independent
  - core.visibility.macro-location
last_verified: "2026-11-05"
---

# Choose who can depend on targets and load build logic

## Use this when

Define a package's supported interface or diagnose a visibility failure. This
page covers direct target declarations and `.bzl` loading; symbolic macros have
an additional declaration-location rule described below.

## Choose the boundary

Bazel has two separate checks. **Target visibility** controls dependency edges
to targets, such as labels in `deps` or `srcs`; a forbidden edge fails analysis.
**Load visibility** controls which packages can load a `.bzl` file. Granting one
does not grant the other. [Evidence: target, load, independent](../verification/core-visibility.md#claims).

Our recommendation: keep implementation targets private and grant access to
the packages that use the supported interface. When access fails, first identify
which check rejected the request and whether that dependency belongs in the
interface. Do not widen unrelated targets merely to make a build pass.

## Set target visibility

For targets declared directly in a `BUILD.bazel` file, use the rule's
`visibility` attribute to grant access beyond its own package:

| Entry in the attribute | Additional permitted users |
| --- | --- |
| `//visibility:private` | None; targets in the declaring package retain access. |
| `//client:__pkg__` | Targets in `//client`, excluding its subpackages. |
| `//client:__subpackages__` | Targets in `//client` and its subpackages. |
| A `package_group` label | Targets in the packages selected by that group. |
| `//visibility:public` | Targets in every package. |

If a direct rule declaration omits visibility, its package's `default_visibility`
applies; without that setting it defaults to private. This default rule does not
describe targets created inside symbolic macros. [Evidence: specifications and defaults](../verification/core-visibility.md#claims).

Our recommendation: use an explicit public declaration only for an intended
public interface. Reuse a `package_group` when several targets share the same
access list.

## Set `.bzl` load visibility

Call `visibility()` at the top level of the `.bzl` file, once, after its `load()`
statements. The declaration takes package specifications, such as `//client` or
`//client/...`; these are different from target-visibility entries. Negative
package specifications and `package_group` labels are not supported here.
[Evidence: load](../verification/core-visibility.md#claims).

A `.bzl` file without a declaration is public for loading. Our recommendation:
declare the intended scope explicitly for internal build logic.
[Evidence: load-default](../verification/core-visibility.md#claims).

Setting target visibility on the `.bzl` file through `exports_files` controls
whether other targets may consume it as a source file. It does not set load
visibility. [Evidence: independent](../verification/core-visibility.md#claims).

## Follow the tested example

The [visibility fixture](../examples/visibility/) separates the two boundaries:

- [lib/BUILD.bazel](../examples/visibility/lib/BUILD.bazel) exposes `//lib:shared`
  only to `//allowed` and exposes `restricted.bzl` as a source file publicly.
- [lib/restricted.bzl](../examples/visibility/lib/restricted.bzl) allows loading
  from `//allowed`, in addition to its own package.
- [allowed/BUILD.bazel](../examples/visibility/allowed/BUILD.bazel) successfully
  loads the helper and depends on the shared target.
- [denied/BUILD.bazel](../examples/visibility/denied/BUILD.bazel) contains an
  intentionally rejected dependency. The separate
  [negative-load module](../examples/visibility/negative-load/) demonstrates a
  rejected load even though the `.bzl` source target is public.

Run the exact commands in the [verification record](../verification/core-visibility.md#execution).
The permitted build passed; both forbidden cases failed with visibility errors.
The checks ran with rc files disabled and no visibility-disabling flags.

## Boundary: symbolic macros

A target created by a symbolic macro uses the innermost macro definition's
package as its declaration location for visibility; its label's package alone
does not describe access. Forwarding the macro implementation's `visibility`
parameter is the documented way to export a target to the macro's caller.
This paragraph is source-verified; the fixture uses direct rule declarations
and does not test macro visibility delegation. [Evidence: macro-location](../verification/core-visibility.md#claims).

For the label and package model, read [labels and targets](labels-and-targets.md).
For dependency attributes, read [the rule contract](rule-contract.md).
