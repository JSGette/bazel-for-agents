---
title: "Select shell rules and interpreter dependencies"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_shell": "0.8.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["shell.setup.exports", "shell.setup.discovery", "shell.setup.toolchain"]
last_verified: "2026-11-05"
---

# Select shell rules and interpreter dependencies

Use this when adding shell entry points, tests, or shell-based build tools.
Declare `rules_shell` at the selected version and use its public rule loads:
`@rules_shell//shell:sh_binary.bzl`, `sh_library.bzl`, and `sh_test.bzl` export
`sh_binary`, `sh_library`, and `sh_test` respectively.
[Binary][binary], [library][library], [test][test]

## Account for the interpreter

The module invokes its shell configuration extension, imports
`local_config_shell`, and registers that repository's toolchains. This is
local configuration; adding the ruleset is not evidence that the same shell
binary exists on every executor. [Module][module], [extension][configure]

The public `sh_toolchain` is loaded from
`@rules_shell//shell/toolchains:sh_toolchain.bzl`. Its `path` is an absolute
interpreter path. The optional `launcher` and `launcher_maker` support Windows:
the launcher is target-configured, while the launcher maker is exec-configured.
The toolchain type is `@rules_shell//shell:toolchain_type`.
[Toolchain schema][toolchain]

Our recommendation is to record interpreter availability as an execution
requirement, and use a declared executable rule for tools that can avoid shell
interpretation. A shell target's runtime contract and a `run_shell` build
action's execution environment should each be reviewed explicitly.

## Choose the next page

- [Targets](targets.md): entry script, libraries, runtime data, environment.
- [Runfiles](runfiles.md): lookup APIs, repository mapping, child processes.
- [Windows processes](../windows/paths-and-processes.md): quoting and platform
  boundaries.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[binary]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_binary.bzl
[library]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_library.bzl
[test]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_test.bzl
[module]: https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_shell/0.8.0/MODULE.bazel
[configure]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/extensions/sh_configure.bzl
[toolchain]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/toolchains/sh_toolchain.bzl
