# Starlark basics: claim ledger

Verified 2026-11-05 against Bazel 9.3.1, commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`. Each source link below pins that commit.
The only executed example for these pages is the set fixture recorded below.
No claim here establishes behavior on all later Bazel releases or other Starlark
implementations. The collection-selection advice is an editorial recommendation.

## starlark.context.build

**Source-verified.** BUILD files declare targets by calling rules; their syntax
rejects function definitions and `for`/`if` statements while allowing
comprehensions and conditional expressions.

Sources: [BUILD file role](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-files.md#L20),
[syntax checker](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/DotBazelFileSyntaxChecker.java#L34),
[BUILD checker invocation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/PackageFactory.java#L578).

## starlark.context.bzl

**Source-verified.** `.bzl` files define extension symbols. Top-level `load`
statements import named symbols using string-literal arguments. Underscore-prefixed
symbols cannot be loaded from another file. Top-level `for` and `if` statements
are rejected.

Sources: [extension loading](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/build-files.md#L54),
[private symbols](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Resolver.java#L609),
[top-level for check](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Resolver.java#L757),
[top-level if check](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Resolver.java#L852).

## starlark.context.module

**Source-verified.** `MODULE.bazel` is the module manifest, including direct
dependencies. Its syntax checker rejects `load` and function definitions.

Sources: [module role](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/external/module.md#L13),
[module checker configuration](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/bazel/bzlmod/CompiledModuleFile.java#L107),
[rejected syntax](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/DotBazelFileSyntaxChecker.java#L109).

## starlark.syntax.import

**Source-verified.** Python `import`, `class`, `while`, `try`, and `raise` are
unsupported. The parser directs import users to `load` and raise users to `fail`.

Source: [forbidden keywords and diagnostics](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Parser.java#L400).

## starlark.syntax.control

**Source-verified.** `.bzl` functions may contain `for` and `if` statements; the
resolver specifically rejects these at top level.

Sources: [for resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Resolver.java#L757),
[if resolution](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/syntax/Resolver.java#L852).

## starlark.numeric.int

**Source-verified.** Starlark integers have arbitrary magnitude and exact
arithmetic. Source: [integer implementation/API documentation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/StarlarkInt.java#L23).

## starlark.numeric.float

**Source-verified.** Floating-point values and the `float()` constructor are
available. Source: [float built-in](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/MethodLibrary.java#L462).

## starlark.collections.list

**Source-verified.** Lists are mutable sequences with indexing and concatenation;
they can contain repeated values. Source: [list type documentation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/StarlarkList.java#L42).

## starlark.collections.dict

**Source-verified.** Dictionaries map hashable keys to values and iterate over
keys in insertion order. Sources: [dict semantics](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/Dict.java#L63),
[key hashability check](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/Dict.java#L273).

## starlark.set.default

**Source-verified and default use runtime-verified.**
`experimental_enable_starlark_set` defaults to true and controls availability of
the set type/constructor. The fixture passes without setting it explicitly.
Source: [flag declaration](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/packages/semantics/BuildLanguageOptions.java#L780).

## starlark.set.semantics

**Source-verified.** Sets contain unique hashable values, support membership and
union, are constructed with `set()` rather than a literal, preserve first-addition
iteration order, compare by elements independently of order, and reject mutation
once frozen. Source: [set implementation/API documentation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/net/starlark/java/eval/StarlarkSet.java#L40).
The executed subset is recorded separately below.

## starlark.collections.depset

**Source-verified.** Depsets support efficient transitive aggregation, are
immutable, have a homogeneous element type and a documented hashability
requirement, and suppress duplicates when flattened. They do not offer fast
membership; their default traversal order is deterministic but unspecified.
Source: [depset implementation/API documentation](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java#L43).

## starlark.collections.flatten

**Source-verified.** Converting a depset to a list traverses its nested graph.
Source: [toList traversal contract](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/collect/nestedset/Depset.java#L241).
Avoiding repeated flattening is a recommendation inferred from this cost.

## Executed fixture

**Claim ID:** `starlark.set.probe`; **status:** runtime-verified.

The [fixture source](../examples/starlark-set/probe.bzl) checks set construction,
duplicate elimination, length, membership, mutation, and union. It writes sorted
values and returns the output through `DefaultInfo(files = depset([out]))`.
It also exercises a `.bzl` rule loaded from BUILD in a module-based project.

Exact command run on 2026-11-05 from `examples/starlark-set/` on Linux x86_64:

```sh
/workspace/scratch/bazel-probe/bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //:sets
cat bazel-bin/sets.txt
```

The binary identity and SHA-256 were checked in the [original probe](starlark-set.md).
The truststore setting supplies the environment's proxy CA with TLS verification
retained. Rc files were ignored, no Starlark feature/compatibility flags were set,
and no external rulesets were declared. The fixture's module lock is retained.

Expected and observed: successful build; output `alpha`, `beta`, `delta`, `gamma`,
each on its own line with a final newline. The probe does not validate set
iteration order, freezing, invalid syntax/types, transitive depset behavior,
other platforms, or external ruleset compatibility.
