---
title: "Use Apple support and Xcode-backed C++ toolchains"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"apple_support": "2.11.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["apple.setup.scope", "apple.setup.module", "apple.setup.actions"]
last_verified: "2026-11-05"
---

# Use Apple support and Xcode-backed C++ toolchains

Use this when building native code against Xcode or writing an Apple-specific
build action. `apple_support` 2.11.0 supplies Apple C++ toolchains, platform and
constraint definitions, and rule-author helpers. Its own overview directs Apple
application bundling to `rules_apple` and Swift compilation to `rules_swift`;
those distinct rulesets are outside this page's version review. [Scope][readme]

## Understand module-provided setup

The module invokes `apple_cc_configure_extension`, imports the generated
`local_config_apple_cc` and `local_config_apple_cc_toolchains` repositories,
and registers the latter's toolchains. It also invokes the Xcode configuration
extension. These paths discover/configure local Apple tooling; they do not
constitute a downloaded Xcode distribution. [Module][module],
[C++ configuration][configure], [Xcode discovery][xcode]

Xcode discovery observes `DEVELOPER_DIR` and `XCODE_VERSION`. Record the selected
installation and SDK as environmental inputs, and inspect toolchain resolution
when multiple C++ toolchain families are registered. Selecting an Apple target
platform and selecting an available Xcode installation are related but separate
decisions. [Discovery inputs][xcode]

## Use the action helpers when authoring Apple rules

Load `apple_support` from `@apple_support//lib:apple_support.bzl`.
`action_required_attrs()` supplies the helper's required rule attributes.
`run` and `run_shell` combine action arguments with the selected Xcode's host
and target environment and its execution requirements. This release defaults
`use_default_shell_env` to true inside these helpers when it was not supplied;
account for that when assessing environmental inputs. [Helper implementation][helpers]

`run` supports `path_placeholders` and `xcode_path_resolve_level` for replacing
Xcode/SDK placeholders in arguments and, when selected, parameter-file contents.
`run_shell` does not support that placeholder substitution. Prefer the public
helper contract to embedding a developer's absolute Xcode path in generated
arguments. [Action and placeholder contracts][helpers]

Continue with [Apple platforms](platforms.md) for device/simulator and SDK
selection boundaries. For the separate downloaded SDK path in the `llvm`
integration, see [LLVM runtime inputs](../llvm/sysroots.md).

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[readme]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/README.md
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/apple_support/2.11.0/MODULE.bazel
[configure]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/crosstool/setup.bzl
[xcode]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/xcode/xcode_configure.bzl
[helpers]: https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/lib/apple_support.bzl
