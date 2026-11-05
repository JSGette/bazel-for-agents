# Outputs and actions: claim record

Verified against Bazel 9.3.1, commit `fee2bf2d1c14bc2096068a4d46f1842472092044`,
on 2026-11-05. Source verification applies to the bounded statements below.
Runtime verification is limited to the [foundation fixture record](foundations.md),
which specifies the exact binary, flags, environment, commands, and results.
No external rulesets were selected for these examples.

| Claim ID | Statement | Primary evidence | Execution coverage |
| --- | --- | --- | --- |
| `outputs.default-files` | `DefaultInfo.files` is a depset of default outputs; its implicit default is predeclared outputs. | [DefaultInfo API][default] | Fixture asserts explicit default files; implicit fallback inspected in source only. |
| `outputs.groups` | `OutputGroupInfo` exposes named groups requested with `--output_groups`; custom providers are recommended for semantic consumer interfaces. | [Output groups][rules] | Metadata absent after initial report build and present after explicit group request. |
| `outputs.runfiles` | Runfiles describe runtime files separately from default build outputs. | [Runfiles API][runfiles], [DefaultInfo API][default] | Producer's default output and runtime file membership asserted separately. |
| `outputs.runfiles-construction` | `ctx.runfiles(files=...)` creates a runfiles object; `DefaultInfo(runfiles=...)` exposes it, and `default_runfiles` retrieves it. | [Context API][ctx], [DefaultInfo API][default] | Exercised by producer and consumer. |
| `outputs.runfiles-merge` | `merge` and `merge_all` return combined objects; the API recommends `merge_all` for many objects to avoid deep depsets. | [Runfiles API][runfiles] | One `merge` and its propagated contents checked; large merges not tested. |
| `outputs.executable` | `DefaultInfo.executable` identifies the executable for an executable or test rule. | [DefaultInfo API][default] | Source-only; no executable fixture. |
| `actions.declaration` | `declare_file` returns an artifact declaration requiring a separate producing action. | [Action API][actions] | Greeting, report, and metadata artifacts declared and built. |
| `actions.registration` | Rule implementations register actions during analysis; they cannot read generated file contents then. | [Rules guide][rules] | Observed graph matches fixture; prohibition on reading content is source-verified. |
| `actions.file-contract` | Generated files have a producing action; the guide specifies exactly one producer and requires writing declared outputs. | [Rules guide][rules] | Positive producer chain executed; missing-output failures not tested. |
| `actions.builtins` | `write` writes supplied text; `expand_template` substitutes template text at execution; `run` invokes an executable. | [Action API][actions] | `write` and generated-template expansion tested; `run` source-only. |
| `actions.inputs` | Inputs, tools, executable, arguments, and outputs have distinct roles in `run`; tools have documented runfiles handling. | [Action API][actions], [Rules guide][rules] | Source-only for subprocess actions; fixture checks built-in template inputs. |
| `actions.demand` | Registered actions need not execute if their outputs are not requested. | [Rules guide][rules] | Metadata action visible in `aquery` while its output was absent before explicit request. |

The pages' design recommendations are editorial choices, identified as such.
Fixture-specific examples point to the checked source and runtime record rather
than duplicating untested code. Source-only descriptions do not imply remote,
Windows, manifest-based runfiles, or language-ruleset validation.

[default]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/DefaultInfoApi.java
[runfiles]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/RunfilesApi.java
[ctx]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleContextApi.java#L469
[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[rules]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md
