---
title: "Represent Apple OS, architecture, and environment separately"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"apple_support": "2.11.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["apple.platform.constraints", "apple.platform.xcode", "apple.platform.actions"]
last_verified: "2026-11-05"
---

# Represent Apple OS, architecture, and environment separately

Use this when the right CPU still produces the wrong Apple binary, or when an
Apple action can execute locally but not on a selected worker.

## Model the destination environment

The ruleset provides public definitions in `@apple_support//platforms` and
`@apple_support//constraints`. Its rule-author helpers distinguish target OS,
architecture, and `device` versus `simulator`. macOS uses the `device` environment
in this model. CPU alone is insufficient to identify these destinations.
[Platform definitions][platforms], [constraints][constraints], [helper logic][helpers]

`platform_constraint_attrs()` supplies attributes for these checks, and
`platform_info_from_rule_ctx()` combines them. The OS helper recognizes iOS,
macOS, tvOS, visionOS, and watchOS. The architecture helper additionally handles
pointer-authentication constraints when identifying arm64e.
[Constraint inspection][helpers]

Our recommendation is to use the provided platform vocabulary consistently
through custom rules and native dependencies. Do not infer simulator/device
from the machine running Bazel, or substitute an OS/CPU-only platform for a
platform whose environment constraints are meaningful.

## Keep SDK selection and worker availability distinct

The Xcode configuration rule can describe available local and remote Xcode
versions and select a mutually available version. These are declarations about
available installations; they do not install an SDK on an executor.
[Xcode selection implementation][xcode]

The `apple_support` action helpers add the selected configuration's execution
information and SDK/Xcode environment to the action. An execution platform must
still provide those tools. Inspect both the selected target platform and the
action's execution requirements when debugging remote failures.
[Action environment and execution requirements][helpers]

Minimum deployment OS, SDK version, and selected Xcode version are distinct
inputs to the configuration. Record them separately in future integration
coverage. A successful compile does not validate application signing,
packaging, deployment, or execution on a device.

Return to [setup](setup.md) for toolchain registration and helper APIs.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[helpers]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/lib/apple_support.bzl
[platforms]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/platforms/BUILD
[constraints]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/constraints/BUILD
[xcode]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/xcode/xcode_config.bzl
