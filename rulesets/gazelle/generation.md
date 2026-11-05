---
title: "Generate and review BUILD declarations with Gazelle"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"gazelle": "0.54.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/go/setup.md"]
claim_ids: ["gazelle.generation.entry", "gazelle.generation.modes", "gazelle.generation.index"]
last_verified: "2026-11-05"
---

# Generate and review BUILD declarations with Gazelle

## Use this when

Maintain BUILD declarations after source imports change, add generated-code
support, or make a build-generation change reviewable.

## Give the generator a defined scope

`@gazelle//:def.bzl` exports `gazelle` and `gazelle_binary`. The former provides a
runnable generator target; the latter assembles a binary with selected language
extensions. Default extensions cover Go, protocol buffers, and visibility.
Other languages require their own extension rather than being implied by a
Gazelle dependency. [Exports and DEFAULT_LANGUAGES](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/def.bzl);
[Custom generator construction](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/internal/gazelle_binary.bzl).

The generator resolves source-language imports to Bazel labels and merges
language-generated declarations with existing BUILD files. Explicit resolution
directives and indexed library rules participate in that process. Generation
success is not compilation or a proof that an external label exists.
[Dependency-resolution behavior](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/README.md).

Repository recommendation: keep one documented project entry point with its
language extensions and default arguments. Separate generation policy from
Go dependency resolution, which belongs to [go_deps](../go/dependencies.md).

## Preview and apply deliberately

The `gazelle` target supports `command`, `mode`, `build_tags`, `prefix`,
`extra_args`, `data`, and `env`. `update` is its default command. Output mode
`fix` writes merged BUILD files; `print` displays the resulting files; `diff`
displays changes without writing them. The `fix` command and `fix` output mode
are different controls: the command enables additional transformations, while
the mode determines how results are emitted.
[Runner attribute schema](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/def.bzl);
[Commands and output modes](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

Repository recommendation: inspect the generated diff, especially loads,
visibility, build constraints, dependencies, and manually maintained attributes.
After accepting changes, compile and test the affected targets separately.
Preserve intentional exceptional content with narrow directives or `keep`
annotations, rather than allowing every regeneration to undo it.
[keep annotations and directives](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

## Large and mixed-language trees

Recursion controls which directories are updated. Indexing controls which BUILD
rules inform import resolution; disabling recursion does not itself disable full
indexing. Lazy indexing can reduce the visited scope, but nonstandard layouts may
need `go_search` or `proto_search` mappings. Restrict language selection when a
subtree has a separate generation owner.
[Recursion, index, and lang controls](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md);
[Lazy-index search mappings](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/README.md).

Continue with [directives](directives.md). No generator invocation was run for
this page, so the API reference does not claim a clean regeneration of any
particular repository.

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#gazelle-generation).
