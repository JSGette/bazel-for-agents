---
title: "Review action hermeticity and reproducibility"
status: "source-verified"
bazel_verified: ["9.3.1"]
rulesets_verified: {}
platforms_verified: []
required_flags: []
prerequisites: ["actions/inputs-tools-environment.md", "actions/directories-and-symlinks.md"]
claim_ids: ["actions.hermetic.inputs", "actions.hermetic.sandbox", "actions.hermetic.nondeterminism", "actions.hermetic.environment"]
last_verified: "2026-11-05"
---

# Review action hermeticity and reproducibility

Use this page before sharing action-cache results or moving an action to another
execution environment. The review procedure below is a repository recommendation;
it is not a certification that a particular action is hermetic.

## Write down the action's complete input contract

For each action, identify the tool distribution, runtime support files, source
inputs, generated inputs, parameters, and environment that can affect its output.
Bazel's `run()` interface represents these through distinct input, tool, argument,
and environment fields. A toolchain or execution requirement selects how work is
run; it does not itself replace missing artifact dependencies. [Action API][actions]

An undeclared file can change without causing the action to rebuild, because
Bazel does not know that dependency exists. The resulting stale output can also
be reused through a shared cache. This is why “the command ran successfully” is
not a sufficient review of an action declaration. [Sandboxing rationale][sandbox]

Our recommendation: make a consumer's declared input set conservative first, then
optimize it only with evidence of the tool's real dependency behavior. Keep
repository downloads and dependency discovery outside ordinary compile/generate
actions; give those actions already-resolved input artifacts.

## Inspect the execution boundary, not just the strategy name

Sandboxing constrains execution according to the selected implementation. The
`local` strategy performs no sandboxing. A process-wrapper sandbox stages declared
inputs but does not provide all of the filesystem restrictions of an OS-specific
sandbox. The sandboxing guide explicitly notes that knowing an absolute path can
still permit reading host files. [Strategy and filesystem boundaries][sandbox]

Therefore a successful sandboxed build is useful evidence, not proof that every
host dependency has been removed. Our recommendation is to inspect actual actions
and test with a controlled tool installation and environment. Record the strategy
and host/platform used; do not label the result universal remote compatibility.

A failing sandbox can also reflect missing platform support rather than a rule
error. Diagnose the failure and the actual strategy before changing declarations.
Do not use an unsandboxed rerun as the final evidence that a dependency bug is
fixed. [Sandbox strategy and debugging guidance][sandbox]

## Separate stable inputs from stable output generation

Pinned tools and declared inputs do not alone establish byte-for-byte output
stability. The hermeticity guide lists nondeterministic tool behavior, build IDs,
timestamps, system binaries that vary by host, and source-tree writes as sources
of trouble. [Source][hermeticity]

Our recommended review asks:

- Does the tool embed wall-clock time, absolute host paths, random values, or
  environment-derived metadata? If so, establish an explicit normalization policy.
- Are ordered outputs produced from an ordering contract rather than incidental
  filesystem enumeration?
- Are all writes confined to declared outputs and permitted temporary storage?
- Does a clean, independently executed build produce equivalent intended results
  under the recorded inputs?

These are validation questions, not assertions that every tool supports a
particular normalization flag. Read the exact tool's supported API before adding
compiler or archive options.

## Use evidence appropriate to the claim

Our recommendation is to distinguish three observations: the action graph has
complete declarations, an execution succeeds in a constrained environment, and
independent executions produce the required equivalent output. A cache hit only
shows reuse for a computed key; it does not exercise the tool again or establish
that hidden dependencies are absent. The underlying risk is Bazel's documented
inability to account for undeclared input changes. [Source][sandbox]

Compare meaningful output properties, including bytes when byte reproducibility
is the requirement. Keep any deliberate variation documented at the owning rule
or packaging layer. Automated claim fixtures and remote CI are tracked separately
in [issue #1](https://github.com/JSGette/bazel-for-agents/issues/1).

## Evidence boundary

This page is source-verified at the versions in its metadata. It adds no executed
fixture or cross-platform compatibility result. The
[claim ledger](../verification/starlark-actions-testing.md) records the inspected
symbols and limitations.

[actions]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java
[sandbox]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/docs/sandboxing.md
[hermeticity]: https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/basics/hermeticity.md
