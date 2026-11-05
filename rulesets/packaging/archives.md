---
title: "Create archives and system-package outputs"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_pkg": "1.3.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["pkg.archives.exports", "pkg.archives.composition", "pkg.archives.outputs", "pkg.archives.collisions"]
last_verified: "2026-11-05"
---

# Create archives and system-package outputs

Use this after defining the [file mappings](file-mappings.md).
Load the format-specific public entry point:

| Format | Export |
| --- | --- |
| Tar and compressed tar | `pkg_tar` from `@rules_pkg//pkg:tar.bzl` |
| Zip | `pkg_zip` from `@rules_pkg//pkg:zip.bzl` |
| Debian package | `pkg_deb` from `@rules_pkg//pkg:deb.bzl` |
| RPM | `pkg_rpm` from `@rules_pkg//pkg:rpm.bzl` |

[Tar export][tar-export], [Zip export][zip-export], [Debian export][deb-export],
[RPM export][rpm-export]

## Distinguish file inputs from archive composition

`pkg_tar.srcs` accepts file or mapping inputs. `pkg_tar.deps` accepts tar
archives whose contents are unpacked and repacked into the result; it does not
place each archive into the output as an opaque file. `package_dir` prefixes
the destination paths as the archive is written. [Tar rule][tar]

The tar rule supports built-in compression choices and an exec-configured
`compressor` executable. Zip offers `compression_type` and `compression_level`.
Choose the format and compressor as part of the artifact contract rather than
assuming a filename suffix alone defines consumer behavior.
[Tar options][tar], [Zip options][zip]

## Make collisions fail deliberately

For new archive definitions, our recommendation is to set
`allow_duplicates_with_different_content` to false: both tar and zip expose the
attribute, and this release's default is true. Tar separately controls duplicate
entries from dependency archives using `allow_duplicates_from_deps`.
Inspect archive member names and metadata in verification, not just the existence
of an output file. [Tar collision controls][tar], [Zip collision controls][zip]

`out` identifies the declared output. When `package_file_name` is supplied,
the shared output helper creates the artifact with that name and makes the
default output a symlink to it. A custom consumer should inspect the selected
rule's output contract instead of guessing a filename from its target label.
[Output-file construction][output-files]

System packages add format-specific package metadata and tooling. Consult the
selected rule's pinned schema and [metadata guidance](metadata.md); this page
does not claim that every format runs on every host.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[tar-export]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/tar.bzl
[zip-export]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/zip.bzl
[deb-export]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/deb.bzl
[rpm-export]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/rpm.bzl
[tar]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/tar/tar.bzl
[zip]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/zip/zip.bzl
[output-files]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/util.bzl
