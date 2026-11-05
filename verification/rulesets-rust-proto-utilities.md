# Rust, protobuf, and utility source verification

Observed: 2026-11-05. Editorial Bazel baseline: 9.3.1. All records below are
`source-verified`: exact release APIs and implementation were inspected. No
fixture commands were run for these pages, no complete module graph was resolved,
and no execution platform or compiler/runtime combination is validated here.
The Bazel version is a baseline requirement, not a ruleset integration result.

## Source identity

The selected registry entries come from BCR snapshot
`9bc19aec3357f320fc262ab71a8d054af6b6a74d`. Release archives were downloaded
and their SHA-256 values checked against each entry's `source.json` integrity.
GitHub release tags were resolved to the commits below for immutable API links.
Registry patches and manifest requests remain part of the published module
identity; upstream source alone is not the resolved dependency graph.

| Module | Source release | Upstream commit | Registry manifest |
| --- | --- | --- | --- |
| `rules_rs` | 0.2.1 | [99e2e1126523](https://github.com/hermeticbuild/rules_rs/tree/99e2e11265235c148a2acf4201f534829248784f) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rs/0.2.1/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rs/0.2.1/source.json) |
| `rules_rust` | 0.75.0 | [21234a3c7d71](https://github.com/bazelbuild/rules_rust/tree/21234a3c7d71e70f858e7e6d783138768b300e64) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rust/0.75.0/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rust/0.75.0/source.json) |
| `rules_rust_prost` | 0.75.0 | [21234a3c7d71](https://github.com/bazelbuild/rules_rust/tree/21234a3c7d71e70f858e7e6d783138768b300e64) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rust_prost/0.75.0/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_rust_prost/0.75.0/source.json) |
| `protobuf` | 36.2 | [2c74169b3406](https://github.com/protocolbuffers/protobuf/tree/2c74169b34066ceb8ddb6b882fcb3fb32d737a55) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/protobuf/36.2/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/protobuf/36.2/source.json) |
| `bazel_lib` | 3.7.2 | [904332fd1c97](https://github.com/bazel-contrib/bazel-lib/tree/904332fd1c978e1d84161c120b26533df279c3dc) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_lib/3.7.2/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_lib/3.7.2/source.json) |
| `bazel_skylib` | 1.9.2 | [3de43ed45e1c](https://github.com/bazelbuild/bazel-skylib/tree/3de43ed45e1c7923d53c4db56ca3de3e46601580) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_skylib/1.9.2/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_skylib/1.9.2/source.json) |
| `bazel_features` | 1.54.1 | [6f5b91edb290](https://github.com/bazel-contrib/bazel_features/tree/6f5b91edb290af78d50ea12c8c2db44d46f1fcde) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_features/1.54.1/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/bazel_features/1.54.1/source.json) |
| `rules_multitool` | 1.11.1 | [0be566f364df](https://github.com/bazel-contrib/rules_multitool/tree/0be566f364df52308bfb7629e888e5084c3f5a85) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_multitool/1.11.1/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/rules_multitool/1.11.1/source.json) |
| `with_cfg.bzl` | 1.0.2 | [9b8b10962419](https://github.com/fmeum/with_cfg.bzl/tree/9b8b10962419346889e528cbe57a539754489d57) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/with_cfg.bzl/1.0.2/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/with_cfg.bzl/1.0.2/source.json) |
| `re.bzl` | 0.4.1 | [aa210e888590](https://github.com/jvolkman/re.bzl/tree/aa210e888590cb3c519a9f8a967a49668461d3ca) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/re.bzl/0.4.1/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/re.bzl/0.4.1/source.json) |
| `toml.bzl` | 0.5.0 | [336bff08f5eb](https://github.com/jvolkman/toml.bzl/tree/336bff08f5ebff07f9e3836f47e7ba25a3b392c9) | [MODULE.bazel](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/toml.bzl/0.5.0/MODULE.bazel), [source.json](https://github.com/bazelbuild/bazel-central-registry/blob/9bc19aec3357f320fc262ab71a8d054af6b6a74d/modules/toml.bzl/0.5.0/source.json) |

`rules_rust_prost` uses the `extensions/prost` subdirectory of the same
rules_rust release archive. `rules_rs` additionally provisions a fork at
`2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733`; it is not the BCR rules_rust module.
Go protobuf claims inspect rules_go 0.65.0 at
`fb591bc876354b939ef767887e772c15f679a283`.

## Claim records

For every record: `status=source-verified`, `platforms=[]`, `fixture=null`,
`commands=[]`, `expected=null`, `observed=null`; only source inspection was
performed. Recommendations in the pages are editorial choices, not measured
performance claims. Each page supplies its exact ruleset versions.

### Choose a Rust integration

Page: [rulesets/rust/choosing-integration.md](../rulesets/rust/choosing-integration.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.integration.facade` | rules_rs provisions its own pinned rules_rust repository and re-exports core rules. | [rs-fork](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust.bzl); [rs-wrapper](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rust_library.bzl) |
| `rust.integration.apis` | The two integrations expose different toolchain and Cargo extension APIs. | [rs-toolchains](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/module_extension.bzl); [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl); [rust-tools](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl); [rust-cargo](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl) |
| `rust.integration.dependencies` | Module declarations and extension-generated repositories are distinct dependency inputs. | [rs-module](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/MODULE.bazel); [rust-module](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/MODULE.bazel); [rs-fork](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust.bzl) |

### Configure Rust toolchains

Page: [rulesets/rust/setup.md](../rulesets/rust/setup.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.setup.rs-tags` | rules_rs toolchain tags use a scalar version, edition, and generated repository name. | [rs-toolchains](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/module_extension.bzl) |
| `rust.setup.rs-selection` | For each repository name, root rules_rs toolchain declarations override dependencies; nonroot declarations merge with conflict checks. | [rs-toolchain-selection](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/toolchain_config.bzl) |
| `rust.setup.direct` | Direct rules_rust uses root toolchain tags or its own defaults and registers the rust_toolchains hub. | [rust-tools](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl); [rust-module](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/MODULE.bazel) |
| `rust.setup.host-cargo` | rules_rs host_cargo configures existing executables for repository-time host Cargo. | [rs-toolchains](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/toolchains/module_extension.bzl) |

### Model Rust libraries, binaries, and tests

Page: [rulesets/rust/targets.md](../rulesets/rust/targets.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.targets.loads` | Public Rust rules are exported by the direct defs file and rules_rs wrappers. | [rust-defs](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/defs.bzl); [rs-wrapper](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rust_library.bzl) |
| `rust.targets.inputs` | Rust rules distinguish srcs/crate_root, compile_data, data, and compiler edition/features. | [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl); [rs-fork-rules](https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/rust/private/rust.bzl) |
| `rust.targets.deps` | Direct rules_rust separates Rust deps, execution-configured proc_macro_deps, and native link_deps. | [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl) |
| `rust.targets.tests` | rust_test can compile the inline tests of a supplied crate target. | [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl) |

### Resolve Cargo dependencies

Page: [rulesets/rust/dependencies.md](../rulesets/rust/dependencies.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.cargo.rs-inputs` | rules_rs from_cargo requires Cargo.toml, Cargo.lock, and execution/target platform triples. | [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl) |
| `rust.cargo.rs-helpers` | rules_rs generates package-sensitive aliases and dependency helpers in the hub defs.bzl. | [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl) |
| `rust.cargo.direct-inputs` | Crate Universe has separate Cargo and rendering lockfiles and manifest/spec generation modes. | [rust-cargo](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl) |
| `rust.cargo.annotations` | Both integrations expose annotations but with distinct attributes and generated repository layouts. | [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl); [rust-cargo](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl) |

### Declare Cargo build-script inputs

Page: [rulesets/rust/build-scripts.md](../rulesets/rust/build-scripts.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.buildscript.stages` | cargo_build_script separately compiles and runs a build script with distinct inputs/environment. | [rust-buildscript](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/private/cargo_build_script_wrapper.bzl); [rs-fork-buildscript](https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/cargo/private/cargo_build_script_wrapper.bzl) |
| `rust.buildscript.outputs` | The build-script rule produces build information consumed by dependent Rust compilation. | [rust-buildaction](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/private/cargo_build_script.bzl); [rust-buildscript](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/cargo/private/cargo_build_script_wrapper.bzl) |
| `rust.buildscript.annotations` | Generated crates can receive build-script inputs via integration-specific annotation fields. | [rust-cargo](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/crate_universe/extensions.bzl); [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl) |
| `rust.buildscript.rs-paths` | The rules_rs fork exposes an explicit opt-in for build scripts emitting nonhermetic host paths. | [rs-fork-buildscript](https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/cargo/private/cargo_build_script_wrapper.bzl); [rs-crates](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/extensions.bzl) |

### Link Rust and native libraries

Page: [rulesets/rust/ffi.md](../rulesets/rust/ffi.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `rust.ffi.link-deps` | Direct and facade Rust rule implementations expose link_deps for native linkage; direct rust_proc_macro lacks this attribute and is excluded from the CcInfo-in-deps warning. | [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl); [rs-fork-rules](https://github.com/hermeticbuild/rules_rust/blob/2ab43f0bbaa406ffb1a0dd64ae2ecb8f7734f733/rust/private/rust.bzl) |
| `rust.ffi.outputs` | Direct rules export staticlib and cdylib rules returning CcInfo. | [rust-defs](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/defs.bzl); [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl) |
| `rust.ffi.exec-target` | Procedural macros and selected compiler tools use execution configuration while native libraries belong to target linkage. | [rust-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/private/rust.bzl); [rust-tools](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/rust/extensions.bzl) |
| `rust.ffi.bindgen-facade` | rules_rs provides a distinct extension provisioning its bindgen integration. | [rs-bindgen](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust_bindgen.bzl) |

### Set up protobuf rules and compiler selection

Page: [rulesets/protobuf/setup.md](../rulesets/protobuf/setup.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `protobuf.setup.loads` | protobuf exports proto_library and ProtoInfo from its bazel public entry points. | [proto-library](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/proto_library.bzl); [proto-info-public](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/common/proto_info.bzl) |
| `protobuf.setup.compiler` | protobuf36.2 enables preference for prebuilt protoc and registers prebuilt and source toolchains. | [proto-module](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/MODULE.bazel); [proto-flags](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/flags/BUILD); [proto-toolchains](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/toolchains/BUILD.bazel) |
| `protobuf.setup.roles` | proto_toolchain configures its compiler as an executable in execution configuration. | [proto-compiler-rule](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_toolchain_rule.bzl); [proto-compiler-macro](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/toolchains/proto_toolchain.bzl) |
| `protobuf.setup.versions` | protobuf module dependencies and language rules have separately selected release inputs. | [proto-module](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/MODULE.bazel) |

### Model protobuf sources and generated libraries

Page: [rulesets/protobuf/code-generation.md](../rulesets/protobuf/code-generation.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `protobuf.sources.graph` | proto_library has ProtoInfo-constrained deps, option_deps, exports, and import path transformation attributes. | [proto-rule](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_library_rule.bzl) |
| `protobuf.sources.providers` | ProtoInfo carries direct/transitive sources and descriptor sets; option deps are excluded from transitive descriptor sets. | [proto-info](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/proto_info.bzl) |
| `protobuf.codegen.languages` | C++, Python, and Go integrations expose separate language library rules over proto inputs. | [proto-cc-impl](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/cc_proto_library.bzl); [proto-python-impl](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/private/oss/py_proto_library.bzl); [go-proto](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/def.bzl) |
| `protobuf.codegen.descriptors` | proto_descriptor_set combines transitive descriptor sets from ProtoInfo dependencies. | [proto-descriptors](https://github.com/protocolbuffers/protobuf/blob/2c74169b34066ceb8ddb6b882fcb3fb32d737a55/bazel/proto_descriptor_set.bzl) |

### Select gRPC generation by language

Page: [rulesets/protobuf/grpc.md](../rulesets/protobuf/grpc.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `grpc.go.wrapper` | go_grpc_library defaults to go_proto plus go_grpc_v2 compilers. | [go-proto](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/def.bzl); [go-plugins](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/BUILD.bazel) |
| `grpc.go.runtime` | Go proto compilers carry generation and implicit runtime dependency information. | [go-compiler](https://github.com/bazel-contrib/rules_go/blob/fb591bc876354b939ef767887e772c15f679a283/proto/compiler.bzl) |
| `grpc.rust.tonic` | Prost toolchains expose execution-configured Tonic plugin and runtime fields with completeness validation. | [prost-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/prost.bzl); [prost-runtime](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/BUILD.bazel) |

### Integrate Rust Prost and Tonic

Page: [rulesets/protobuf/prost.md](../rulesets/protobuf/prost.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `prost.direct.module` | Direct rules_rust_prost is a separate module from the same rules_rust release archive and registers a default toolchain. | [prost-module](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/MODULE.bazel); [prost-build](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/BUILD.bazel) |
| `prost.rule.proto` | rust_prost_library takes a mandatory ProtoInfo-valued proto and returns crate-group information. | [prost-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/prost.bzl) |
| `prost.toolchain.roles` | Prost toolchains distinguish executable generator plugins from Rust runtime providers and resolve protoc separately; omitting Tonic requires all three Tonic fields empty, including its otherwise nonempty default plugin flag. | [prost-rules](https://github.com/bazelbuild/rules_rust/blob/21234a3c7d71e70f858e7e6d783138768b300e64/extensions/prost/private/prost.bzl) |
| `prost.facade` | rules_rs generates a distinct Prost facade repository backed by its fork and own runtime targets. | [rs-prost](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/rules_rust_prost.bzl); [rs-prost-runtime](https://github.com/hermeticbuild/rules_rs/blob/99e2e11265235c148a2acf4201f534829248784f/rs/private/prost/BUILD.bazel) |

### Choose a Starlark utility library

Page: [rulesets/utilities/library-selection.md](../rulesets/utilities/library-selection.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `utilities.skylib` | Skylib exports path/select helpers and common build-setting rules with BuildSettingInfo. | [skylib-paths](https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/paths.bzl); [skylib-selects](https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/lib/selects.bzl); [skylib-settings](https://github.com/bazelbuild/bazel-skylib/blob/3de43ed45e1c7923d53c4db56ca3de3e46601580/rules/common_settings.bzl) |
| `utilities.bazel-lib` | bazel_lib exports file/directory action helpers and registers supporting toolchains. | [lib-copy](https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/copy_to_directory.bzl); [lib-params](https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/params_file.bzl); [lib-module](https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/MODULE.bazel) |
| `utilities.directory-path` | DirectoryPathInfo carries a tree artifact and relative path; directory_path validates the artifact kind. | [lib-path](https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/directory_path.bzl); [lib-path-impl](https://github.com/bazel-contrib/bazel-lib/blob/904332fd1c978e1d84161c120b26533df279c3dc/lib/private/directory_path.bzl) |
| `utilities.features` | bazel_features exports feature predicates and globals through generated supporting repositories. | [features](https://github.com/bazel-contrib/bazel_features/blob/6f5b91edb290af78d50ea12c8c2db44d46f1fcde/features.bzl); [features-module](https://github.com/bazel-contrib/bazel_features/blob/6f5b91edb290af78d50ea12c8c2db44d46f1fcde/MODULE.bazel) |

### Pin prebuilt executables with rules_multitool

Page: [rulesets/utilities/multitool.md](../rulesets/utilities/multitool.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `multitool.hubs` | The multitool extension reads hub_name/lockfile tags and generates named tool hubs; the module registers the default hub. | [multitool-extension](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/extension.bzl); [multitool-module](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/MODULE.bazel) |
| `multitool.distributions` | Lockfiles describe per-OS/CPU executable distributions and fetch code reads each SHA256. | [multitool-schema](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/lockfile.schema.json); [multitool-fetch](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/multitool.bzl); [multitool-lock](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/lockfile.bzl) |
| `multitool.targets` | Generated executable targets select a toolchain and expose a symlink to its executable. | [multitool-tool](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_tool_template/tool.bzl.template); [multitool-target](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_tool_template/BUILD.bazel.template); [multitool-toolchains](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/hub_repo_template/toolchain_info.bzl.template) |
| `multitool.merge` | Multiple lockfiles are merged at tool-name granularity with later values replacing earlier ones. | [multitool-lock](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/private/lockfile.bzl); [multitool-extension](https://github.com/bazel-contrib/rules_multitool/blob/0be566f364df52308bfb7629e888e5084c3f5a85/multitool/extension.bzl) |

### Use regex in Starlark deliberately

Page: [rulesets/utilities/regex.md](../rulesets/utilities/regex.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `regex.api` | re.bzl exports compile/search/match/fullmatch/findall/finditer/split/sub and flags. | [regex-public](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re.bzl); [regex-core](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/private/re.bzl) |
| `regex.syntax` | The implementation supports a bounded regex syntax rather than Python re equivalence; backreferences and lookarounds are unsupported. | [regex-readme](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/README.md); [regex-compiler](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/private/compiler.bzl) |
| `regex.anchors` | Dollar-anchor handling is end-of-text unless multiline mode is selected, with upstream tests covering the behavior. | [regex-anchors](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/tests/test_anchors.bzl) |
| `regex.reuse` | compile returns a reusable object with search/match/fullmatch methods. | [regex-core](https://github.com/jvolkman/re.bzl/blob/aa210e888590cb3c519a9f8a967a49668461d3ca/re/private/re.bzl) |

### Parse and emit TOML in Starlark

Page: [rulesets/utilities/toml.md](../rulesets/utilities/toml.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `toml.api` | toml.bzl exports decode/encode, temporal constructors, and datetime_to_string. | [toml-public](https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml.bzl); [toml-datetime](https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/datetime.bzl) |
| `toml.errors` | decode defaults to failing on parse errors; a non-None default enables fallback return, and max_depth defaults to128. | [toml-decode](https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/decode.bzl) |
| `toml.encode` | encode requires a dictionary root and has an explicit max_tables bound. | [toml-encode](https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/toml/private/encode.bzl) |
| `toml.scope` | The module declares its own test-suite dependency; this page does not execute that suite or assert measured conformance. | [toml-module](https://github.com/jvolkman/toml.bzl/blob/336bff08f5ebff07f9e3836f47e7ba25a3b392c9/MODULE.bazel) |

### Apply scoped configuration with with_cfg.bzl

Page: [rulesets/utilities/configuration-wrappers.md](../rulesets/utilities/configuration-wrappers.md).

| Claim ID | Bounded statement | Evidence |
| --- | --- | --- |
| `withcfg.api` | with_cfg.bzl exports with_cfg and original_settings through its root bzl file. | [cfg-public](https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg.bzl) |
| `withcfg.builder` | with_cfg builds a wrapper using set/extend and returns a macro plus a rule that must be bound globally. | [cfg-builder](https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/with_cfg.bzl) |
| `withcfg.reset` | resettable and reset_on_attrs restore selected settings for designated dependency paths. | [cfg-builder](https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/with_cfg.bzl) |
| `withcfg.providers` | Wrappers have a defined provider forwarding set and accept extra_providers. | [cfg-builder](https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/with_cfg.bzl); [cfg-providers](https://github.com/fmeum/with_cfg.bzl/blob/9b8b10962419346889e528cbe57a539754489d57/with_cfg/private/rule_defaults.bzl) |

## Known gaps and contradictory prose

- No compiler, SDK, cross-platform, remote-execution, runtime, registry-auth, or complete dependency-graph compatibility run is recorded.
- The rules_rust_prost narrative says no default toolchain exists; MODULE.bazel and BUILD.bazel register one. The guidance follows those declarations.
- rules_rust_prost prose shows explicit proto_compiler setup while implementation deprecates that attribute. The guidance follows the current resolution path.
- The rules_rs README includes stale module-version examples. The reviewed release identity is the registry version plus verified archive, not those examples.
- rules_multitool JSON schema omits sha256 from required fields, but fetch implementation reads it directly. Guidance requires a digest.
- C++ and Python gRPC release selection/integration, and independent bindgen release selection, are not covered as tested recipes.
- Published parsing/performance descriptions were not promoted to measured conformance, throughput, or complexity results.
- Per-claim executable tests and BuildBuddy orchestration are tracked in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).
