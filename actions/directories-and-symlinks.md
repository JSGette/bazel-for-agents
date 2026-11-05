---
title: "Use directory artifacts and explicit symlink actions"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["actions/declaring-actions.md", "actions/arguments-and-param-files.md"]
claim_ids: ["actions.directory.declaration", "actions.directory.expansion", "actions.directory.mapping", "actions.symlink.file", "actions.symlink.path"]
last_verified: "2026-11-05"
---

# Use directory artifacts and explicit symlink actions

Use a directory artifact when one action produces a tree whose individual files
are not named in advance by the rule's ordinary analysis. Use individual declared
files when their identities are part of the rule's public contract.

## Distinguish a directory artifact from a path string

`ctx.actions.declare_directory()` declares a generated directory `File`. A producing
action is still required. Its expanded contents support regular files and
directories; the API does not support symlinks inside tree artifacts. Do not model
an arbitrary host directory by passing its absolute path to this constructor.
[Directory and symlink API][actions]

Ordinary rule analysis does not inspect the directory's generated file contents.
For a consumer action, `Args.add_all()` expands directory values to files by
default, during execution-time argument construction. Disable expansion when the
tool expects the directory path itself. Register the directory as an action input
as well as supplying the command-line argument. [Directory API][actions], [Args API][args]

Our recommendation: document whether a provider field contains a tree artifact
or individual files. The distinction affects command-line expansion and what a
consumer can know during analysis.

## Use directory mapping for per-file generated actions

Bazel 9.3.1 includes `ctx.actions.map_directory()`. It declares a template that,
after input directories have been built, invokes a Starlark implementation to
create actions producing files in the specified output directories. This is the
explicit API for this deferred action-creation pattern; it is not an ordinary
rule implementation reading generated output during analysis. [API][actions]

The API is experimental and gated by `--experimental_allow_map_directory`, whose
9.3.1 default is `true`. An explicit disabling configuration makes calls fail;
availability by default is not a stable-API guarantee.
[Flag definition][core-options], [gate implementation][action-impl]

The mapping interface has named dictionaries for input directories, output
directories, tools, and additional inputs. The implementation receives a
`template_ctx`, expanded input-directory objects, and the supplied mappings.
Additional parameters are restricted to strings, booleans, and integers. The
implementation must be a top-level function; lambdas and nested functions are
not accepted. [Callback and parameter definitions][actions]

Scheduling properties, execution group/toolchain selection, environment, mnemonic,
and resource estimates can be supplied for the generated actions. Keep the
callback's required tools and data in the explicit mappings instead of capturing
analysis state. [API][actions]

This page establishes the API's existence and contract. It does not claim a
locally executed mapping fixture or interoperability with a remote service.

## Choose which symlink dependency you mean

`ctx.actions.symlink()` requires exactly one of `target_file` or `target_path`.
These have different artifact and invalidation contracts. [API][actions]

| Intent | Declaration and action contract |
| --- | --- |
| Point to an artifact tracked by Bazel | Declare a file or directory output matching `target_file`'s type. Changes to the referent or its contents invalidate the output. |
| Produce the literal text of a symlink | Declare with `declare_symlink()` and provide `target_path`. Bazel preserves the path text without resolving it; a dangling link is permitted. |

`declare_symlink()` requires `--allow_unresolved_symlinks`, which defaults to
`true` in 9.3.1; explicitly disabling it rejects the declaration.
[Flag definition][core-options], [declaration gate][action-impl]

For `target_path`, no path normalization is applied. `target_type` may be `file`
or `directory`; it determines symlink versus junction creation on Windows and has
no effect on other operating systems. `is_executable` applies only to
`target_file` and checks executability instead of modifying permissions.
[Symlink API][actions]

Our recommendation: use an artifact-tracking symlink when the dependency is a
known build artifact. Use a literal symlink only when its path text is the
intended product, and test the consumer's filesystem/platform requirements.

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[args]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java
[core-options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java
[action-impl]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java
