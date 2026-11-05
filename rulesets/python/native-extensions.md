---
title: "Connect Python runtimes to C and C++ extensions"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_python": "2.4.6"}
platforms_verified: []
required_flags: []
prerequisites: ["rulesets/python/setup.md", "rulesets/python/targets.md"]
claim_ids: ["python.native.headers", "python.native.extension", "python.native.abi", "python.native.libs"]
last_verified: "2026-11-05"
---

# Connect Python runtimes to C and C++ extensions

## Use this when

Build an extension from native source, consume Python headers, or embed Python
inside a native application. This is an ABI and toolchain integration, not just
a Python dependency declaration.

## Obtain headers through the selected runtime

`@rules_python//python/cc:current_py_cc_headers` forwards the active Python
C/C++ toolchain's header providers. The adjacent `current_py_cc_headers_abi3`
target requests its ABI3 header set and fails if the selected toolchain does not
provide one. This keeps header selection tied to the target configuration.
Do not infer the target headers from the Python interpreter installed on the
machine running Bazel.
[Public targets](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/cc/BUILD.bazel);
[Resolution and failure behavior](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/current_py_cc_headers.bzl).

The `current_py_cc_libs` target separately forwards library/linking information
from that toolchain, including shared-library ownership hints. Header access,
linking libpython, and loading a Python extension are separate requirements;
inspect the selected providers and platform linker behavior for the particular
consumer. [Library forwarding](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/current_py_cc_libs.bzl).

## Recognize the current extension API

`@rules_python//python/cc:py_extension.bzl` exports `py_extension`. It is explicitly
experimental in 2.4.6. Its macro constructs native compilation/shared-library
targets, adds Python headers, handles platform-specific linking, and wraps the
result with `PyInfo` and runtime files for Python consumers.
[Public experimental API](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/cc/py_extension.bzl);
[Macro implementation](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_macro.bzl);
[Python wrapper](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_rule.bzl).

| Input | Contract |
| --- | --- |
| `srcs`, `hdrs`, compilation options | Native sources compiled for this extension |
| `deps` | Native libraries linked into the extension |
| `dynamic_deps` | Shared-library dependencies |
| `linkopts` | Options for the internal source library |
| `user_link_flags` | Options passed to shared-library linking |
| `module_name` | Output module basename; otherwise the target name |
| `imports` | Additional Python import search paths |

These are the macro's documented distinctions. Repository recommendation: keep
linker options attached to their actual owner; do not use a global process
library path to compensate for missing runtime dependencies.
[Arguments and wiring](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_macro.bzl).

## ABI labels are not an ABI proof

The wrapper uses the resolved toolchain's `soabi` in its regular filename and
chooses `.pyd` for Windows or `.so` otherwise. With nonempty `py_limited_api`, it
instead emits an `.abi3` filename. In the inspected macro/wrapper, that parameter
does not add a `Py_LIMITED_API` compilation definition or validate that the source
uses only the limited API. Do not claim that setting this parameter alone creates
a stable-ABI extension. Verify compilation defines, exported initialization
symbol, headers, and runtime imports separately.
[Compilation argument flow](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_macro.bzl);
[Filename and provider construction](https://github.com/bazel-contrib/rules_python/blob/943362ffab1a2e8488f50b8554256f9330d3837e/python/private/cc/py_extension_rule.bzl).

Repository recommendation: record the Python ABI/threading mode, target platform,
C/C++ toolchain, transitive native libraries, and import test result together.
An upstream platform branch in source is evidence of intended handling, not a
successful local test on that platform. For prebuilt native wheels, start with
[dependency platform selection](dependencies.md).

## Verification boundary

This page reviews exact release APIs. No project module graph, SDK installation,
platform build, or integration fixture was executed for this page. These versions
are source references, not a tested dependency combination.
See the [claim record](../../verification/rulesets-go-python.md#python-native-extensions).
