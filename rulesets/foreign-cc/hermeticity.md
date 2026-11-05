---
title: "Audit foreign builds for declared inputs and stable outputs"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_foreign_cc": "0.17.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["foreign.hermetic.environment", "foreign.hermetic.interface", "foreign.hermetic.debugging"]
last_verified: "2026-11-05"
---

# Audit foreign builds for declared inputs and stable outputs

Use this when a foreign build succeeds locally but fails on another worker,
misses the cache, or produces different artifacts.

## Trace every tool and discovery path

Our review recommendation is to inventory the external system's configure-time
probes, generated files, subprocesses, environment, downloads, and installed
outputs. Supply dependencies through declared labels and the selected toolchain.
Replace uncontrolled dependency fetching inside the build with explicit external
repository inputs where the upstream build supports that configuration.

The framework's action sets `use_default_shell_env = True` and supplies its own
constructed environment. Therefore a foreign-build wrapper is not, by itself,
proof that all environment inputs are pinned. Its `env` supports `$(execpath)`
for declared dependency files and converts those to absolute paths because the
build is not run at the execution-root directory. Variables containing `PATH`
are prepended to existing values. [Environment implementation][framework]

## Separate build settings from exported interface settings

The shared `includes` and `defines` attributes describe information passed to
Bazel consumers. The schema explicitly says they are not passed to the foreign
compiler; configure the external build itself through its adapter options as
well. An exported `CcInfo` can otherwise describe an interface that the actual
foreign compilation did not use. [Shared attribute contracts][framework]

Likewise, declare the installed files with the output attributes described in
[setup](setup.md). This release enables
`experimental_validate_outputs_in_action` by default, validating expected
installed outputs before the main action exits. That detects missing declared
outputs; it does not establish their contents or ABI. [Output validation][framework]

## Inspect evidence from the failing action

The framework adds output groups named for the configure adapter plus `_logs`,
containing the generated build script, log, and wrapper script. Inspect these
alongside the actual action inputs, environment, tools, and outputs.
[Debug-output construction][framework]

For repeatability, compare installed artifacts from controlled builds and
inspect embedded source/build paths. `set_file_prefix_map` can request a prefix
map for supported compiler paths; its schema says it has no effect on MSVC.
Do not equate that one setting, sandboxing, or a cache hit with complete
reproducibility. [Prefix-map setting][framework]

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[framework]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl
