---
title: "Choose LLVM execution and target platform pairs"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"llvm": "0.8.26"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["llvm.cross.pairs", "llvm.cross.abi", "llvm.cross.ffi"]
last_verified: "2026-11-05"
---

# Choose LLVM execution and target platform pairs

Use this when the compiler runs on one platform and emits code for another.
Begin with [setup](setup.md) and [runtime inputs](sysroots.md).

## Separate where tools run from what they produce

The release defines execution pairs for Linux, macOS, and Windows on x86_64
and AArch64. Its target table separately includes those OS families, additional
Linux architectures, UEFI, BPF, and WebAssembly pairs. These are declared
coverage tables; this repository has not executed that matrix. The toolchain
declarations associate execution and target constraints for each pair.
[Supported-pair tables][pairs], [declarations][declare]

Our recommendation is to select the target platform according to the required
ABI, then inspect the actual resolved compiler execution platform. Registering
a compatible compiler does not provision a remote worker or execute the target
program on that worker.

## Preserve ABI-specific selection

The generated Windows toolchains distinguish the MinGW-compatible settings
from explicit MSVC settings. The MSVC branch has distinct target-settings
checks even where OS and CPU constraints match. Do not replace the integration's
platform with a CPU/OS-only clone and expect identical runtime behavior.
[Target settings][declare], [Windows ABI description][readme]

For other platforms, carry libc, C++ library, and any target-specific constraints
through the build. Building a binary for a target and running a test on that
target are separate validation steps. Cross-compilation needs a suitable test
runner or actual target machine before runtime support can be claimed.

## Review language interoperability separately

The pinned integration documents Go 1.27 as its minimum for unpatched cgo
integration, and describes additional Rust native-linking/runtime constraints.
Treat those as integration-specific source guidance requiring validation with
the selected language ruleset and SDK. The generic C++ support table does not
prove that any Go or Rust compiler version can use the toolchain unchanged.
[Interoperability notes][readme]

Verify a minimal compile/link target, a runtime smoke test on the destination,
and at least one representative native dependency before expanding a platform
matrix. Record compiler stage, target ABI, language SDK, and execution platform
in the future test evidence.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[pairs]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/platforms/common.bzl
[declare]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl
[readme]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md
