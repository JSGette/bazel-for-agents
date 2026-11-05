---
title: "Understand invocations and rc configuration"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["configuration.invocation-boundary", "configuration.rc-discovery", "configuration.rc-imports", "configuration.rc-precedence", "configuration.named-configs", "configuration.rc-observability"]
last_verified: "2026-11-05"
---

# Understand invocations and rc configuration

Use this when a command behaves differently across machines, CI jobs, or working
sessions. Our recommendation is to inspect effective options before editing BUILD
files to compensate for an unexplained configuration difference.

## Put each option in the right part of the invocation

The command boundary separates startup options from command options. Startup
options precede the command name and affect client/server startup or rc discovery;
command options follow the command name. In rc files, `startup` lines contain the
former and command-specific sections contain the latter. An rc-discovery switch
cannot take effect merely by being placed after the command.
[Client option processing][client], [invocation syntax][guide]

This page describes option semantics, not a tested command template. Read the
project's launcher and Bazel version selection before assuming a program named
`bazel` is the bare binary used in a verification record.

## Know every source of rc options

Bazel 9.3.1 collects rc files in this order:

1. System rc, unless disabled with `--nosystem_rc`.
2. Project-root `.bazelrc`, next to `MODULE.bazel`, unless disabled with
   `--noworkspace_rc`.
3. User-home `.bazelrc`, unless disabled with `--nohome_rc`.
4. Paths from the `BAZELRC` environment variable, comma-separated.
5. Explicit `--bazelrc` paths, in occurrence order.

The first three standard files are optional. Paths explicitly supplied through
`BAZELRC` or `--bazelrc` are validated for readability. Imported files add to this
set. Inspect environment-provided paths as well as the repository's visible rc
file when reproducing a build. [Discovery and validation implementation][client]

`--bazelrc=/dev/null` stops processing subsequent explicit `--bazelrc` paths. It
does not disable standard rc discovery, earlier explicit paths, or `BAZELRC`.
`--ignore_all_rc_files` is the startup switch that skips rc loading altogether,
including explicitly supplied rc files. [Discovery control][client]

## Understand imports before reading precedence

`import` requires a readable imported file. `try-import` tolerates an absent or
unreadable file, but it still rejects malformed contents and import cycles.
`%workspace%/` resolves an import relative to the project root. Imports expand at
their position in the source; subsequent options at the same command specificity
can override imported scalar settings. [Import implementation][parser]

The current parser also accepts `try-import-if-bazel-version` with a version
condition and path. Its condition is checked before the optional import. Our
recommendation is to use this only when maintaining explicitly supported modern
Bazel versions that need different configuration; do not build a collection of
historical compatibility settings into generic guidance. [Conditional import parser][parser]

## Apply command specificity and flag semantics

| Section | Meaning |
| --- | --- |
| `startup` | Startup options |
| `common` | Options applied to commands that support them; a recognized option for another command can be ignored |
| `always` | Options applied to every command; unsupported options fail |
| Command name, such as `build` or `test` | Defaults for that command and commands inheriting its options |

A more-specific command section takes precedence over a less-specific one, so
`test` settings override inherited `build` settings regardless of their textual
order. At equal specificity, rc order applies. Ordinary command-line options have
higher parsing priority than unconditional rc defaults. Scalar flags generally
replace earlier values; repeatable flags can accumulate according to the option's
own definition. [Rc parsing and command inheritance][handler], [rc semantics][guide]

Do not turn this into a claim that a command-line value always controls the final
build configuration: [platform flags](platforms-and-constraints.md) and transitions
operate later. Invocation policies can also enforce options after parsing.
[Option processing pipeline][handler]

## Expand named configurations deliberately

A `command:name` section defines a named config. `--config=name` expands applicable
sections in place, at that occurrence's precedence, and includes definitions from
all loaded rc files. Configs can include other configs; cycles are rejected.
Repeated expansion can repeat accumulating flags. A name is not scoped to one rc
file and does not select a platform unless its options do so.
[Expansion implementation][expander], [config option][options]

General named configs do not set startup options. There is a separate host-OS
startup mechanism: `startup:linux`, `startup:macos`, and the other supported host-OS
sections are automatically considered by the client. For command sections, host-OS
selection is controlled by `--enable_platform_specific_config`, whose 9.3.1 default
is false. This uses the host OS, not the target platform.
[Startup host-OS sections][client], [command flag default][options]

## Observe configuration without changing its meaning

`--announce_rc` reports applied rc options and config expansion notes. It defaults
to false. Our recommendation is to record the selected Bazel binary/version, full
argument boundaries, relevant rc paths and named configs, and non-secret environment
inputs when investigating a difference. Review logs before sharing them when rc
files contain authentication options. [Reporting option][options], [reporting pipeline][handler]

A probe with `--ignore_all_rc_files` answers a question about controlled defaults;
it does not reproduce a project invocation that relies on rc-selected platforms,
features, or remote services. Conversely, inheriting personal rc files can conceal
a missing declaration. Choose the mode deliberately and record it with results.
Disabling rc loading can also remove injected reporting or authentication options,
which matters for the deferred [CI verification work](https://github.com/JSGette/bazel-for-agents/issues/1).

## Evidence scope

Source review at Bazel 9.3.1; no rc integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Platform and
user-home paths vary by operating system; this page does not claim an OS matrix.

[client]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/option_processor.cc
[parser]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/rc_file.cc
[options]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/CommonCommandOptions.java
[handler]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/BlazeOptionHandler.java
[expander]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/ConfigExpander.java
[guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/run/bazelrc.md
