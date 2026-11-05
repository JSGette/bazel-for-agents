---
title: "Model Go packages, binaries, tests, and runtime data"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_go": "0.65.0", "gazelle": "0.54.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/go/setup.md", "core/providers.md", "core/outputs-and-runfiles.md"]
claim_ids: ["go.targets.package", "go.targets.files", "go.targets.tests", "go.targets.runfiles"]
last_verified: "2026-11-05"
---

# Model Go packages, binaries, tests, and runtime data

## Use this when

Add a package, executable, test, or generated Go source. Start from the public
`@rules_go//go:def.bzl` exports and let the project’s Gazelle target maintain
ordinary source/dependency declarations where configured.
[Public exports](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/def.bzl).

## Choose the dependency relationship

| Attribute | Meaning |
| --- | --- |
| `srcs` | Files compiled as this package, subject to Go build constraints |
| `deps` | Directly imported libraries providing `GoInfo` |
| `importpath` | Source import identity, explicitly set or inherited through `embed` |
| `embed` | Compatible libraries whose sources compile into this package |
| `embedsrcs` | Files available to `//go:embed` during compilation |
| `data` | Runtime files or programs |

`embed` is not an ordinary import edge. Embedded libraries must have the same
`importpath`; at most one can enable cgo, and the embedding rule cannot also
enable it. Files in `embedsrcs` must satisfy the documented logical-directory
restrictions. [Attribute contracts](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl);
[source and provider merging](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/context.bzl).

Repository recommendation: represent a reusable package with `go_library`, then
use its public dependency interface. A binary may embed a main-package library,
and tests may embed the package under test so unexported package declarations
are compiled with same-package tests. Distinguish that operation from importing
another package through `deps`. [Binary attributes](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/binary.bzl);
[Test construction](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/test.bzl).

## Generated sources and build constraints

Generated files can participate in `srcs` and `embedsrcs`. Their producers must
remain explicit graph dependencies; generation does not imply that Gazelle can
inspect source contents that do not exist yet. Protect required generated-source
dependencies using the generator's configured extension or a narrow `keep`
annotation. [Generated-file support](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/library.bzl);
[Generated-source keep example](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

## Runtime data and tests

Use the `github.com/bazelbuild/rules_go/go/runfiles` package, available through
`@rules_go//go/runfiles`, for logical runfile lookup. `Rlocation` locates a file;
`Env` supplies runfiles environment entries for a child process. The library
handles manifest and directory layouts and repository mappings. Avoid deriving
paths from a canonical external-repository name or assuming a symlink tree.
[Library target](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/runfiles/BUILD.bazel);
[Lookup and environment contract](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/runfiles/runfiles.go).

`go_test` normally changes to the package directory to match Go test behavior.
Its `rundir` attribute changes that location, but the documented behavior differs
when runfile symlinks are unavailable. Runtime resources should therefore use
runfiles lookup when portability matters, rather than relying on the process
working directory. [rundir contract](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/go/private/rules/test.bzl).

For cgo, instrumentation, and platform selection, continue with [cgo](cgo.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#go-targets).
