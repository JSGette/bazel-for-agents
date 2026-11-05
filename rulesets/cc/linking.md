---
title: "Choose C/C++ linking boundaries"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_cc": "0.2.27"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["cc.linking.static", "cc.linking.import", "cc.linking.shared"]
last_verified: "2026-11-05"
---

# Choose C/C++ linking boundaries

Use this when importing native libraries, producing a shared library, or
investigating duplicate symbols and missing runtime libraries.

## Separate three linking decisions

- `linkstatic` expresses the rule's static-versus-dynamic linking preference;
  for `cc_library` it also controls shared-library output creation. The final
  result still depends on available libraries, toolchain features, and linking
  mode. It does not alone promise a fully static executable.
- `alwayslink` asks for all object files in a static library to be linked even
  when symbols do not otherwise pull them in. Use it only when that retention
  is part of the library's contract, such as registration through static objects.
- Runtime ABI and C/C++ runtime selection belong to the toolchain and platform
  choices; record those choices alongside the target's linking policy.

[Linking attribute contract][attrs], [library behavior][library]

## Represent prebuilt libraries with cc_import

`cc_import` accepts `static_library`, `pic_static_library`, `shared_library`,
`interface_library`, and `hdrs` for their distinct roles. In particular, a
Windows import library is a link input, while its DLL is a runtime artifact.
`system_provided = True` declares that the runtime library is supplied by the
system; it is incompatible with supplying `shared_library` in that target.
Without that setting, an `interface_library` requires a `shared_library`.
[Import implementation and validation][import]

Our recommendation is to preserve the runtime artifact in the dependency
contract and test the installed or packaged binary. A successful link is not a
runtime deployment check.

## Define shared-library ownership

`cc_shared_library` takes C++ roots in `deps` and shared-library dependencies
providing `CcSharedLibraryInfo` in `dynamic_deps`. Its analysis accounts for
which C++ targets are provided by dynamic dependencies and reports conflicting
exports or static-link ownership. `exports_filter` changes this analysis
accounting; it does not itself control the native linker's exported symbol set.
Use the toolchain/linker mechanism separately when symbol visibility must be
restricted. [Shared-library rule][shared]

Diagnose the actual link action and dependency graph before adding global
`linkopts`, `alwayslink`, or permissive ownership workarounds. Continue with
[packaging file mappings](../packaging/file-mappings.md) for delivery layout.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[attrs]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/attrs.bzl
[library]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_library.bzl
[import]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_import.bzl
[shared]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_shared_library.bzl
