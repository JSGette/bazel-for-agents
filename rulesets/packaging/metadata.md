---
title: "Control package metadata and reproducibility"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_pkg": "1.3.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["pkg.metadata.permissions", "pkg.metadata.timestamps", "pkg.metadata.rpm"]
last_verified: "2026-11-05"
---

# Control package metadata and reproducibility

Use this when an archive is structurally correct but differs across builds or
installs with the wrong permissions or owner.

## Specify metadata at the mapping boundary

`pkg_attributes` accepts octal-string `mode`, textual `user`/`group`, numeric
`uid`/`gid`, and additional format-specific fields. It is the supported way to
construct mapping attributes. `pkg_files` defaults to mode `0644`,
`pkg_mkdirs` to `0755`, and `pkg_mklink` to `0777`. Without explicit owner fields,
the package builder chooses values; the mapping API says not to rely on that
choice. [Attribute constructor and defaults][mappings]

Our recommendation is to set executable modes and ownership explicitly when
they are part of the delivery contract. Do not infer installation permissions
from the host checkout's mode bits.

## Keep timestamps intentional

Tar exposes `mtime`, `portable_mtime`, `preserve_mtime`, and `stamp`.
Zip exposes `timestamp` and `stamp`; its default fixed timestamp is
1980-01-01 00:00 UTC, and the format rounds timestamps to two-second precision.
For both rules, `stamp = 0` disables build-time stamping, `stamp = 1` uses
build time, and `stamp = -1` follows the invocation's stamping setting. With
stamping disabled, the configured timestamp/preservation options still matter.
[Tar time controls][tar], [Zip time controls][zip]

Prefer fixed metadata for artifacts intended to be reproducible. If release
stamping is required, record which metadata changes are intentional and verify
all other fields independently. A fixed timestamp does not by itself establish
byte-for-byte reproducibility of input binaries or compressors.

## Separate package tools from package descriptions

The `rules_pkg` module registers its discovered system RPM toolchain only as a
`dev_dependency`. Consumers cannot rely on that development registration to
supply `rpmbuild`. The public RPM configuration support can discover a system
installation; such a tool remains an explicit environment input.
[Module registration][module], [RPM configuration][rpm-tool]

Validate archive member paths, ownership, modes, symlinks, timestamps, and any
format-specific metadata expected by consumers. Installing an operating-system
package is a separate integration test from producing its archive.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[mappings]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl
[tar]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/tar/tar.bzl
[zip]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/zip/zip.bzl
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_pkg/1.3.0/MODULE.bazel
[rpm-tool]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/toolchains/rpm/rpmbuild_configure.bzl
