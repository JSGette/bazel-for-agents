---
title: "Keep Windows paths, shell syntax, and runfiles explicit"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: ["9.3.1"]
rulesets_verified: {"rules_shell": "0.8.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["windows.process.actions", "windows.process.genrule", "windows.process.runfiles", "windows.process.paths"]
last_verified: "2026-11-05"
---

# Keep Windows paths, shell syntax, and runfiles explicit

Use this when a build works on a Unix executor but fails on native Windows.
Keep execution-platform syntax separate from the target program's platform.

## Avoid accidental shell interpretation

`ctx.actions.run` accepts an executable and a sequence of arguments.
`ctx.actions.run_shell` accepts a shell command with separate argument values.
Our recommendation is to use a declared executable and structured arguments
when no shell behavior is required. Do not build a single command string by
concatenating unquoted paths or assume one quoting convention covers Bash,
Batch, PowerShell, and an executable's own response-file parser.
[Action API][actions]

For a `genrule` requiring platform-specific shell code, Bazel 9.3.1 provides
`cmd_bash`, `cmd_bat`, and `cmd_ps`. On Windows, `cmd_ps` has precedence over
`cmd_bat`, which has precedence over `cmd`/`cmd_bash`; the Batch command uses
`cmd.exe`. Treat these as distinct programs, not interchangeable string
spellings. [Genrule command contracts][genrule]

## Use runfiles lookup instead of directory guesses

`--enable_runfiles` is a tri-state setting whose default is off on Windows and
on elsewhere. Accordingly, a runtime consumer must not require a symlink tree
unless the build's supported configuration guarantees one. The shell runfiles
library supports both manifests and directories. [Bazel option][options],
[shell lookup implementation][runfiles]

Use [shell runfiles guidance](../shell/runfiles.md) for scripts and the selected
language's runfiles API for its programs. A runtime lookup key is not a path
separator conversion of a build-time execution path.

## Treat path length and symlinks as environment requirements

`--output_user_root` is a Bazel startup option that can place outputs under a
shorter root. This is a useful mitigation when a selected tool has path-length
limits; it does not change that tool's semantics. `--windows_enable_symlinks`
is also a startup option, and actual symlink creation requires Windows support
such as Developer Mode or sufficient privilege. [Startup parser][startup],
[versioned Windows guidance][windows-doc]

Review case sensitivity, executable extensions, argument length, and response
files against the actual tools in the chosen execution environment. Validate
native Windows behavior separately from running Linux tools in a Linux
execution environment on a Windows machine.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[genrule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/genrule/GenRuleBaseRule.java
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java
[runfiles]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/runfiles/runfiles.bash
[startup]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/startup_options.cc
[windows-doc]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/configure/windows.md
