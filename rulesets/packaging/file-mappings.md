---
title: "Describe installation layouts with package mappings"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_pkg": "1.3.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["pkg.mappings.providers", "pkg.mappings.paths", "pkg.mappings.links"]
last_verified: "2026-11-05"
---

# Describe installation layouts with package mappings

Use this when packaging generated files or designing an installation tree.
Our recommendation is to describe the layout separately from the archive or
system-package format.

## Build a mapping layer

Load mapping rules from `@rules_pkg//pkg:mappings.bzl`: `pkg_files`,
`pkg_filegroup`, `pkg_mkdirs`, `pkg_mklink`, `pkg_attributes`, and `strip_prefix`.
`pkg_files` describes destination paths and attributes through packaging
providers; it does not produce an archive. `pkg_filegroup` combines mapping
providers for a downstream packager. [Mappings][mappings], [providers][providers]

| Input decision | API |
| --- | --- |
| Files or generated target outputs | `pkg_files.srcs` |
| Remove a source-side directory prefix | `strip_prefix` helper and attribute |
| Add an installation-side directory | `prefix` |
| Override one file's destination | `renames`, keyed by source label |
| Set permissions and ownership | `pkg_attributes(...)` passed to `attributes` |
| Preserve a specially configured or empty directory | `pkg_mkdirs` |
| Describe an installation symlink | `pkg_mklink` |

[Mapping schemas][mappings]

## Review the destination names

The default `pkg_files.strip_prefix` strips directories, retaining filenames.
Use an explicit layout when files from different directories could share a
basename. A rename key must resolve to one included file; the implementation
rejects keys covering multiple files or excluded inputs. [Path processing][mappings]

Ordinary prefix stripping works on paths known during analysis. It does not
rewrite paths inside a directory artifact. The special `REMOVE_BASE_DIRECTORY`
rename handles a directory artifact's containing directory, while
`filter_directory` supplies a separate transformation rule for directory
contents. Pick the operation matching the actual artifact type.
[Directory handling][mappings]

`include_runfiles` includes runtime files using Bazel's runfiles layout. It is
not an application-specific install-layout generator. Review that layout and
runtime lookup requirements before distributing a Bazel-built executable.
[Runfiles mapping][mappings]

Continue with [archives](archives.md) and [metadata](metadata.md).

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[mappings]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl
[providers]: https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/providers.bzl
