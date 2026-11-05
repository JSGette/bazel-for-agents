---
title: "Declare shell entry points, libraries, and tests"
status: source-verified
bazel_baseline: "9.3.1"
bazel_verified: []
rulesets_verified: {"rules_shell": "0.8.0"}
platforms_verified: []
required_flags: []
prerequisites: ["core/labels-and-targets.md", "core/providers.md"]
claim_ids: ["shell.targets.inputs", "shell.targets.launcher", "shell.targets.environment"]
last_verified: "2026-11-05"
---

# Declare shell entry points, libraries, and tests

Use this when deciding where each script or runtime dependency belongs.
Load the public rules described in [setup](setup.md).

## Define the executable contract

`sh_binary` and `sh_test` require exactly one file in `srcs`. The rule accepts a
source or generated script, and its documented contract requires an executable
script. Put supporting files in `data`; use `deps` for shell libraries providing
`ShInfo`. `sh_library` aggregates its source files and dependency runfiles rather
than compiling them into a new program. [Executable rule][executable],
[library implementation][library]

A dependency makes files available; it does not insert `source` statements into
your script. Our recommendation is to make script-level imports explicit and
resolve their paths through the [runfiles library](runfiles.md).

## Choose launcher behavior intentionally

`use_bash_launcher` requests a generated Bash wrapper that initializes the
runfiles library, exports its environment, and invokes the main file using its
runfiles location. Its default is false. Ordinary non-Windows execution without
this wrapper exposes the original script through the rule's output symlink;
Windows has separate launcher handling. Do not assume setting `srcs` rewrites an
arbitrary script's interpreter or shell syntax. [Implementation][executable]

`env` supplies environment entries and `env_inherit` identifies values inherited
from the invocation environment; the implementation returns
`RunEnvironmentInfo`. It expands supported locations in `env` against `data`.
Prefer explicit, minimal values over inherited ambient settings when repeatable
behavior matters. [Environment construction][executable]

## Review tests as runtime programs

For a shell test, inspect its entry script, declared runtime tools/data,
interpreter, and exit behavior. Test data should be located through runfiles;
temporary outputs belong in the test's supplied writable locations. The
[execution-test guidance](../../testing/execution-tests.md) covers that Bazel
contract. Passing a shell test on one OS does not establish portability of its
external utilities or shell-specific syntax.

## Verification boundary

This is source-verified guidance for the versions above. No integration build,
resolved dependency graph, or platform execution is claimed by this page. See
the [native ruleset evidence](../../verification/rulesets-native.md) for source
identity and coverage; executable integration coverage is follow-up work.

[executable]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_executable.bzl
[library]: https://github.com/bazel-contrib/rules_shell/blob/c02969a1822191a179cd70c0cedd076385446a26/shell/private/sh_library.bzl
