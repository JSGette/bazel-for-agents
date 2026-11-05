---
title: "Configure the GCC distribution module"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"gcc_toolchain": "0.13.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["gcc.setup.extension", "gcc.setup.distribution", "gcc.setup.registration"]
last_verified: "2026-11-05"
---

# Configure the GCC distribution module

Use this when selecting `gcc_toolchain` from `f0rmiga/gcc-toolchain`.
The module version is 0.13.0; it is separate from the GCC compiler version.

## Configure through the module extension

The public extension is `gcc_toolchains` from
`@gcc_toolchain//toolchain:module_extensions.bzl`. Its `toolchain` tag accepts a
repository `name` and `target_arch`; this release accepts `x86_64`, `aarch64`,
and `armv7`. It also exposes compiler version and selected feature/flag settings.
Only root-module tags are processed, so a dependency cannot choose the consumer's
GCC repositories by adding its own tag. [Extension implementation][extension]

The root must import the generated repositories and register their toolchain
targets. The ruleset's own module declarations are development dependencies and
do not provide registrations for consuming projects. [Module][module],
[extension rationale][extension]

## Pin the compiler distribution consciously

`gcc_version` defaults to `16.2.0` in this release. `gcc_versions` describes
version/target-architecture download URLs and SHA-256 hashes; the repository
rule downloads and extracts the selected archive using that hash. It then
constructs compiler, binutils, builtin include, and sysroot paths from the
archive. [Distribution and defaults][defs]

Our recommendation is to record both the module and compiler selection, retain
the archive identity in dependency evidence, and inspect custom flag additions
for host paths. Do not infer libc compatibility or supported execution hosts
from the GCC version alone.

## Review optional configuration

The tag exposes `extra_cflags`, `extra_cxxflags`, `extra_ldflags`, optional
Fortran support, and constraint/settings additions. `supports_param_files`
defaults to false; it enables the generated C++ toolchain's response-file
support when selected. Match these options to the selected distribution and
actual command-line limits, then verify the resulting actions.
[Shared extension attributes][defs]

Continue with [cross-compilation](cross-compilation.md) for the execution-host
restriction, which is narrower than the target-architecture list.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[extension]: https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/module_extensions.bzl
[defs]: https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/defs.bzl
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/gcc_toolchain/0.13.0/MODULE.bazel
