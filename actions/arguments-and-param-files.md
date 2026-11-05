---
title: "Build action arguments and parameter files"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["actions/declaring-actions.md", "starlark/depsets.md"]
claim_ids: ["actions.args.lazy", "actions.args.tokens", "actions.args.mapping", "actions.args.params", "actions.args.dependencies", "actions.args.shell"]
last_verified: "2026-11-05"
---

# Build action arguments and parameter files

Use this page when a rule constructs a tool invocation, especially one with
transitive inputs or a command line that can grow large.

## Preserve tokens and defer transitive expansion

Create an `Args` object with `ctx.actions.args()` and pass it in the action's
`arguments` list. The object can retain depsets and their transformations until
command-line construction for execution. This avoids eagerly copying transitive
arguments into analysis-time lists. [Args API][args]

| Need | API and boundary |
| --- | --- |
| One value, optionally preceded by a flag | `add()`; use strings or individual files, not a list or directory. |
| A sequence of separate tokens | `add_all()`; accepts a list, tuple, or depset. |
| One argument containing joined values | `add_joined()`; choose the delimiter required by the tool. |

A `File` normally becomes its `path`; string values remain strings. Formatting
patterns take exactly one `%s` placeholder. Prefer these operations over building
one shell-like command string for a program that expects separate arguments.
[Conversion and method contracts][args]

A file's presence in `Args` is not an input declaration. Register every file the
action reads through the action's `inputs` or `tools` interface as appropriate.
[Action parameter contracts][actions]

## Control transformations explicitly

`add_all()` expands directory values by default, then applies `map_each`, then
per-item formatting and optional duplicate removal. `before_each` adds a separate
prefix token before each resulting argument. Empty results omit the optional
argument name and terminator by default; `omit_if_empty = False` changes that.
`uniquify` defaults to `False`. [Processing order and defaults][args]

A `map_each` function may return a string, `None` to filter an item, or a list of
strings to produce several arguments. Use a top-level function: nested closures
are rejected unless `allow_closure` is enabled, and can retain large analysis
objects. A second callback parameter can receive a `DirectoryExpander` when
manual directory expansion is needed. `print()` inside this deferred callback
does not produce visible output. [Callback contract][args]

Our recommendation: use formatting options for simple formatting and reserve
`map_each` for actual transformations. Document whether the tool cares about
argument order or repetition before enabling deduplication.

## Match the tool's response-file parser

`use_param_file()` permits an `Args` object to spill into a parameter file; its
format string specifies how the file path appears in the invocation. With
`use_always = False`, Bazel decides based on the system and argument length.
`use_always = True` forces spilling. The tool must understand the resulting
argument and file syntax; Bazel does not change the tool's parser. [API][args]

`set_param_file_format()` chooses among these formats: [API][args]

| Format | Representation |
| --- | --- |
| `shell` (default) | One shell-quoted item per line. |
| `multiline` | One verbatim item followed by a newline. |
| `flag_per_line` | `--` flags only, with associated values joined using `=`. Intended for the Abseil flags format. |

Choose based on the actual tool, especially for whitespace, literal quotes,
backslashes, newlines, and arguments that are not flags. Our recommendation is to
include those cases in the tool integration test. Parameter files may be elided
from the output tree; the API documents `--materialize_param_files` for inspection.
[API][args]

For `run_shell()`, argument indices refer to the flattened values, not to `Args`
objects. An `Args` object with unknown length makes later fixed indices
unpredictable. Prefer `run()` for a direct tool invocation; use the shell interface
only when shell behavior is part of the action. [Shell argument contract][actions]

Continue with [inputs, tools, and environment](inputs-tools-environment.md).

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[args]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/CommandLineArgsApi.java
[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
