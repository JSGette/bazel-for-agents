---
title: "Pin prebuilt executables with rules_multitool"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_multitool": "1.11.1"}
platforms_verified: []
required_flags: []
prerequisites: []
claim_ids: ["multitool.hubs", "multitool.distributions", "multitool.targets", "multitool.merge"]
last_verified: "2026-11-05"
---

# Pin prebuilt executables with rules_multitool

Use this when the build needs an existing executable distribution, such as a
formatter or code generator. The reviewed release is `rules_multitool` 1.11.1.

## Describe the distribution in a lockfile

The JSON lockfile maps tool names to `binaries`. Each binary selects `os` and
`cpu`, a `kind`, a download URL, and distribution-specific fields. The inspected
platform vocabulary is Linux/macOS/Windows and x86_64/arm64. Archive and package
entries name the executable's path within the distribution.
[Schema][multitool-schema], [validation][multitool-lock].

Record a SHA-256 for every binary. Although the JSON schema's required-field list
omits `sha256`, the fetch implementation indexes that field and passes it to the
Bazel downloader. Follow the implementation and pin both URL and content.
[Fetch implementation][multitool-fetch].

## Create and expose a hub

Use `multitool` from `@rules_multitool//multitool:extension.bzl` and its `hub` tag.
The tag requires `lockfile`; `hub_name` defaults to `multitool`. The module imports
and registers that default hub's toolchains. A separately named hub needs its own
exposure and registration in the consuming module.
[Extension][multitool-extension], [default registration][multitool-module].

The generated tool target is under `@<hub>//tools/<name>:<name>`. It resolves a
toolchain, creates an executable symlink, and returns executable `DefaultInfo`.
The generated toolchain declarations include both execution-constrained and
target-constrained variants. [Generated target][multitool-target],
[implementation][multitool-tool], [toolchains][multitool-toolchains].

Our recommendation for a custom build action is to consume the executable through
an execution-configured tool attribute and declare its files/runfiles as the
action requires. A tool that runs during a cross build must be runnable where the
action executes, regardless of the architecture of the output it generates.

## Review merging and runtime assumptions

Lockfiles merge at whole-tool granularity: later tool-name entries overwrite
earlier ones. The extension controls the order in which module tags contribute
lockfiles. There is no version-aware conflict solver in that merge function.
Avoid accidental shared tool names; inspect the final generated hub when modules
contribute the same name. [Merge][multitool-lock], [tag order][multitool-extension].

The generated `cwd` and `workspace_root` wrappers are separate targets intended
to run the tool in those locations. Do not automatically use a working-directory
wrapper as an action tool; choose the action's input and working-directory
contract deliberately. [Generated wrappers][multitool-target].

Downloading a pinned executable does not establish that its dynamic libraries,
SDK, or other runtime requirements exist on a worker. Our validation recommendation
is to execute it under each supported execution environment before describing the
tool integration as hermetic or remotely executable.

## Verification boundary

The cited release sources were inspected. No local Bazel 9.3.1 integration run or
resolved transitive dependency graph is recorded for this page. Treat the version
selection as a source-reviewed candidate, not a tested combination. See the
[claim ledger](../../verification/rulesets-rust-proto-utilities.md).

[multitool-extension]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/extension.bzl
[multitool-module]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/MODULE.bazel
[multitool-schema]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/lockfile.schema.json
[multitool-lock]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/lockfile.bzl
[multitool-toolchains]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_template/toolchain_info.bzl.template
[multitool-target]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_tool_template/BUILD.bazel.template
[multitool-tool]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_tool_template/tool.bzl.template
[multitool-fetch]: https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/multitool.bzl
