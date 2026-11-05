---
title: "Expose build outputs and runtime files"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: ["linux-x86_64: foundation fixture only"]
required_flags: []
prerequisites: ["core/providers.md"]
claim_ids: [outputs.default-files, outputs.groups, outputs.runfiles, outputs.runfiles-construction, outputs.runfiles-merge, outputs.executable]
last_verified: "2026-11-05"
---

# Expose build outputs and runtime files

Use this page when a rule produces the right file but its consumers or runtime
cannot find it. Read [providers](providers.md) for the analysis-time interface.

## Choose the interface by purpose

| Purpose | Interface | Meaning |
| --- | --- | --- |
| Build the target's normal results | `DefaultInfo(files = ...)` | A depset of the target's default output files. [API][default-info] |
| Request an additional named collection of outputs | `OutputGroupInfo(...)` | Named output groups selectable with `--output_groups`. [Guide][groups] |
| Pass a particular artifact and its meaning to another rule | A custom provider | An explicit interface for the consumer. [Guide][providers] |
| Supply files needed at runtime | `DefaultInfo(runfiles = ...)` | A runfiles object describing runtime dependencies. [API][default-info] |
| Identify what to execute for an executable or test rule | `DefaultInfo(executable = ...)` | The executable artifact, for a rule declared executable or a test. [API][default-info] |

These interfaces serve different purposes. In particular, a runfiles object is
not the target's default-output depset, and an output group is not a substitute
for a consumer's semantic provider contract. [Runfiles API][runfiles-api],
[output-group guidance][groups]

## Set default outputs explicitly

Our recommendation for a file-producing custom rule is to return the intended
default outputs explicitly in `DefaultInfo.files`. If `files` is omitted, Bazel's
documented default is the rule's predeclared outputs; it is not every artifact
declared inside the implementation. [DefaultInfo API][default-info]

For optional output collections, return a named field on `OutputGroupInfo`.
The [fixture](../examples/foundations/defs.bzl) returns the greeting as a default
output and metadata in the `metadata` group. The [execution record][execution]
shows that requesting the report did not materialize the metadata in a fresh
output directory; requesting the metadata group did. [Output selection][groups]

Pass a particular output to another rule through a documented custom provider
field. The fixture's consumer reads `source[GreetingInfo].message`, avoiding any
assumption about which default output appears first. This is our recommended
interface design; the [provider guide][providers] supplies the underlying API.

## Construct and propagate runfiles deliberately

Create a runfiles object with `ctx.runfiles(files = ...)` and pass it through
`DefaultInfo(runfiles = ...)`. A dependency's default runfiles are available as
`dependency[DefaultInfo].default_runfiles`. [Context API][ctx-runfiles],
[DefaultInfo API][default-info]

Merge the runfiles of dependencies whose files are needed at runtime. `merge()`
returns a new combined runfiles object. When combining many such objects, use
`merge_all()`; the API recommends this to avoid building deeply nested depsets.
Keep the returned object—merging is not an in-place mutation. [Runfiles API][runfiles-api]

The [fixture](../examples/foundations/defs.bzl) makes this distinction visible:

- The greeting's default files contain `greeting.txt`.
- Its runfiles contain `runtime.txt`.
- The report's action uses `greeting.txt` as its template input.
- The report also merges the greeting's runfiles for downstream use.

Those facts were checked by analysis assertions and a configured-target query.
The fixture does not execute a program that opens a runfile. [Observed results][execution]

## Verify and respect the boundary

Follow the exact commands in the [foundation record][execution] to build the
default output, inspect the report's runfiles, and request the metadata group.
The [claim record](../verification/core-outputs-actions.md) maps these results and
the source-only claims separately.

Executable startup, language-specific runfiles lookup, and platform-dependent
runtime layout need a separate example for the selected ruleset. Our recommendation
is to keep those concerns out of this basic provider example and avoid teaching a
hand-built runtime path as a universal recipe.

Continue with [declaring actions](../actions/declaring-actions.md) to connect
artifact declarations to the actions that produce them.

[default-info]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/DefaultInfoApi.java
[groups]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#requesting-output-files
[providers]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#custom-providers
[runfiles-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/RunfilesApi.java
[ctx-runfiles]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleContextApi.java#L469
[execution]: ../verification/foundations.md
