---
title: "Select attributes with typed build settings"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["core/phases-and-graphs.md", "configuration/platforms-and-constraints.md"]
claim_ids: ["configuration.select-resolution", "configuration.condition-matching", "configuration.typed-settings", "configuration.select-context"]
last_verified: "2026-11-05"
---

# Select attributes with typed build settings

Use this when a target needs different attributes under different configurations.
Our recommendation is to use platform constraints for platform identity and typed
build settings for project-specific choices.

## Resolve values during analysis

`select()` describes a configurable attribute value. During analysis Bazel matches
its condition labels and resolves the attribute before the rule implementation
reads it through `ctx.attr`. It is not an imperative branch that executes a BUILD
file differently. Macros run before that resolution and cannot inspect which
branch will win. [Attribute resolution][select], [configuration contexts][attribute-guide]

Matching is not first-branch-wins. If several conditions match, Bazel eliminates
less-specific matches; remaining different values are an ambiguity error. Several
remaining matches are allowed when they produce the same value.
`//conditions:default` is used only when no condition matches; with no match and no
default, ordinary analysis reports an error. `no_match_error` supplies an
explanation for that case. [Resolution implementation][select]

A `config_setting` can combine native option `values`, typed build-setting
`flag_values`, and `constraint_values`. The conditions are combined with AND.
Constraint matching checks the target platform, allowing it to carry additional
unmentioned constraints. Strings in `flag_values` are parsed according to the
setting's type. Prefer a narrow, named condition over repeated complicated
selectors. [Matching implementation][config-setting]

Specificity includes native settings, typed flag settings, and constraints;
it is not simply the number of entries in a dictionary. A condition that refines
another must contain its requirements and add a stricter requirement.
Constraint refinement is also supported through the platform constraint APIs.
[Condition refinement][config-matching], [constraint refinement][constraint-rule]

## Define a typed configuration interface

A Starlark build-setting rule declares a `build_setting` descriptor, receives the
automatically added `build_setting_default` attribute, and reads the configured
raw value as `ctx.build_setting_value`. It can validate that value and return a
provider for its consumers. A setting declared with `flag = True` is writable from
the command line; a non-flag setting can still be changed by transitions.
[Rule API][rule-api], [setting context][context], [setting API][config-api]

| Descriptor | Value | Use when |
| --- | --- | --- |
| `config.bool` | Boolean | An independent on/off choice |
| `config.int` | Integer | A numeric configuration value |
| `config.string` | String | A named mode or scalar choice |
| `config.string_list` | List of strings | Order or repetition matters |
| `config.string_set` | Set of strings | Order and duplicates have no meaning |

These descriptors exist in 9.3.1. List and set settings accept comma-separated
values by default; their `repeatable = True` mode treats each occurrence as one
string. A list preserves order and duplicates; a set does not give those semantic
significance. Prefer the type that expresses the setting's meaning; do not encode
an unordered choice as an order-sensitive list by habit. [Typed descriptors][config-api]

`label_flag` and `label_setting` provide label-valued settings that forward the
selected target's providers. The former is command-line configurable; both can be
changed by transitions. Use them when configuration chooses a dependency interface
rather than a scalar mode. [Label-valued settings][config-guide]

A build-setting rule's provider is its consumer interface. It is distinct from the
raw setting value used for configuration matching and transition inputs. Keep
validation and provider conversion explicit. [Build-setting model][config-guide]

## Keep configuration logic in the right layer

Use a macro to wire declarations, a `select()` to vary an attribute, and a
[transition](transitions.md) when a dependency needs a different configuration.
The selector on a transitioned dependency attribute is resolved in the owner's
configuration; the dependency is then analyzed in its transitioned configuration.
Its own selectors see that configuration. [Dependency transitions][attribute-guide]

Our recommendation is to provide a deliberate default only when the default is
actually supported. A broad fallback can conceal a missing platform or feature
case. Avoid enumerating every machine when the choice depends on a single
constraint. Use the configured graph when investigating what was selected; the
unconfigured target graph cannot establish which branch a build uses.
See [phases and graphs](../core/phases-and-graphs.md).

## Evidence scope

Source review at Bazel 9.3.1; no integration fixture was executed for this page.
See the [claim ledger](../verification/configuration-toolchains.md). Flags or
platform behavior described here do not establish a tested project configuration.

[select]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/ConfiguredAttributeMapper.java
[attribute-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/configure/attributes.md
[config-setting]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/config/ConfigSetting.java
[config-matching]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/config/ConfigMatchingProvider.java
[constraint-rule]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/rules/platform/ConstraintSettingRule.java
[rule-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkRuleFunctionsApi.java
[context]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/analysis/starlark/StarlarkRuleContext.java
[config-api]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/config/StarlarkConfigApi.java
[config-guide]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/config.md
