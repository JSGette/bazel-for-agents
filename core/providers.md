---
title: "Pass information between rules with providers"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: ["linux-x86_64 (linked fixture only)"]
required_flags: []
prerequisites: ["core/rule-contract.md"]
claim_ids: ["providers.identity", "providers.schema", "providers.requirements", "providers.defaults", "providers.output-groups", "providers.transitive"]
last_verified: "2026-11-05"
---

# Pass information between rules with providers

Use this when a consumer needs a dependency's artifacts or structured build
metadata. Providers form the analysis-time interface between dependent targets.
The producer returns instances; the consumer retrieves an instance using the
provider symbol as a key, as in `source[GreetingInfo]`.
[Identity evidence][identity]

## Give rule-specific information a named interface

Define a custom provider in a `.bzl` global, document its fields, construct an
instance in the producer, and return it in the implementation's provider list.
Consumers use the same exported provider symbol to retrieve the instance.
[Identity evidence][identity]

In [the fixture](../examples/foundations/defs.bzl), `GreetingInfo` carries a
`message` artifact and a `person` string. The consumer uses the artifact directly
as an action input instead of reconstructing its output path. That is the pattern
we recommend for named outputs with a specific role.

`provider(fields = {...})` restricts allowed field names and supplies documentation.
It does not require every declared field to be populated, and the documentation
strings are not runtime type declarations. Our recommendation is to document and
consistently construct required fields; use the provider's `init` mechanism when
the interface needs construction-time validation. [Schema evidence][schema]

## State what a dependency must provide

Use the dependency attribute's `providers` argument to express a required
interface. The fixture's `source` attribute requires `GreetingInfo` and rejects
the `filegroup` passed to `//:bad_provider`. [Requirement evidence][requirements]

Two declarations serve different purposes:

| Declaration | Meaning |
| --- | --- |
| `attr.label(providers = [GreetingInfo])` | Dependencies supplied through this attribute must return `GreetingInfo`. |
| `rule(provides = [GreetingInfo])` | The rule advertises `GreetingInfo` and its implementation must return it. |

An attribute requirement does not require the producer to advertise the provider
with `provides`; returning it is sufficient for that check. We recommend advertising
the rule's public custom providers anyway. In an attribute requirement, a flat list
requires all listed providers; nested lists express alternatives, each of which
requires all its members. [Requirement evidence][requirements]

## Keep the three output interfaces distinct

| Interface | Use |
| --- | --- |
| Custom provider, such as `GreetingInfo` | A semantic contract between rules: named artifacts and metadata. |
| `DefaultInfo` | General target information, including default files, runfiles, and executable information. |
| `OutputGroupInfo` | Named groups of artifacts that can be selected for building. |

Every rule target has `DefaultInfo`, including when its implementation does not
explicitly return it. For new producing rules, explicitly set `files` to a `depset`
of the intended default artifacts. `runfiles` describes runtime files and is a
separate interface; placing a file in a custom provider does not automatically
make it a default output. [Default-output evidence][defaults]

The fixture exposes `greeting.txt` through both `GreetingInfo.message` and
`DefaultInfo.files`, and exposes `runtime.txt` separately as runfiles. Continue to
[outputs and runfiles](outputs-and-runfiles.md) for that distinction.

Use output groups for optional artifacts that users need to request together.
The fixture's `metadata` group holds `greeting.metadata.txt`; selecting that group
requests its producing action. Use custom providers for the consumer-facing
meaning of artifacts, and output groups for build selection.
[Output-group evidence][groups]

## Forward transitive information deliberately

A rule reads providers from its direct dependencies. If its consumers need
information from further down the dependency graph, the rule must propagate that
information through its own providers. For transitive artifact collections, our
recommendation follows Bazel's guidance: compose `depset` values rather than
repeatedly flattening the dependency closure. [Propagation evidence][transitive]

## Verify the interface

The [foundation verification record](../verification/foundations.md) includes the
successful consumer build, checks on its dependency's default files and runfiles,
separate output-group selection, and the intentional missing-provider failure.
These ran on Bazel 9.3.1/Linux x86_64. Provider `init`, nested alternative
requirements, and larger transitive graphs are source-verified here, not exercised
by this fixture.

[identity]: ../verification/core-rules-providers.md#providersidentity
[schema]: ../verification/core-rules-providers.md#providersschema
[requirements]: ../verification/core-rules-providers.md#providersrequirements
[defaults]: ../verification/core-rules-providers.md#providersdefaults
[groups]: ../verification/core-rules-providers.md#providersoutput-groups
[transitive]: ../verification/core-rules-providers.md#providerstransitive
