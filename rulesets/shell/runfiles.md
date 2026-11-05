---
title: "Resolve shell runfiles through the library"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_shell": "0.8.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["shell.runfiles.lookup", "shell.runfiles.context"]
last_verified: "2026-11-05"
---

# Resolve shell runfiles through the library

Use this when a shell program needs a declared data file, another script, or a
Bazel-built executable at runtime.

## Use logical runfiles paths

The public dependency is `@rules_shell//shell/runfiles`. Its Bash library
provides `rlocation`, which searches directory-based runfiles or a manifest and
applies repository mapping. A file's build-time execution path and its runtime
lookup key serve different purposes. Use the library instead of constructing
paths from `bazel-bin`, a guessed external-repository directory, or the process's
current working directory. [Runfiles implementation and usage][runfiles]

The library must be initialized before calling it. The pinned upstream file
contains the supported initialization sequence. A shell target may instead use
the `use_bash_launcher` behavior described in [targets](targets.md). This page
does not provide an unexecuted copy of the initialization script.

## Preserve repository context

`rlocation` uses the calling script's repository mapping by default. Its optional
second argument supplies a canonical source-repository context explicitly;
`runfiles_current_repository` can obtain that context from a caller. This matters
when a shared library performs a lookup on behalf of code in another repository.
Do not hard-code canonical repository names or assume an apparent name has the
same meaning in every module. [Mapping implementation][runfiles]

`runfiles_export_envvars` prepares environment variables needed by children that
use Bazel runfiles libraries. Our recommendation is to export that environment
when spawning such a child, quote the resolved path as one shell argument, and
check lookup failure before using the result. [Child-process support][runfiles]

## Keep availability and lookup separate

Declaring the file in `data` or a suitable dependency makes it part of the
runtime contract; calling `rlocation` performs lookup. Neither substitutes for
the other. The [target implementation](targets.md) describes how the shell
rules collect dependencies. Verify both directory and manifest behavior when
the supported platforms require both.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[runfiles]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/runfiles/runfiles.bash
