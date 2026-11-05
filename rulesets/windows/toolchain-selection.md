---
title: "Choose Windows compiler, ABI, and SDK ownership"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_cc": "0.2.27", "llvm": "0.8.26"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["windows.tools.discovery", "windows.tools.llvm", "windows.tools.imports"]
last_verified: "2026-11-05"
---

# Choose Windows compiler, ABI, and SDK ownership

Use this when choosing native Windows compilation or cross-compiling a Windows
artifact. Our recommendation is to record four separate choices: execution OS,
target CPU, target ABI, and source of compiler/SDK/runtime inputs.

## Local Visual C++ discovery

The `rules_cc` configuration path searches installed Visual C++ tools.
`BAZEL_VC` selects a VC directory; `BAZEL_VS` selects a Visual Studio directory
whose `VC` child is used. The implementation checks these supplied paths before
its automatic search. `BAZEL_VC_FULL_VERSION` selects the toolset version and
`BAZEL_WINSDK_FULL_VERSION` supplies the requested SDK version.
[Windows discovery][windows], [tracked environment inputs][configure]

These settings select existing installations. They are not registry modules
that download a named Visual Studio release. Pin and provision the appropriate
worker image or installation separately, and retain the actual selected tool
and SDK versions in build evidence.

## LLVM's explicit Windows integration

The `llvm` module described in [LLVM setup](../llvm/setup.md) has its own
MSVC-ABI toolchain path using clang-cl/lld-link, and distinct target settings
from its GNU/MinGW path. Its module configures the `windows_support` dependency
for Microsoft runtime and SDK inputs. This is separate from `rules_cc`'s local
Visual C++ discovery; do not combine their setup assumptions.
[LLVM module inputs][llvm-module], [toolchain branches][llvm-declare]

The pinned integration documents explicit acceptance gates for the Microsoft
inputs and restrictions including unsupported debug CRT modes. Inspect those
requirements before choosing that route; this repository has not reviewed
`windows_support` as an independent ruleset or executed the cross-platform
matrix. [Integration boundaries][llvm-readme]

## Preserve the link and runtime distinction

For prebuilt DLL dependencies, `cc_import.interface_library` describes the link
interface and `shared_library` describes the runtime DLL. A `system_provided`
import declares the runtime supplied outside the target, and cannot also supply
`shared_library`. Prefer a complete declared runtime dependency when packaging
the library with the application. [Import validation][imports]

Continue with [paths and processes](paths-and-processes.md), then verify the
built program on the intended Windows runtime.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[configure]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/cc_configure.bzl
[windows]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/windows_cc_configure.bzl
[llvm-module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel
[llvm-declare]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl
[llvm-readme]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md
[imports]: https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_import.bzl
