---
title: "Cross-compile a binary"
status: "source-verified"
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["toolchains/cross-compilation.md", "rulesets/llvm/cross-compilation.md", "diagnostics/toolchain-resolution.md", "rulesets/go/cgo.md"]
claim_ids: []
last_verified: "2026-11-05"
---

# Cross-compile a binary

This is a task checklist and reading path. Follow the exact version and evidence
boundaries in the linked pages; this page adds no independently verified API
claims and is not a runnable integration fixture.

## 1. Name both environments

Record where build tools run and where the binary must run, including architecture, OS, ABI, and any runtime/SDK requirements. A target architecture alone is insufficient to select every native input.

Read [cross compilation](../toolchains/cross-compilation.md) and
[platforms and constraints](../configuration/platforms-and-constraints.md).

## 2. Choose a coherent toolchain family

Use the selected language rules and native-toolchain integration. Keep execution-compatible compiler binaries distinct from target sysroots and runtimes; mixed-language builds must agree on the ABI boundary.

Read [cross compilation](../rulesets/llvm/cross-compilation.md) and
[cross compilation](../rulesets/gcc/cross-compilation.md).

## 3. Inspect resolution before execution

Confirm the configured target, selected execution platform, toolchain wrappers, and action executable. Check execution groups when code generation and compilation have different worker requirements.

Read [toolchain resolution](../diagnostics/toolchain-resolution.md) and
[execution groups](../toolchains/execution-groups.md).

## 4. Verify more than compilation

Inspect the produced binary format and linkage, then run it on an appropriate target environment or a deliberately configured emulator. Do not describe a build-only result as proof of target runtime behavior. The runtime-check requirement is this repository’s validation recommendation.

Read [cgo](../rulesets/go/cgo.md) and
[ffi](../rulesets/rust/ffi.md).

## Completion evidence

Record the source change, selected dependency graph, Bazel version, relevant
platforms and flags, and the assertions actually observed. Preserve gaps rather
than inferring a wider compatibility result. Executable recipe coverage and CI
are follow-up work in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
