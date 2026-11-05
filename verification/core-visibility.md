# Visibility evidence

Verified 2026-11-05 against Bazel 9.3.1, commit
`fee2bf2d1c14bc2096068a4d46f1842472092044`.

## Claims

All rows use the [visibility reference at the pinned commit](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/concepts/visibility.md).
The section names below identify the evidence within that source. Recommendations
about keeping interfaces narrow are editorial guidance, not extra Bazel semantics.

| Claim ID | Bounded statement | Source section | Verification |
| --- | --- | --- | --- |
| `core.visibility.target` | Target visibility checks dependency edges during analysis; direct target declarations grant access within their package. | Target visibility; Rule target visibility | Source-verified; allowed/denied dependency exercised below. |
| `core.visibility.specifications` | Direct targets accept private/public, exact-package/subpackage, and package-group visibility entries with the scope stated on the page. | Visibility specifications | Source-verified; exact-package scope exercised below. Other forms were not individually tested. |
| `core.visibility.defaults` | For direct rule declarations, an omitted visibility uses package default_visibility, otherwise private. | Rule target visibility | Source-verified. No separate default-visibility probe. |
| `core.visibility.load` | Load visibility governs `.bzl` loading, allows its own package, uses package specifications, and is declared at most once at top level; negative specs and package-group labels are excluded. | Load visibility; Declaring load visibility; Deduplicating with package groups | Source-verified; top-level exact-package declaration and rejected external load exercised below. The after-load position is documented placement guidance. |
| `core.visibility.load-default` | Omitting a `.bzl` visibility declaration makes it public for loading. | Declaring load visibility | Source-verified. No separate omitted-declaration probe. |
| `core.visibility.independent` | A `.bzl` source target's visibility and its load visibility are independent. | Load visibility | Source-verified; public source target with restricted loading exercised below. |
| `core.visibility.macro-location` | Targets created within a symbolic macro use the innermost macro definition's package as declaration location; forwarding visibility exports the target to the caller. | Locations within symbolic macros | Source-verified only; no macro fixture. Delegation and finalizers are outside this page's scope. |

## Execution

Environment: Linux x86_64; official Bazel 9.3.1 binary whose SHA-256 was verified
in the [baseline probe](starlark-set.md). No external rulesets are declared.
The generated module locks are retained in the fixture. Bazel's own default
dependencies are not evidence for any separately selected ruleset stack.

Configuration: every invocation used `--ignore_all_rc_files` and `--batch`.
The JVM truststore argument below enables trust in the environment's HTTPS proxy
CA; TLS verification remained enabled. Inherited proxy configuration was retained.
No visibility, compatibility, or Starlark feature flags were changed.

From `examples/visibility`, the exact commands were:

```sh
/workspace/scratch/bazel-probe/bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //allowed:consumer
/workspace/scratch/bazel-probe/bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //denied:consumer
/workspace/scratch/bazel-probe/bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //...
```

From `examples/visibility/negative-load`:

```sh
/workspace/scratch/bazel-probe/bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //:consumer
```

For reproduction elsewhere, substitute the path to the same verified binary.
The JVM truststore location is an environment-specific prerequisite, not a
recommended project setting.

| Check | Expected | Observed |
| --- | --- | --- |
| `//allowed:consumer` | Helper load and target dependency accepted. | Exit 0; build completed successfully. |
| `//denied:consumer` | Analysis rejects dependency on `//lib:shared`. | Exit 1; visibility error identifies those two target labels. |
| Parent fixture `//...` | Normal wildcard build succeeds with intentional failures excluded. | Exit 0; two targets analyzed and build completed successfully. |
| Negative module `//:consumer` | Loading the restricted `.bzl` fails before analysis. | Exit 1; error says the Starlark file is not visible for loading from package `//`. |

The negative target is tagged `manual`; the separate negative-load module is
listed in the parent fixture's `.bazelignore`. Their commands are intentional
failure probes. They are not proposed fixes or disablement recipes.

No runtime executable is involved: this fixture checks package loading and target
analysis. It does not verify filesystem isolation, arbitrary external repository
mappings, symbolic macro delegation, or later Bazel versions.
