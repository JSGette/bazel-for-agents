---
title: "Choose a Go SDK and rule entry points"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_go": "0.65.0", "gazelle": "0.54.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md"]
claim_ids: ["go.setup.modules", "go.setup.sdk", "go.setup.registration", "go.setup.nogo"]
last_verified: "2026-11-05"
---

# Choose a Go SDK and rule entry points

## Use this when

Set up a Go module, choose the compiler, or identify which API owns a build
setting. Keep three versions distinct: Bazel, `rules_go`, and the Go SDK.
Gazelle has its own version and generates BUILD declarations.

## Public entry points

| Concern | Entry point |
| --- | --- |
| BUILD rules | `@rules_go//go:def.bzl`: `go_library`, `go_binary`, `go_test`, `go_cross_binary` |
| SDK module extension | `@rules_go//go:extensions.bzl`: `go_sdk` |
| Go dependency module extension | `@gazelle//:extensions.bzl`: `go_deps` |
| BUILD generation | `@gazelle//:def.bzl`: `gazelle` |

These apparent names assume direct module dependencies named `rules_go` and
`gazelle`; honor explicit repository aliases in the consuming project.
Sources: [rule exports](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/def.bzl),
[SDK export](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/extensions.bzl),
[dependency export](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/extensions.bzl),
[generator export](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/def.bzl).

## Choose the SDK deliberately

Repository recommendation: declare the intended SDK in the root module. The
`go_sdk.download` tag accepts an explicit `version`; `go_sdk.from_file` accepts
exactly one of `go_mod` and `go_work`. The latter reads the `toolchain` directive
first, then `go`. A Go language version and an SDK patch version need not express
the same intent, so inspect the actual directive before adopting file-based
selection. [Tag definitions and validation](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl);
[version extraction](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/go_mod.bzl).

The extension also supports `go_sdk.host`. It discovers a host installation,
which is a different reproducibility boundary from a downloaded distribution.
Prefer a versioned download for shared build instructions. The extension's default
platform expansion covers the host and a fixed list of common execution platforms;
it is not proof that every desired executor or target is supported.
[SDK construction and execution platforms](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl).

The ruleset module already registers `@go_toolchains//:all`. The extension
constructs toolchain declarations in module order, processing the root first.
Do not copy compiler paths from a generated repository name into actions: use
toolchain consumers. [registration](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/MODULE.bazel);
[ordering and generated repositories](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl).

## Developer tools and static analysis

`@rules_go//go` exposes the selected host-compatible Go tool for developer
commands. Upstream explicitly excludes using this convenience target in build
actions; an action should consume the actual execution toolchain.
[SDK use contract](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/docs/go/core/bzlmod.md).

Configure `nogo` through `go_sdk.nogo` when static checks should participate in
compilation. Only the root's tag is honored; `includes` and `excludes` bound its
package scope, with the default covering the main repository.
[nogo selection and validation](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/extensions.bzl).

Continue with [targets](targets.md), [dependencies](dependencies.md), and
[Gazelle generation](../gazelle/generation.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#go-setup).
