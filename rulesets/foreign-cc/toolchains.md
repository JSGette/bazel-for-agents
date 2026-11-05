---
title: "Select foreign-build tools and C++ compilation together"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_foreign_cc": "0.17.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["foreign.tools.extension", "foreign.tools.modes", "foreign.tools.execution", "foreign.tools.cmake"]
last_verified: "2026-11-05"
---

# Select foreign-build tools and C++ compilation together

Use this when choosing CMake/Make/Ninja and the compiler used inside an external
build. A build-system executable and a target compiler are separate tools that
must run on a compatible execution platform.

## Use the current module extension

The public extension is `tools` from
`@rules_foreign_cc//foreign_cc:extensions.bzl`. Tool-specific tags such as
`cmake`, `ninja`, and `make` take `mode`, optional `version`, execution/target
constraints, `register_toolchain`, and a `target` for custom tools. The schema
admits `system`, `binary`, `source`, `custom`, and `noop`; validation restricts
which modes each tool supports. Do not assume every tool supports every mode.
[Extension][extension], [tool specifications][specs], [validation][planner]

`custom` uses a declared target. `system` represents an executor-provided tool;
it is not converted into a pinned distribution merely by being a toolchain.
Choose binary/source/custom integrations when their declared inputs meet the
project's portability requirements. [Tool specifications][specs]

The extension publishes `rules_foreign_cc_toolchains`; this ruleset's own module
registers the hub's `:all` pattern. Root tags with registration enabled take
priority over defaults. Non-root tags can request repositories but do not add
registrations to the hub. A root `tools.explicit()` suppresses the defaults,
leaving only root-requested registrations. [Precedence implementation][extension],
[registration plan][planner]

## Preserve execution consistency

The adapters use a named `foreign_cc` execution group to resolve tools together.
The CMake rule requests its build-tool types and C++ toolchain through that
framework. The build action uses the same group; build-time dependencies are
configured for it. Do not select a CMake executable for one machine while
expecting its nested compiler process to run on another. [Execution group][groups],
[CMake declaration][cmake]

CMake receives compiler paths, toolchain flags, and target information. Its
`generate_crosstool_file` option defaults to true. The rule documents
`CMAKE_SYSTEM_NAME` as required when using that option for cross-compilation;
a supplied `CMAKE_TOOLCHAIN_FILE` uses the supplied file instead. Review the
resulting configuration script and selected toolchain rather than replacing
compiler settings with ambient `CC`/`CXX`. [CMake configuration][cmake]

Continue with [hermeticity](hermeticity.md).

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[extension]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/extensions.bzl
[planner]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/extension_impl.bzl
[specs]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/tool_specs.bzl
[groups]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework/exec_groups.bzl
[cmake]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/cmake.bzl
