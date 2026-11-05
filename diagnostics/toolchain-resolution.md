---
title: "Diagnose toolchain selection"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md"]
claim_ids: ["diagnostics.toolchains.debug", "diagnostics.toolchains.layers"]
last_verified: "2026-11-05"
---

# Diagnose toolchain selection

## Use this when

Use this page when no toolchain matches or Bazel chooses a different one than
expected. Read [resolution](../toolchains/resolution.md) for the exact 9.3.1
selection behavior before changing registration order.

## Inspect the same configured target

`--toolchain_resolution_debug` accepts a regex filter for relevant toolchain types
or target labels. It is an analysis diagnostic flag, not a mechanism for selecting
a toolchain. Restrict it to the failing area to keep the evidence readable.
[PlatformOptions][platform]

Use [cquery](cquery.md) to confirm the target's configuration and transitions. Then
inspect these separate layers:

1. The rule's required and optional toolchain types, including execution-group
   membership.
2. Registered toolchain declarations and candidate execution platforms, including
   extra registrations from the effective command line.
3. Target constraints, execution constraints, and any platform restrictions on
   allowed toolchain types.
4. The selected implementation's provider contents and the action's executable.

These are the resolution inputs and outputs described in the
[source-verified toolchain pages](../toolchains/resolution.md). This ordering is
our diagnostic recommendation.

A matching compiler name is insufficient evidence. Verify that the tool runs on
the execution platform and produces code for the target platform. With multiple
execution groups, inspect the group used by the particular action; one rule can
resolve more than one execution context. [Cross-compilation](../toolchains/cross-compilation.md);
[execution groups](../toolchains/execution-groups.md)

## Coverage and next task

The debug flag and resolution behavior were source-reviewed. No compiler/toolchain
matrix was executed here. Continue with [aquery](aquery.md) for the resulting
action and [platform properties](../remote/platforms-and-properties.md) for remote
worker requirements.

## Evidence

[Diagnostics claim ledger](../verification/diagnostics.md).

[platform]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java
