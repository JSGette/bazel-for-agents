---
title: "Select C/C++ rules and compiler toolchains"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_cc": "0.2.27"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["cc.setup.exports", "cc.setup.local", "cc.setup.custom"]
last_verified: "2026-11-05"
---

# Select C/C++ rules and compiler toolchains

Use this when introducing C/C++ targets or reviewing which compiler a build uses.
Our recommendation is to make the rule dependency, compiler selection, target
platform, and runtime ABI separate decisions.

## Load the public rules explicitly

Declare the `rules_cc` module at the selected version. Public rule entry points
include `@rules_cc//cc:cc_library.bzl`, `cc_binary.bzl`, `cc_test.bzl`,
`cc_import.bzl`, and `cc_shared_library.bzl`. Each exports the correspondingly
named rule; `@rules_cc//cc:defs.bzl` re-exports them. Load `CcInfo` from
`@rules_cc//cc/common:cc_info.bzl` and `cc_common` from
`@rules_cc//cc/common:cc_common.bzl` when authoring integrations. [Exports][defs]

Do not treat the ruleset version as a compiler version. In this release,
`rules_cc` uses its `cc_configure_extension` and registers the generated
`local_config_cc_toolchains` repository. That path discovers local tools; it
does not pin a downloaded compiler distribution. [Module][module],
[configuration implementation][configure]

## Choose compiler ownership deliberately

| Requirement | Reference |
| --- | --- |
| Use and inspect local compiler discovery | The rules_cc module and configuration implementation linked above |
| Pin a source/distribution-based LLVM integration | [LLVM setup](../llvm/setup.md) |
| Select the GCC distribution integration | [GCC setup](../gcc/setup.md) |
| Use Xcode-backed Apple compilation | [Apple setup](../apple/setup.md) |
| Select Windows compiler and SDK inputs | [Windows toolchains](../windows/toolchain-selection.md) |

These are choices, not interchangeable setup APIs. Record compiler/SDK versions
and the selected execution and target platforms separately from `rules_cc`.
Treat local discovery as an explicit machine dependency when assessing remote
execution or repeatability.

## Consume the toolchain from custom rules

`@rules_cc//cc:use_cc_toolchain.bzl` exports `use_cc_toolchain`; its result is
used in a rule's toolchain requirements. `@rules_cc//cc:find_cc_toolchain.bzl`
exports `find_cc_toolchain`, which retrieves the C++ toolchain from the supplied rule context. Use these public APIs and `cc_common` for C++ integration
instead of reaching into `cc/private`. [Requirement helper][use],
[lookup helper][find]

Continue with [target interfaces](targets.md) and [linking](linking.md).

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[defs]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/defs.bzl
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_cc/0.2.27/MODULE.bazel
[configure]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/cc_configure.bzl
[use]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/use_cc_toolchain.bzl
[find]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/find_cc_toolchain.bzl
