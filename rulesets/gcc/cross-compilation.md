---
title: "Respect the GCC execution-host and target contracts"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"gcc_toolchain": "0.13.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["gcc.cross.execution", "gcc.cross.target"]
last_verified: "2026-11-05"
---

# Respect the GCC execution-host and target contracts

Use this when choosing a GCC target architecture or investigating why toolchain
resolution rejects an execution platform.

## Do not confuse target support with host support

The generated C++ and Fortran toolchain registrations explicitly require
`@platforms//os:linux` and `@platforms//cpu:x86_64` on the execution side.
The target architecture can be x86_64, AArch64, or ARMv7. Therefore the presence
of an AArch64 target archive is not evidence that the compiler runs on an
AArch64 executor. [Registration templates][defs], [tag schema][extension]

Our recommendation is to make the Linux x86_64 execution requirement explicit
when planning local or remote builds. A different developer host needs a
suitable execution environment; merely changing the target platform does not
supply one.

## Describe the target fully

Default target constraints include Linux and the selected architecture. The
extension exposes `extra_target_compatible_with` and `extra_target_settings`
for additional selection conditions. These affect toolchain eligibility; they
do not modify the machine code or libc contents of a downloaded distribution
by themselves. [Constraint construction and compiler archive selection][defs]

Choose ABI, libc requirements, instruction-set options, and runtime delivery
requirements together. Keep C/C++ flags that alter those properties consistent
with the selected distribution and with dependent native libraries. This is a
configuration-review recommendation, not a claim that every flag combination
is supported.

## Validate the resulting program separately

Inspect the selected toolchain and compile/link action, then verify the emitted
architecture and run a smoke test on the target environment. A successful
cross-link on Linux x86_64 does not establish target runtime compatibility.
Record the module version, GCC version, archive hashes, target settings, and
execution platform in the eventual fixture evidence.

For the module's extension and registration flow, return to [setup](setup.md).

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[defs]: https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/defs.bzl
[extension]: https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/module_extensions.bzl
