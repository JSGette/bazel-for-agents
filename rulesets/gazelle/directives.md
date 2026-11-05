---
title: "Control Gazelle without fighting generated files"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"gazelle": "0.54.0"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/gazelle/generation.md"]
claim_ids: ["gazelle.directives.scope", "gazelle.directives.resolution", "gazelle.directives.ownership", "gazelle.directives.macros"]
last_verified: "2026-11-05"
---

# Control Gazelle without fighting generated files

## Use this when

Gazelle chooses the wrong dependency label, overwrites an intentional change,
walks an unsuitable subtree, or needs to recognize a project macro.

## Put policy next to the owned code

Directives are top-level BUILD comments of the form `# gazelle:key value`.
Most settings apply to that directory and descendants; use each directive's
specific contract to understand exceptions. Place a narrowly scoped directive
where the policy starts, rather than changing generation for unrelated code.
[Directive syntax and scope](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

| Decision | Relevant directive | Boundary |
| --- | --- | --- |
| Set Go import identity | `prefix` | Controls generated import paths beneath this location |
| Resolve a specific import | `resolve` | Maps source language/import language/import string to a label |
| Resolve an import pattern | `resolve_regexp` | Pattern and optional replacement captures must match the intended imports |
| Omit input files or a tree | `exclude` | Matching source files are excluded; matching directories are not traversed |
| Preserve one BUILD file | `ignore` | Rules remain readable/indexable; descendant BUILD files may still change |
| Restrict generated languages | `lang` | Limits indexing and generation to listed languages |
| Update existing BUILD files only | `generation_mode update_only` | Does not create BUILD files in new directories |

Sources: [General directive contracts](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md);
[Go-specific prefix behavior](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/language/go/reference.md).

## Teach macros explicitly

`map_kind` maps a generated rule kind to another kind and its load location.
The replacement must accept the attributes Gazelle produces and preserve the
relevant meaning. This is an API compatibility commitment by the project macro,
not something Gazelle proves. Existing rules of the original kind are not
converted automatically by that directive.
[map_kind contract](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

`alias_kind` instead teaches Gazelle to index and update an existing wrapper as
its underlying rule kind. It does not force newly generated targets to call that
wrapper. Choose based on whether the goal is generation policy or recognition
of an existing API. [alias_kind contract](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

## Preserve the smallest exceptional piece

A `keep` annotation can protect a rule, attribute, or list entry. It is useful
for dependencies inferred only after a generator runs, because Gazelle cannot
read absent generated source imports. Add a reason so the next editor can tell
whether the annotation is still necessary.
[keep comments and generated sources](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md).

`build_tags` configures Gazelle's source interpretation. Treat it as generation
configuration and independently check the Go build configuration that will
compile the targets; the two tools have different jobs.
[build_tags control](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/gazelle-reference.md);
[Go generation configuration](https://github.com/bazel-contrib/bazel-gazelle/blob/ed9d0f2d159457270694ce66803ef471b5ac3be3/language/go/config.go).

For third-party modules, put generation overrides in
`go_deps.gazelle_override` rather than editing downloaded repositories. See
[Go dependencies](../go/dependencies.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#gazelle-directives).
