# Configuration and toolchain evidence

All records are **source-verified**, inspected on 2026-11-05 against Bazel 9.3.1
commit `fee2bf2d1c14bc2096068a4d46f1842472092044`. No platform-specific integration
run or executable fixture is claimed here. Sources below are implementation, API
definitions, or release-pinned documentation; upstream tests were read, not run.
No ruleset dependency graph was resolved for these conceptual pages.

Runnable claim assertions and BuildBuddy automation are tracked separately in
[issue #1](https://github.com/JSGette/bazel-for-agents/issues/1). The current pages
contain API descriptions and design guidance, not tested setup recipes.

## configuration.platform-roles

Host, execution, and target roles differ; one target platform is used per configuration, falling back to host when unspecified.

- [platform-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java): `computeTargetPlatform/getNormalized`.
- [platform-config](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformConfiguration.java): `constructor/reportInvalidOptions`.
- [exec-transition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java): `execution platform assignment`.

## configuration.constraints

Constraint settings define dimensions; values choose a dimension value. Defaults and conditional refinement affect matching; conflicting platform values are rejected.

- [constraint-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ConstraintSettingRule.java): `default_constraint_value/refines_constraint_value`.
- [platform-impl](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/Platform.java): `create`.
- [constraint-collection](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/platform/ConstraintCollection.java): `constraint validation and lookup`.

## configuration.platform-inheritance

Platforms accept at most one parent; child constraints override parent values, and execution properties merge with child overrides and empty-value removal.

- [platform-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/PlatformRule.java): `parents/exec_properties`.
- [platform-impl](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/Platform.java): `create`.

## configuration.platform-flags

Target-platform flags override earlier configuration values, including repeatable flags; required_settings separately gates execution-platform eligibility and is not inherited.

- [platform-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/PlatformRule.java): `flags/required_settings and platform_flags documentation`.
- [registered-platforms](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredExecutionPlatformsFunction.java): `ConfigMatchingUtil.validate`.

## configuration.target-compatibility

Ordinary target compatibility constrains supported target platforms; broad-pattern incompatible targets are skipped and explicit requests normally fail.

- [platform-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/platforms.md): `Skipping incompatible targets`.

## configuration.select-resolution

select resolves attributes during analysis, removes less-specific matches, accepts equal remaining values, otherwise rejects ambiguity; default is used only with no match.

- [select](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/ConfiguredAttributeMapper.java): `resolveSelector/getResolvedAttribute`.

## configuration.condition-matching

config_setting combines native options, typed flags and constraints; matching and specialization use their respective requirements.

- [config-setting](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/config/ConfigSetting.java): `create/diffConstraintValues/UserDefinedFlagValuesMatch`.
- [config-matching](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ConfigMatchingProvider.java): `refines`.
- [constraint-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ConstraintSettingRule.java): `refines_constraint_value`.

## configuration.typed-settings

The config descriptors include bool,int,string,string_list,string_set; label_flag/label_setting forward selected dependency providers; flag=True exposes command-line setting, with distinct list/set repeatable semantics. Build-setting rules receive defaults and raw configured values.

- [config-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java): `descriptor methods`.
- [rule-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java): `build_setting parameter`.
- [context](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleContext.java): `getBuildSettingValue`.
- [config-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md): `Build settings`.

## configuration.select-context

Macros cannot resolve a selector; dependency-attribute selection occurs before the dependency transition, while dependency selectors see the resulting configuration.

- [attribute-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/configure/attributes.md): `select and dependencies / Why does select always return true?`.
- [config-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md): `transition attr timing`.

## configuration.transition-placement

Incoming rule transitions produce one configuration; outgoing dependency transitions may split, with split results exposed through ctx.split_attr.

- [rule-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java): `cfg`.
- [config-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md): `Incoming/Outgoing edge transitions and Accessing attributes with transitions`.

## configuration.transition-contract

Transition input/output declarations bound access; ordinary nonempty returned dictionaries must exactly match outputs, while a top-level empty dict is no-change. Native options are validated.

- [function-transition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/StarlarkDefinedConfigTransition.java): `evaluate/validateFunctionOutputsMatchesDeclaredOutputs`.
- [function-util](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/FunctionTransitionUtil.java): `applyAndValidate/validateNativeSettings`.

## configuration.transition-allowlist

The rule-definition implementation adds a missing function-transition allowlist attr and checker, validates explicit attrs, and rejects unused ones.

- [rule-functions](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleClassFunctions.java): `checkAndAddAllowlistIfNecessary and FUNCTION_TRANSITION_ALLOWLIST_CHECKER`.
- [allowlist](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/FunctionSplitTransitionAllowlist.java): `ATTRIBUTE_NAME/LABEL`.

## configuration.execution-transition

Execution transitions use the selected execution platform; executable label attrs require explicit cfg; config.exec can select a named group.

- [exec-transition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java): `create`.
- [attr-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java): `cfg on label`.
- [config-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java): `exec`.

## configuration.transition-cost

Additional and split configurations can increase configured-target graph size. The performance advice is qualitative, not a repository benchmark.

- [config-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md): `Memory and performance considerations`.

## toolchains.requirement

Rules request toolchain types; config_common.toolchain_type supports optional requirements and defaults mandatory=True.

- [rule-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java): `toolchains`.
- [config-common](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/ConfigStarlarkCommonApi.java): `toolchain_type`.

## toolchains.provider

Resolved implementations must provide ToolchainInfo, with interface-defined fields. Optional unresolved types yield None and undeclared lookups fail.

- [resolved](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/ResolvedToolchainContext.java): `load/forToolchainType`.
- [toolchain-context](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainContextApi.java): `indexing contract`.
- [toolchain-info](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java): `provider constructor`.

- [lookup validation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkToolchainContext.java): `getIndex`.

## toolchains.action-association

Action toolchain identifies the type supplying tools; explicit named groups route actions, subject to automatic-group validation.

- [action-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java): `run/run_shell toolchain parameter`.
- [action-impl](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java): `determineExecGroup`.

## toolchains.tool-dependencies

Action tool paths do not themselves describe input closures; tools and FilesToRunProvider carry declared files/runfiles; executable attrs declare cfg.

- [action-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java): `executable/tools/inputs`.
- [attr-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java): `executable/cfg`.

## toolchains.definition-parts

A type identifies a role, implementation provides ToolchainInfo, and a registered toolchain wrapper connects them with constraints.

- [toolchain-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ToolchainRule.java): `toolchain_type/toolchain`.
- [resolved](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/ResolvedToolchainContext.java): `ToolchainInfo provider validation`.
- [toolchain-info](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java): `provider interface`.

## toolchains.compatibility

Wrappers have distinct execution and target constraints, target_settings, and the mutually exclusive use_target_platform_constraints mode.

- [toolchain-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ToolchainRule.java): `attribute contracts`.
- [single-resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java): `resolveConstraints`.

## toolchains.registration

MODULE registration takes absolute target patterns; wrapper and execution-platform registrations are separate; multi-target expansion is lexical by target name.

- [module-globals](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java): `registerToolchains/registerExecutionPlatforms`.

## toolchains.registration-scope

dev_dependency registrations are ignored outside root or when dev dependencies are ignored; labels use declaring-module repository mappings.

- [module-globals](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java): `registration dev_dependency handling`.
- [registered](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredToolchainsFunction.java): `getBzlmodToolchains`.

## toolchains.registration-priority

Extra toolchains precede module registrations and are reversed; module graph traversal is breadth-first root first with per-module order retained.

- [registered](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredToolchainsFunction.java): `compute/getBzlmodToolchains`.
- [depgraph](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/BazelDepGraphValue.java): `getDepGraph order contract`.
- [platform-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java): `extraToolchains normalization`.

## toolchains.execution-candidates

Extra execution platforms precede module entries without reversal; repeated flags replace the list; host is appended and earliest duplicate registration wins.

- [registered-platforms](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredExecutionPlatformsFunction.java): `compute/getBzlmodExecutionPlatforms`.
- [platform-keys](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/PlatformKeys.java): `loadExecutionPlatforms`.
- [platform-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java): `extra_execution_platforms`.

## toolchains.matching

For each type/execution-platform pair, first compatible registration wins after target/execution constraints, settings, and platform eligibility filtering.

- [single-resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java): `resolveConstraints`.
- [registered](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/RegisteredToolchainsFunction.java): `targetSettings filtering`.
- [platform-keys](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/PlatformKeys.java): `filterExecutionPlatforms/isPlatformSuitable`.

## toolchains.platform-selection

Normal selection requires mandatory types then maximizes resolved requested types including optional types, retaining priority on ties; forced selection has a separate early branch.

- [resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunction.java): `findExecutionPlatformForToolchains/countToolchainsOnPlatform`.
- [resolution-tests](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/test/java/com/google/devtools/build/lib/skyframe/toolchains/ToolchainResolutionFunctionTest.java): `optional-resolution test cases`.

## toolchains.resolution-debug

toolchain_resolution_debug is a regex filter on types and targets, disabled by its default exclusion expression.

- [platform-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java): `toolchain_resolution_debug`.

## toolchains.named-groups

Named groups define independent requirements/resolution and group-specific toolchain access; config.exec selects a group for an executable dependency.

- [rule-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java): `exec_group/exec_groups`.
- [exec-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/exec-groups.md): `definition/access`.
- [config-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java): `exec`.

## toolchains.automatic-groups

Global incompatible_auto_exec_groups defaults false in 9.3.1; per-rule dynamic overrides and enabled/disabled modes exist. Active automatic groups resolve per type.

- [core-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/CoreOptions.java): `incompatible_auto_exec_groups`.
- [rule-class](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/RuleClass.java): `AutoExecGroupsMode.isEnabled`.
- [auto-exec-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/auto-exec-groups.md): `automatic group model`.

## toolchains.group-action-routing

Explicit exec_group wins routing; under automatic groups a supplied toolchain must belong to that group; otherwise its automatic group or default group is used.

- [action-impl](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkActionFactory.java): `determineExecGroup and toolchain-annotation checks`.
- [action-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java): `toolchain/exec_group`.

## toolchains.group-properties

Named-group constraints and group-prefixed execution properties specialize target-level execution policy.

- [exec-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/exec-groups.md): `Execution group inheritance / execution properties / exec_group_compatible_with`.

## toolchains.cross-platform-model

Cross compilation distinguishes the machine running build tools from the platform of produced artifacts; wrapper constraints describe both.

- [platform-guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/platforms.md): `platform roles`.
- [toolchain-rule](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ToolchainRule.java): `exec_compatible_with/target_compatible_with`.

## toolchains.cross-tool-dependencies

Attribute transitions determine dependency configurations; build-time tools need execution-compatible artifacts and action association.

- [attr-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkAttrModuleApi.java): `cfg`.
- [exec-transition](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ExecutionTransitionFactory.java): `execution platform assignment`.
- [action-api](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java): `toolchain parameter`.

## toolchains.cross-selection

Generic resolution matches declared constraints and settings; arbitrary ToolchainInfo fields are not a universal ABI schema.

- [single-resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/skyframe/toolchains/SingleToolchainResolutionFunction.java): `resolveConstraints`.
- [toolchain-info](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/platform/ToolchainInfoApi.java): `arbitrary provider fields`.

## toolchains.cross-validation

Execution-platform registration declares candidates, not runner provisioning; --platforms uses one entry. Separate compile/run validation is repository guidance.

- [module-globals](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/ModuleFileGlobals.java): `registerExecutionPlatforms`.
- [platform-options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/PlatformOptions.java): `getNormalized/computeTargetPlatform`.

## Conflicts resolved against implementation

- The toolchain resolver method comment says “first” suitable platform, while its
  implementation ranks candidates by resolved requested types. The page follows
  the implementation and its optional-toolchain tests.
- The transition API describes output keys as a subset of declared outputs. The
  implementation requires exact keys for normal nonempty return dictionaries;
  its top-level empty dictionary no-change path is documented separately.
- Automatic execution groups are available, but the global flag defaults false.
  Rule-local modes and overrides mean this is not a universal per-rule default.
- Function-transition allowlist enforcement exists, but missing allowlist
  attributes are inserted automatically; boilerplate is not required solely
  to declare the ordinary built-in allowlist attribute.

## configuration.invocation-boundary

Startup options precede the command and command options follow it; rc startup sections are processed by the client.

- [client](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/option_processor.cc): `SplitCommandLine/ParseStartupOptions`.
- [guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/run/bazelrc.md): `startup option placement`.

## configuration.rc-discovery

Rc discovery orders system, project, home, BAZELRC, then explicit paths; ignore_all_rc_files skips loading, while /dev/null only terminates later explicit paths.

- [client](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/option_processor.cc): `GetRcFiles/ParseOptions and GetAndValidateExistingRcFiles`.

## configuration.rc-imports

Imports expand in place; try-import ignores unreadable files but not malformed files or cycles; conditional version imports and project-relative expansion are supported.

- [parser](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/rc_file.cc): `ParseFile import processing`.

## configuration.rc-precedence

Rc parsing respects command specificity and option-specific accumulation; command-line priority does not preclude later invocation policy or platform configuration.

- [handler](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/BlazeOptionHandler.java): `parseRcOptions/getCommandNamesToParse/parseOptions`.
- [guide](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/run/bazelrc.md): `Option precedence`.

## configuration.named-configs

Named configs expand applicable sections in place across loaded rc definitions; cycles fail. Host-OS startup sections are separate; command host-OS config flag defaults false.

- [expander](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/ConfigExpander.java): `expandConfigOptions/getExpansion`.
- [client](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/option_processor.cc): `ParseStartupOptions`.
- [options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/CommonCommandOptions.java): `enable_platform_specific_config/config`.

## configuration.rc-observability

announce_rc defaults false and exposes rc/expansion notes; suppressing rc files also suppresses options supplied there. Reproduction recommendations are editorial guidance.

- [options](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/CommonCommandOptions.java): `announce_rc`.
- [handler](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/runtime/BlazeOptionHandler.java): `rcfileNotes reporting`.
- [client](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/cpp/option_processor.cc): `ignore_all_rc_files handling`.
