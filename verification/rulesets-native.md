# Native ruleset source evidence

Observed 2026-11-05. Editorial floor: Bazel 9.3.1. Each ruleset page records the
exact release whose source was inspected. Except for the named Bazel core APIs
on the Windows process page, this batch is ruleset-source review, not a claim
of a successful Bazel 9.3.1 integration. No resolved module graph, compiler/SDK
execution, upstream test run, remote service, or platform matrix was exercised.

## Source identity

Release archives were downloaded and their SHA-256 integrity compared with the
pinned BCR `source.json`. Tags were resolved to the commits below. Registry
module metadata and patches are part of the source identity; the raw upstream
module file alone is not the resolved dependency graph.

| Module | BCR version | Upstream tag | Commit |
| --- | --- | --- | --- |
| rules_cc | [0.2.27](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_cc/0.2.27/source.json) | `0.2.27` | [11976124184a](https://github.com/bazelbuild/rules_cc/tree/11976124184a79bfecaedf6ff5cbf2f17f815a21) |
| rules_shell | [0.8.0](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_shell/0.8.0/source.json) | `v0.8.0` | [c02969a18221](https://github.com/bazel-contrib/rules_shell/tree/c02969a1822191a179cd70c0cedd076385446a26) |
| rules_pkg | [1.3.0](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_pkg/1.3.0/source.json) | `1.3` | [c62b199e2411](https://github.com/bazelbuild/rules_pkg/tree/c62b199e2411cb1f4ea3af4d01f743df1be135cb) |
| rules_foreign_cc | [0.17.0](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_foreign_cc/0.17.0/source.json) | `0.17.0` | [aa554e6002e6](https://github.com/bazel-contrib/rules_foreign_cc/tree/aa554e6002e686a95ef08d93f2f205c4d299c8e0) |
| llvm | [0.8.26](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/source.json) | `v0.8.26` | [53ff474eae0a](https://github.com/hermeticbuild/hermetic-llvm/tree/53ff474eae0a3e617ce615dec635c4b38db495c8) |
| gcc_toolchain | [0.13.0](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/gcc_toolchain/0.13.0/source.json) | `0.13.0` | [310058832146](https://github.com/f0rmiga/gcc-toolchain/tree/310058832146d3e080bb2bf182ccb54240c2cd3a) |
| apple_support | [2.11.0](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/apple_support/2.11.0/source.json) | `2.11.0` | [373df5ad8e5d](https://github.com/bazelbuild/apple_support/tree/373df5ad8e5de7ced7e05a16c57406856f01ee06) |

Bazel source: [`fee2bf2d1c14bc2096068a4d46f1842472092044`](https://github.com/bazelbuild/bazel/tree/fee2bf2d1c14bc2096068a4d46f1842472092044), release 9.3.1.

## Claim records

All records below are **source-verified**. Fixture, commands, expected runtime
result, observed runtime result, and platforms are not supplied for this batch.
Recommendations in the pages are editorial choices; API constraints and defaults
are bounded by the sources linked here. Executable claim verification and
BuildBuddy integration are tracked in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

### cc.setup.exports

Page: [rulesets/cc/setup.md](../rulesets/cc/setup.md).

rules_cc exports C/C++ rules, CcInfo and cc_common through explicit public .bzl entry points.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/defs.bzl).

### cc.setup.local

Page: [rulesets/cc/setup.md](../rulesets/cc/setup.md).

The module instantiates local C++ configuration and registers its generated toolchains.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_cc/0.2.27/MODULE.bazel), [source 2](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/cc_configure.bzl).

### cc.setup.custom

Page: [rulesets/cc/setup.md](../rulesets/cc/setup.md).

Custom rules can request and retrieve the C++ toolchain through use_cc_toolchain and find_cc_toolchain.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/use_cc_toolchain.bzl), [source 2](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/find_cc_toolchain.bzl).

### cc.targets.headers

Page: [rulesets/cc/targets.md](../rulesets/cc/targets.md).

Public headers, private sources, textual headers and include path rewriting have distinct attributes.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_library.bzl).

### cc.targets.dependencies

Page: [rulesets/cc/targets.md](../rulesets/cc/targets.md).

implementation_deps restricts compile-interface propagation while retaining linking dependencies.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_library.bzl).

### cc.targets.flags

Page: [rulesets/cc/targets.md](../rulesets/cc/targets.md).

copts/local_defines and includes/defines have different propagation contracts.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/attrs.bzl).

### cc.targets.providers

Page: [rulesets/cc/targets.md](../rulesets/cc/targets.md).

CcInfo separates compilation and linking contexts.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/cc_info.bzl).

### cc.linking.static

Page: [rulesets/cc/linking.md](../rulesets/cc/linking.md).

linkstatic and alwayslink control different linking behavior; linkstatic does not alone guarantee a fully static executable.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/attrs.bzl), [source 2](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_library.bzl).

### cc.linking.import

Page: [rulesets/cc/linking.md](../rulesets/cc/linking.md).

cc_import models static/shared/interface artifacts and checks system_provided combinations.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_import.bzl).

### cc.linking.shared

Page: [rulesets/cc/linking.md](../rulesets/cc/linking.md).

cc_shared_library uses CcSharedLibraryInfo dynamic dependencies and analysis-time exports accounting, not a symbol-export script.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_shared_library.bzl).

### shell.setup.exports

Page: [rulesets/shell/setup.md](../rulesets/shell/setup.md).

Public sh_binary, sh_library and sh_test have separate .bzl exports.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_binary.bzl), [source 2](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_library.bzl), [source 3](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/sh_test.bzl).

### shell.setup.discovery

Page: [rulesets/shell/setup.md](../rulesets/shell/setup.md).

rules_shell registers local shell configuration from its module.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_shell/0.8.0/MODULE.bazel), [source 2](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/extensions/sh_configure.bzl).

### shell.setup.toolchain

Page: [rulesets/shell/setup.md](../rulesets/shell/setup.md).

The shell runtime toolchain carries an absolute interpreter path and Windows launcher dependencies.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/toolchains/sh_toolchain.bzl).

### shell.targets.inputs

Page: [rulesets/shell/targets.md](../rulesets/shell/targets.md).

Shell executables require exactly one source file, aggregate ShInfo dependencies, and collect data/runfiles.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_executable.bzl), [source 2](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_library.bzl).

### shell.targets.launcher

Page: [rulesets/shell/targets.md](../rulesets/shell/targets.md).

use_bash_launcher generates a wrapper initializing runfiles; shell execution otherwise retains source/launcher semantics.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_executable.bzl).

### shell.targets.environment

Page: [rulesets/shell/targets.md](../rulesets/shell/targets.md).

env and env_inherit contribute RunEnvironmentInfo.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_executable.bzl).

### shell.runfiles.lookup

Page: [rulesets/shell/runfiles.md](../rulesets/shell/runfiles.md).

The Bash runfiles library supports directory and manifest lookup and repository mapping.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/runfiles/runfiles.bash).

### shell.runfiles.context

Page: [rulesets/shell/runfiles.md](../rulesets/shell/runfiles.md).

rlocation takes an optional source repository context; runfiles_current_repository and runfiles_export_envvars support mapping and child process setup.

Evidence: [source 1](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/runfiles/runfiles.bash).

### pkg.mappings.providers

Page: [rulesets/packaging/file-mappings.md](../rulesets/packaging/file-mappings.md).

pkg_files creates packaging providers, not an archive, and pkg_filegroup composes mappings.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl), [source 2](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/providers.bzl).

### pkg.mappings.paths

Page: [rulesets/packaging/file-mappings.md](../rulesets/packaging/file-mappings.md).

strip_prefix, prefix and renames control destination paths; tree-artifact handling has explicit boundaries.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl).

### pkg.mappings.links

Page: [rulesets/packaging/file-mappings.md](../rulesets/packaging/file-mappings.md).

pkg_mkdirs and pkg_mklink represent directory metadata and symbolic links.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl).

### pkg.archives.exports

Page: [rulesets/packaging/archives.md](../rulesets/packaging/archives.md).

pkg_tar, pkg_zip, pkg_deb and pkg_rpm have public format-specific entry points.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/tar.bzl), [source 2](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/zip.bzl), [source 3](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/deb.bzl), [source 4](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/rpm.bzl).

### pkg.archives.composition

Page: [rulesets/packaging/archives.md](../rulesets/packaging/archives.md).

pkg_tar.srcs packages files/mappings while deps unpacks and repacks tar archives; package_dir applies last.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/tar/tar.bzl).

### pkg.archives.outputs

Page: [rulesets/packaging/archives.md](../rulesets/packaging/archives.md).

package_file_name changes the actual artifact name and the default output becomes a symlink.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/util.bzl).

### pkg.archives.collisions

Page: [rulesets/packaging/archives.md](../rulesets/packaging/archives.md).

Tar and zip default to permissive different-content duplicates; explicit rejection is available.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/tar/tar.bzl), [source 2](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/zip/zip.bzl).

### pkg.metadata.permissions

Page: [rulesets/packaging/metadata.md](../rulesets/packaging/metadata.md).

pkg_attributes is the supported mapping-metadata constructor; file/directory/link mode defaults differ.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/mappings.bzl).

### pkg.metadata.timestamps

Page: [rulesets/packaging/metadata.md](../rulesets/packaging/metadata.md).

Tar and zip stamp controls and timestamp defaults have explicit semantics.

Evidence: [source 1](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/tar/tar.bzl), [source 2](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/pkg/private/zip/zip.bzl).

### pkg.metadata.rpm

Page: [rulesets/packaging/metadata.md](../rulesets/packaging/metadata.md).

RPM toolchain discovery in the rules_pkg module is a development-only registration.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_pkg/1.3.0/MODULE.bazel), [source 2](https://github.com/bazelbuild/rules_pkg/blob/c62b199e2411cb1f4ea3af4d01f743df1be135cb/toolchains/rpm/rpmbuild_configure.bzl).

### foreign.setup.exports

Page: [rulesets/foreign-cc/setup.md](../rulesets/foreign-cc/setup.md).

The public defs entry point exports CMake, configure/make, make, Meson, Ninja, MSBuild and Boost adapters.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/defs.bzl).

### foreign.setup.inputs

Page: [rulesets/foreign-cc/setup.md](../rulesets/foreign-cc/setup.md).

lib_source supplies source inputs, deps requires CcInfo, build_data is exec-configured and data is target-configured.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl).

### foreign.setup.outputs

Page: [rulesets/foreign-cc/setup.md](../rulesets/foreign-cc/setup.md).

Installed output declarations produce DefaultInfo, output groups, foreign-build metadata and CcInfo. The default static-library fallback applies only without header-only intent and without static/shared/interface libraries, binaries, or out_data_files; out_data_dirs alone does not suppress it.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl).

### foreign.setup.cmake

Page: [rulesets/foreign-cc/setup.md](../rulesets/foreign-cc/setup.md).

CMake configuration, build and install settings are distinct, and installation defaults on.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/cmake.bzl).

### foreign.tools.extension

Page: [rulesets/foreign-cc/toolchains.md](../rulesets/foreign-cc/toolchains.md).

The tools extension generates a hub with root registrations and defaults; explicit suppresses defaults.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/extensions.bzl), [source 2](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/extension_impl.bzl).

### foreign.tools.modes

Page: [rulesets/foreign-cc/toolchains.md](../rulesets/foreign-cc/toolchains.md).

Tool tags expose validated system/binary/source/custom/noop modes, version, constraints and registration controls.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/extensions.bzl), [source 2](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/tool_specs.bzl), [source 3](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/extension_impl.bzl).

### foreign.tools.execution

Page: [rulesets/foreign-cc/toolchains.md](../rulesets/foreign-cc/toolchains.md).

Foreign build adapters resolve their requested tools in a shared named execution group.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework/exec_groups.bzl), [source 2](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/cmake.bzl).

### foreign.tools.cmake

Page: [rulesets/foreign-cc/toolchains.md](../rulesets/foreign-cc/toolchains.md).

CMake receives compiler/toolchain data and supports generated toolchain files, with explicit cross-compilation settings.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/cmake.bzl).

### foreign.hermetic.environment

Page: [rulesets/foreign-cc/hermeticity.md](../rulesets/foreign-cc/hermeticity.md).

The foreign action uses default shell environment and constructs an explicit environment; env path expansion has special behavior.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl).

### foreign.hermetic.interface

Page: [rulesets/foreign-cc/hermeticity.md](../rulesets/foreign-cc/hermeticity.md).

includes and defines describe downstream compilation interfaces rather than configuring the foreign compiler.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl).

### foreign.hermetic.debugging

Page: [rulesets/foreign-cc/hermeticity.md](../rulesets/foreign-cc/hermeticity.md).

Output groups expose configure-specific logs/scripts and output validation runs within the action by default.

Evidence: [source 1](https://github.com/bazel-contrib/rules_foreign_cc/blob/aa554e6002e686a95ef08d93f2f205c4d299c8e0/foreign_cc/private/framework.bzl).

### llvm.setup.identity

Page: [rulesets/llvm/setup.md](../rulesets/llvm/setup.md).

The llvm module names hermeticbuild/hermetic-llvm, and its module version is separate from its LLVM source/compiler selection.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/llvm.bzl).

### llvm.setup.registration

Page: [rulesets/llvm/setup.md](../rulesets/llvm/setup.md).

The public toolchain package declares execution/target pairs; an extension can publish a selected subset.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/toolchain.bzl).

### llvm.setup.version

Page: [rulesets/llvm/setup.md](../rulesets/llvm/setup.md).

The llvm extension gives the root version request precedence and requires source-index entries.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/llvm.bzl).

### llvm.runtime.model

Page: [rulesets/llvm/sysroots.md](../rulesets/llvm/sysroots.md).

The integration provides target runtime components and libc/C++ runtime constraints rather than requiring one arbitrary sysroot path.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/constraints/libc/libc_versions.bzl), [source 3](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/constraints/cxxstdlib/BUILD.bazel).

### llvm.runtime.glibc

Page: [rulesets/llvm/sysroots.md](../rulesets/llvm/sysroots.md).

Explicit libc constraints and perarchitecture defaults distinguish glibc ABI choices.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/constraints/libc/libc_versions.bzl).

### llvm.runtime.apple

Page: [rulesets/llvm/sysroots.md](../rulesets/llvm/sysroots.md).

The osx extension selects archived SDK inputs or host discovery, with host selection restricted to macOS.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/extensions/osx.bzl), [source 2](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel).

### llvm.runtime.windows

Page: [rulesets/llvm/sysroots.md](../rulesets/llvm/sysroots.md).

Windows GNU and MSVC ABIs use distinct constraint/runtime paths, including explicit Microsoft input license gates.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md), [source 2](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel).

### llvm.cross.pairs

Page: [rulesets/llvm/cross-compilation.md](../rulesets/llvm/cross-compilation.md).

Supported execution and target tables are separate; toolchain declarations pair them with constraints.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/platforms/common.bzl), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl).

### llvm.cross.abi

Page: [rulesets/llvm/cross-compilation.md](../rulesets/llvm/cross-compilation.md).

Windows MSVC selection uses distinct target settings and ABI-specific tool configuration.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md).

### llvm.cross.ffi

Page: [rulesets/llvm/cross-compilation.md](../rulesets/llvm/cross-compilation.md).

The pinned integration documents Go compiler and Rust native-linking constraints beyond general C++ target support.

Evidence: [source 1](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md).

### gcc.setup.extension

Page: [rulesets/gcc/setup.md](../rulesets/gcc/setup.md).

Only root module toolchain tags create GCC repositories; each specifies a target architecture and optional compiler version.

Evidence: [source 1](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/module_extensions.bzl).

### gcc.setup.distribution

Page: [rulesets/gcc/setup.md](../rulesets/gcc/setup.md).

Compiler archives are URL/hash pinned and the default GCC compiler version is16.2.0, separate from module0.13.0.

Evidence: [source 1](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/defs.bzl).

### gcc.setup.registration

Page: [rulesets/gcc/setup.md](../rulesets/gcc/setup.md).

Consumers must import/register generated toolchains; own module registrations are development-only.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/gcc_toolchain/0.13.0/MODULE.bazel), [source 2](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/module_extensions.bzl).

### gcc.cross.execution

Page: [rulesets/gcc/cross-compilation.md](../rulesets/gcc/cross-compilation.md).

Generated GCC and Fortran registrations constrain execution to Linux x86_64.

Evidence: [source 1](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/defs.bzl).

### gcc.cross.target

Page: [rulesets/gcc/cross-compilation.md](../rulesets/gcc/cross-compilation.md).

The target defaults are Linux plus the selected architecture; extension supports extra constraints and target settings.

Evidence: [source 1](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/defs.bzl), [source 2](https://github.com/f0rmiga/gcc-toolchain/blob/310058832146d3e080bb2bf182ccb54240c2cd3a/toolchain/module_extensions.bzl).

### apple.setup.scope

Page: [rulesets/apple/setup.md](../rulesets/apple/setup.md).

apple_support supplies Apple C++ toolchains, constraints/platforms and rule-author helpers; application bundling and Swift are separate rulesets.

Evidence: [source 1](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/README.md).

### apple.setup.module

Page: [rulesets/apple/setup.md](../rulesets/apple/setup.md).

The module configures/registers local Apple C++ toolchains and configures Xcode discovery.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/apple_support/2.11.0/MODULE.bazel), [source 2](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/crosstool/setup.bzl), [source 3](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/xcode/xcode_configure.bzl).

### apple.setup.actions

Page: [rulesets/apple/setup.md](../rulesets/apple/setup.md).

apple_support action helpers combine Xcode environment and execution requirements; run supports path placeholder processing.

Evidence: [source 1](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/lib/apple_support.bzl).

### apple.platform.constraints

Page: [rulesets/apple/platforms.md](../rulesets/apple/platforms.md).

Apple helpers inspect OS, CPU and device/simulator constraints, including pointer authentication for arm64e.

Evidence: [source 1](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/lib/apple_support.bzl), [source 2](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/platforms/BUILD), [source 3](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/constraints/BUILD).

### apple.platform.xcode

Page: [rulesets/apple/platforms.md](../rulesets/apple/platforms.md).

Xcode config may describe local and remote available versions; mutually available selection does not install Xcode.

Evidence: [source 1](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/xcode/xcode_config.bzl).

### apple.platform.actions

Page: [rulesets/apple/platforms.md](../rulesets/apple/platforms.md).

Apple actions receive Xcode-specific execution information through helper composition.

Evidence: [source 1](https://github.com/bazelbuild/apple_support/blob/373df5ad8e5de7ced7e05a16c57406856f01ee06/lib/apple_support.bzl).

### windows.tools.discovery

Page: [rulesets/windows/toolchain-selection.md](../rulesets/windows/toolchain-selection.md).

rules_cc local configuration searches Visual C++ installations and consumes compiler/SDK version environment selections.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/cc_configure.bzl), [source 2](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/toolchain/windows_cc_configure.bzl).

### windows.tools.llvm

Page: [rulesets/windows/toolchain-selection.md](../rulesets/windows/toolchain-selection.md).

The llvm integration has a separate explicit MSVC ABI path configured with windows_support runtime/SDK inputs.

Evidence: [source 1](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/llvm/0.8.26/MODULE.bazel), [source 2](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/toolchain/declare_toolchains.bzl), [source 3](https://github.com/hermeticbuild/hermetic-llvm/blob/53ff474eae0a3e617ce615dec635c4b38db495c8/README.md).

### windows.tools.imports

Page: [rulesets/windows/toolchain-selection.md](../rulesets/windows/toolchain-selection.md).

cc_import distinguishes import libraries from runtime shared libraries and checks system_provided.

Evidence: [source 1](https://github.com/bazelbuild/rules_cc/blob/11976124184a79bfecaedf6ff5cbf2f17f815a21/cc/private/rules_impl/cc_import.bzl).

### windows.process.actions

Page: [rulesets/windows/paths-and-processes.md](../rulesets/windows/paths-and-processes.md).

Bazel run takes executable and argument values while run_shell interprets a command through a shell.

Evidence: [source 1](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java).

### windows.process.genrule

Page: [rulesets/windows/paths-and-processes.md](../rulesets/windows/paths-and-processes.md).

Genrule has distinct Windows Batch and PowerShell command attributes with documented precedence.

Evidence: [source 1](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/genrule/GenRuleBaseRule.java).

### windows.process.runfiles

Page: [rulesets/windows/paths-and-processes.md](../rulesets/windows/paths-and-processes.md).

enable_runfiles is a tri-state setting with Windows default off; shell library supports manifest lookup.

Evidence: [source 1](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java), [source 2](https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/runfiles/runfiles.bash).

### windows.process.paths

Page: [rulesets/windows/paths-and-processes.md](../rulesets/windows/paths-and-processes.md).

output_user_root and windows_enable_symlinks are startup options; symlink mode needs OS support.

Evidence: [source 1](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/startup_options.cc), [source 2](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/configure/windows.md).

## Compatibility boundaries

- `rules_cc` may dispatch public wrappers through a compatibility proxy; review its selected implementation together with the actual Bazel version when running fixtures.
- `rules_shell` uses a runtime interpreter path; declaring the ruleset does not pin a shell distribution.
- `rules_pkg` archive metadata and tool dependencies need execution-level checks before reproducibility claims.
- `rules_foreign_cc` exposes current module-based tool selection but still needs the foreign project, its tools, and environment audited together.
- `llvm` source selection, prebuilt/compiler stages, target runtimes, SDKs, and Go/Rust integration must be tested as a combination.
- `gcc_toolchain` accepts several target architectures but its generated execution constraints are Linux x86_64.
- Apple and Windows provisioning, licensing gates, runtime behavior, and signing/deployment have not been exercised.
- `windows_support` appears as an LLVM dependency; this batch does not promote it to an independently verified ruleset baseline.
