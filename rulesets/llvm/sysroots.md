---
title: "Choose LLVM target runtimes and SDK inputs"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"llvm": "0.8.26"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["llvm.runtime.model", "llvm.runtime.glibc", "llvm.runtime.apple", "llvm.runtime.windows"]
last_verified: "2026-11-05"
---

# Choose LLVM target runtimes and SDK inputs

Use this when selecting a target ABI or investigating header, startup-object,
or runtime-library failures with the LLVM integration.

## Treat runtime components as part of the toolchain

This ruleset supplies target-specific runtime components and models libc and
C++ runtime selection through its constraints and build targets. Its model does
not require the user to provide an arbitrary preassembled sysroot for each
Linux target. Review the selected libc, C++ library, startup objects, and compiler
runtime together. [Integration model][readme], [libc constraints][libc],
[C++ runtime constraints][cxx]

Linux libc choices include musl and versioned glibc constraints named
`@llvm//constraints/libc:gnu.<version>`. The release's ordinary default is
glibc 2.28, with a RISC-V default of 2.33; the supported-version function excludes
RISC-V glibc versions before 2.27. An explicit deployment ABI is preferable to
assuming that CPU and OS alone describe runtime compatibility. [Version table][libc]

The integration documents libc++ as the default C++ library and supports
versioned libstdc++ selection for Linux/glibc. Treat that boundary as part of
interoperability with prebuilt native dependencies; the support statement is
not a local ABI test. [Runtime selection][readme], [constraint generation][cxx]

## Identify where Apple SDK files come from

The `osx` extension in `@llvm//extensions:osx.bzl` supports `from_archive` and
`from_host`. The module supplies a pinned archive by default. Host selection
uses `xcrun` and local SDK paths and only applies when Bazel runs on macOS;
the environment setting `BAZEL_MACOS_USE_HOST_SDK=1` also selects that host path
on macOS. Switching to host SDK discovery changes the reproducibility boundary.
[SDK selection][osx], [default archive configuration][module]

The extension also controls included frameworks/libraries. Verify that the
chosen SDK subset covers the application rather than assuming every framework
is present. [SDK filtering][osx]

## Distinguish Windows runtime families

Windows GNU/MinGW CRT selection and Windows MSVC ABI selection are different
constraints. The MSVC path uses Microsoft runtime/SDK inputs configured through
the `windows_support` dependency; the pinned integration documents explicit
license-acceptance gates. Selecting an LLVM compiler does not eliminate those
SDK/runtime requirements. [Windows integration][readme], [module inputs][module]

See [Windows toolchain selection](../windows/toolchain-selection.md) for the
separate local MSVC discovery path and [cross-compilation](cross-compilation.md)
for execution-versus-target decisions.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[readme]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md
[libc]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/constraints/libc/libc_versions.bzl
[cxx]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/constraints/cxxstdlib/BUILD.bazel
[osx]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/osx.bzl
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel
