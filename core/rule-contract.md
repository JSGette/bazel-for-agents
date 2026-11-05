---
title: "Define a rule's contract"
status: source-verified
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: ["linux-x86_64 (linked fixture only)"]
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/phases-and-graphs.md"]
claim_ids: ["rules.definition", "rules.attributes", "rules.implementation", "rules.action-cardinality", "rules.output-demand"]
last_verified: "2026-11-05"
---

# Define a rule's contract

Use this when creating a custom rule or deciding where build logic belongs.
Start by writing down the inputs the target accepts, the information it exposes
to consumers, and the artifacts it produces. This is our authoring recommendation.

## Separate the definition, target, and implementation

| Piece | Role |
| --- | --- |
| `greeting = rule(...)` in a `.bzl` file | Defines a reusable rule kind with attribute schemas and an implementation. |
| `greeting(name = "greeting", ...)` in `BUILD.bazel` | Instantiates a named target; it does not immediately run the implementation's build work. |
| `_greeting_impl(ctx)` | Runs during analysis for the target being analyzed, registers actions, and returns provider instances. |

The rule symbol must be assigned to a global variable in a `.bzl` file. Its
implementation takes one rule-context argument, conventionally named `ctx`.
These are separate calls with separate purposes. [Definition evidence][definition]

## Make input requirements explicit

Declare rule-specific attributes in `rule(attrs = {...})`, using schemas such as
`attr.string`, `attr.label`, and `attr.label_list`. Bazel already supplies common
attributes such as `name` and `visibility`; do not redeclare them.
[Attribute evidence][attributes]

Use dependency attributes for target inputs. During analysis, ordinary label
attributes expose dependency `Target` objects through `ctx.attr`; the implementation
can read those targets' providers. Use `ctx.file` for an attribute declared with
`allow_single_file`, or `ctx.files` to obtain the default files of dependencies.
[Attribute evidence][attributes]

In the fixture, `person` is string data, `template` is a single-file dependency,
and the consumer's `source` requires `GreetingInfo`. Our recommendation is to
express that provider requirement in the attribute schema so an invalid dependency
fails at the interface. See [providers](providers.md) for the distinction between
an attribute's `providers` requirement and a rule's `provides` declaration.

## Describe execution work during analysis

Rule implementations can inspect attributes and provider values, declare output
`File` objects, and register producing actions. They cannot directly read or write
artifact contents or run external commands. A `File` is a reference to an artifact,
not the contents of that file. [Implementation evidence][implementation]

Use the relevant `ctx.actions` method to describe how each generated artifact is
produced. Registering `ctx.actions.write` also describes an action; it is not
analysis-time file I/O. See [declaring actions](../actions/declaring-actions.md).
[Implementation evidence][implementation]

A rule is not constrained to one action. The fixture's producer registers separate
actions for its message and metadata. A rule may also aggregate existing artifacts
without a producing action of its own, as `filegroup` does.
[Action-count evidence][cardinality]

## Expose the intended result

Return provider instances describing the target's public result. For an ordinary
producing rule, our recommendation is to explicitly return
`DefaultInfo(files = depset([...]))` with the intended default artifacts, plus any
custom provider consumers need. See [providers](providers.md).

Registering an action does not guarantee that it runs. Ordinary output selection
starts from requested files and follows their dependencies; actions whose outputs
are not needed can be omitted. Expose optional artifacts through an output group
when users need to request them separately. Special output groups and validation
actions have additional behavior outside this introductory page.
[Output-demand evidence][demand]

## Follow the runnable example

Read [defs.bzl](../examples/foundations/defs.bzl) with its
[BUILD.bazel](../examples/foundations/BUILD.bazel). Trace `//:greeting` into
`//:report`: the consumer reads `GreetingInfo`, then registers an action using the
generated message as a template. It does not read the message during analysis.

The [verification record](../verification/foundations.md) gives exact commands and
observed results on Bazel 9.3.1/Linux x86_64. Building `//:report` produced
`Greetings, Bazel!`; requesting the metadata group produced `person=Bazel`.
An intentionally invalid consumer failed the provider check during analysis.

These results cover the small fixture, not arbitrary toolchains, language rules,
remote execution, or every rule option. The remaining statements are source-verified.

[definition]: ../verification/core-rules-providers.md#rulesdefinition
[attributes]: ../verification/core-rules-providers.md#rulesattributes
[implementation]: ../verification/core-rules-providers.md#rulesimplementation
[cardinality]: ../verification/core-rules-providers.md#rulesaction-cardinality
[demand]: ../verification/core-rules-providers.md#rulesoutput-demand
