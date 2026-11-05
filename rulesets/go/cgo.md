---
title: "Configure cgo, native dependencies, and cross compilation"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_go": "0.65.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/go/setup.md", "rulesets/go/targets.md"]
claim_ids: ["go.cgo.attributes", "go.cgo.mode", "go.cgo.platform", "go.cgo.instrumentation"]
last_verified: "2026-11-05"
---

# Configure cgo, native dependencies, and cross compilation

## Use this when

A Go package imports C, links native libraries, produces a C-consumable library,
or builds for a different platform.

## Declare the native contract

`cgo = True` permits cgo sources and native files in `srcs`; it does not by itself
force the effective build mode to enable cgo. Declare native library dependencies
in `cdeps`, and use `cppopts`, `copts`, `cxxopts`, and `clinkopts` for their distinct
preprocessing, C, C++, and linking roles. These attributes are valid only for
cgo-enabled source packages. [cgo attribute contract](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl).

The implementation obtains compilation and linking information through the C++
toolchain and its feature configuration. Repository recommendation: model headers,
libraries, compiler distribution, and sysroot as declared inputs instead of
relying on host search paths. `cdeps` should carry native providers, not a shell
command that discovers a host library.
[cgo_context_data_impl](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/context.bzl);
[Native compilation/linking inputs](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/cgo.bzl).

## Separate pure mode from target selection

The effective Go configuration includes `pure`, and the target can constrain cgo
availability. Without a usable C++ toolchain, `go_context` selects pure behavior;
when `pure` was explicitly forced off, that missing toolchain produces an error.
Inspect the effective platform and configuration before changing source code to
work around a cgo failure. [go_context mode selection](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/context.bzl).

Prefer platform-based selection for a complete cross-compilation configuration.
The binary/test `goos` and `goarch` attributes must be specified together when
used; their transition selects a rules_go platform, including its cgo variant
when pure mode is explicitly off. Changing only the Go architecture cannot
manufacture a compatible native compiler, linker, headers, or libraries.
[_go_transition_impl](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/transition.bzl);
[Platform attribute guidance](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/binary.bzl).

`go_cross_binary`, exported from the regular Go rules entry point, wraps a
`go_binary` and can select a `platform`, `sdk_version`, and `compilation_mode`.
Its SDK selector constrains a registered SDK; it is not a download request.
Use it when one BUILD graph needs named variants with different configurations.
[Cross-binary attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/cross.bzl);
[go_cross_transition](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/transition.bzl).

## Linking and instrumentation

`pure`, `static`, and `linkmode` answer different questions. Pure mode disables
cgo; static controls final linking; `linkmode` includes executable, plugin,
C-shared, and C-archive modes with platform restrictions. Static linking does
not mean “no native inputs.” The implementation rejects race and memory-sanitizer
instrumentation when pure mode is effective.
[validate_mode and linking logic](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/mode.bzl);
[Mode attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/binary.bzl).

Repository recommendation: verify the target tuple, C/C++ toolchain, Go SDK,
native library ABI, and runtime loader dependencies as one integration. A build
for one Linux architecture says nothing about macOS, Windows, or another libc.

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#go-cgo).
