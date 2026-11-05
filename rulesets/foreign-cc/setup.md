---
title: "Wrap an external native build with a Bazel contract"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_foreign_cc": "0.17.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["foreign.setup.exports", "foreign.setup.inputs", "foreign.setup.outputs", "foreign.setup.cmake"]
last_verified: "2026-11-05"
---

# Wrap an external native build with a Bazel contract

Use this when a dependency must retain its own native build system. Our
recommendation is to wrap that system with an explicit source, tool, dependency,
and installed-output contract.

The public `@rules_foreign_cc//foreign_cc:defs.bzl` exports `cmake`,
`configure_make`, `make`, `meson`, `meson_with_requirements`, `ninja`, `msbuild`,
and `boost_build`, along with selected variants and `runnable_binary`.
Choose the adapter matching the upstream build system. [Exports][defs]

## Model the boundary

| Attribute | Meaning |
| --- | --- |
| `lib_source` | Required target supplying the source tree to build. |
| `deps` | Native dependency targets providing `CcInfo`. |
| `build_data` | Build-time files/targets configured for the foreign build's execution group. |
| `data` | Target-configured runtime dependencies. |
| `out_static_libs`, `out_shared_libs`, `out_interface_libs` | Expected installed library filenames. |
| `out_binaries` | Expected installed executable filenames. |
| `out_data_files`, `out_data_dirs` | Additional installed files and directories. |
| `out_include_dir` | Installed header directory, default `include`. |
| `out_headers_only` | Explicit header-only output intent. |

[Shared schema and implementation][framework]

The rules expose installed outputs and `CcInfo` to Bazel consumers. Describe
what the external build installs, rather than guessing where its temporary
build tree happens to place a file. The framework assumes a default static
library only when `out_headers_only` is false and no static/shared/interface
library, binary, or `out_data_files` output is declared. `out_data_dirs` alone
does not suppress that fallback. [Output contract][framework]

## Keep CMake stages separate

For `cmake`, `cache_entries` supplies cache variables, `generate_args` configures
the generation command, `build_args` configures the build command, and
`install_args` configures installation. `install` defaults to true.
`working_directory` identifies a nested directory containing the main
`CMakeLists.txt` when the source root is not appropriate. [CMake schema][cmake]

Review [toolchain selection](toolchains.md) before adding compiler paths to
cache entries. Review [hermeticity](hermeticity.md) before assuming the wrapper
prevents host discovery or network downloads performed by the external build.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[defs]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/defs.bzl
[framework]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl
[cmake]: https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/cmake.bzl
