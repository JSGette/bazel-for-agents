---
title: "Model C/C++ target interfaces"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_cc": "0.2.27"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["cc.targets.headers", "cc.targets.dependencies", "cc.targets.flags", "cc.targets.providers"]
last_verified: "2026-11-05"
---

# Model C/C++ target interfaces

Use this when splitting C/C++ code into libraries or fixing accidental dependency
propagation. Our recommendation is to model a library's interface before adding
compiler flags.

## Put files in the attribute matching their role

| Attribute | Contract in rules_cc 0.2.27 |
| --- | --- |
| `srcs` | Implementation sources and private headers. |
| `hdrs` | Published headers available to dependents. |
| `textual_hdrs` | Headers intended for textual inclusion rather than standalone header compilation. |
| `deps` | Dependencies whose compilation interface is available to consumers as well as this target. |
| `implementation_deps` | Dependencies needed by this library's implementation; their headers/include paths are not propagated as part of its public compilation interface, but the libraries still participate in linking. |

[Rule schema and header contract][library]

Keep public headers self-contained with respect to the public dependency
interface. Do not use `implementation_deps` for a library whose headers your
public headers require. This is an interface-design recommendation based on the
propagation boundary above.

## Distinguish include layout from broad compiler options

`strip_include_prefix` removes a prefix from published header paths and
`include_prefix` adds one afterward. `includes` contributes include-search
paths to the target and its dependents. Prefer a deliberate published header
layout over making a large source tree visible with broad include paths.
[Header-path schema][library], [shared attribute schema][attrs]

`copts` affects this target's compilation; `local_defines` also stays local.
`defines` propagates definitions to dependents. Our recommendation is to reserve
propagating options for actual interface requirements, and keep warnings or
implementation tuning local. [Attribute contracts][attrs]

## Preserve semantic providers

`CcInfo` carries `compilation_context` and `linking_context`; default output
files alone do not describe a C++ library's compile/link interface. A custom
code generator or foreign-build adapter must return a meaningful C++ provider
when C++ rules are expected to consume it. [Provider definition][info]

Choose `cc_binary` for an executable and `cc_test` for a test target through
the [public exports](setup.md). See [linking](linking.md) before assuming that a
library's output filenames determine the final binary's linkage.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[library]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_library.bzl
[attrs]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/attrs.bzl
[info]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/cc_info.bzl
