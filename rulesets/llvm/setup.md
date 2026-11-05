---
title: "Select the hermetic-llvm integration"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"llvm": "0.8.26"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["llvm.setup.identity", "llvm.setup.registration", "llvm.setup.version"]
last_verified: "2026-11-05"
---

# Select the hermetic-llvm integration

Use this when choosing the `llvm` module from `hermeticbuild/hermetic-llvm`.
These instructions describe that integration's APIs specifically.

## Record the ruleset and compiler separately

The ruleset candidate is `llvm` 0.8.26. Its module sets its own LLVM source
selection to `23.1.2` and configures associated repositories. The public `llvm`
extension is loaded from `@llvm//extensions:llvm.bzl`; its `version` tag accepts
`llvm_version`, with a root request taking precedence. Source selection must
exist in the ruleset's version index. These are different version decisions.
[Module defaults][module], [selection implementation][extension]

Do not assume changing the source version also downloads a matching prebuilt
compiler. Compiler bootstrap stages and prebuilt seed availability are separate
parts of this integration. The pinned README describes selecting a source-built
stage when the requested version lacks a corresponding prebuilt; verify that
combination before recommending it. [Version and bootstrap guidance][readme]

## Register the intended toolchain family

`@llvm//toolchain:all` is the public broad registration pattern. Toolchain
objects specify execution and target constraints and refer to configured C++
toolchains. For a narrower registration set, the `toolchain` extension in
`@llvm//extensions:toolchain.bzl` accepts `exec` and `target` tags with `os` and
`arch`, generates `llvm_toolchains`, and declares the requested cross-product.
Missing exec or target lists default to that side's supported list.
[Toolchain declarations][declare], [subset extension][toolchain-extension]

The extension validates OS/architecture pairs against its supported tables;
the attribute's accepted strings alone do not establish a valid pair.
[Pair validation][toolchain-extension]

## Decide runtime and SDK policy

Continue with [runtime/sysroot inputs](sysroots.md) before choosing target
platforms, then [cross-compilation](cross-compilation.md). Record the libc ABI,
C++ runtime, compiler stage, SDK inputs, and execution platform along with the
ruleset version. Broad upstream support declarations are not local build or
interoperability results for this repository.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel
[extension]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/llvm.bzl
[declare]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl
[toolchain-extension]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/toolchain.bzl
[readme]: https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md
