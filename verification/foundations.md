# Foundations fixture: Bazel 9.3.1

Verified 2026-11-05 on Linux x86_64. Fixture:
[examples/foundations](../examples/foundations/). No external rulesets are declared.
The generated `MODULE.bazel.lock` records module resolution, including Bazel's
implicit dependencies. This is a focused test of the concepts below, not a
language-ruleset or remote-execution compatibility test.

## Binary and effective configuration

- Official [Bazel 9.3.1 Linux x86_64 binary](https://github.com/bazelbuild/bazel/releases/download/9.3.1/bazel-9.3.1-linux-x86_64).
- SHA-256: `7f775b54bbec487efaf0f49ccda1d2ed02cd34f582edfdd6aeeec76e39ef585c`,
  matched against the [release checksum](https://github.com/bazelbuild/bazel/releases/download/9.3.1/bazel-9.3.1-linux-x86_64.sha256)
  in the initial baseline probe and rechecked here.
- Direct binary invocation; no Bazelisk wrapper; `--ignore_all_rc_files` and
  `--batch`; no compatibility or Starlark feature flags.
- A JVM truststore setting preserves TLS verification through this environment's
  HTTPS proxy. No credentials or environment-dependent tools are used by the
  fixture's template-expansion and file-writing actions.
- Default target configuration in this run: `k8-fastbuild`; execution platform
  reported by `aquery`: `@@platforms//host:host`. These are observations, not
  portable strings for production rules to hardcode.

## Reproduce

Run the [verification script](../examples/foundations/verify.py) from the repository
root. It takes an explicit path to a verified Bazel binary and checks the reported
version before building. The optional `BAZEL_JAVA_TRUSTSTORE` environment variable
supplies the truststore used in this environment; omit it when unnecessary.

The original manual probe began in a newly created fixture directory with no
previous outputs. The reproducible script creates its own fresh `/tmp` output
base on every invocation, so the metadata-absence assertion does not depend on
previous builds. It removes that temporary directory and only convenience
symlinks pointing into it when finished.

Exact successful invocation on 2026-11-05:

```bash
BAZEL_JAVA_TRUSTSTORE=/etc/ssl/certs/java/cacerts \
  python examples/foundations/verify.py \
  /workspace/scratch/bazel-probe/bazel-9.3.1
```

Observed stdout:

```text
PASS: exact outputs, default-output selection, query/cquery/aquery, runfiles, and provider rejection
```

The script invokes `build //:report`, `query 'deps(//:report)'`,
`cquery //:report --output=files`, `aquery 'deps(//:report)' --output=text`, a
Starlark `cquery` expression for runfiles, and explicit metadata-group selection.
It asserts exact bytes for all three generated files, the absence of metadata
before selection, graph-query results, and runfiles contents. Its final build
intentionally requests `//:bad_provider`; the script requires a nonzero exit and
the expected missing-provider diagnostic. Expected rejection therefore counts
as a successful verification, not a successful build of that target.

## Expected and observed results

All successful commands below exited 0. The final negative check exited 1.

| Check | Observed result |
| --- | --- |
| Build `//:report` | `bazel-bin/greeting.txt` contains `Hello, Bazel!` followed by a newline; `bazel-bin/report.txt` contains `Greetings, Bazel!` followed by a newline. Exact contents were asserted. |
| Default-output selection | In the fresh output directory, `greeting.metadata.txt` was absent after building `//:report`. |
| `query 'deps(//:report)'` | `//:greeting`, `//:message.tpl`, `//:report`, `//:runtime.txt`. |
| `cquery //:report --output=files` | `bazel-out/k8-fastbuild/bin/report.txt`. |
| `aquery 'deps(//:report)'` | Two `TemplateExpand` actions: `message.tpl` → `greeting.txt` → `report.txt`. A separate `FileWrite` action declares `greeting.metadata.txt`. Registration does not mean that the metadata output was built. |
| Provider and runfiles assertions | The report implementation checked that the producer's default files contain exactly its generated message and that its runfiles contain exactly `runtime.txt`. |
| Runfiles propagation | The Starlark `cquery` expression returned `["runtime.txt"]` for the report after merging the producer's default runfiles. |
| Explicit metadata group | `bazel-bin/greeting.metadata.txt` contains `person=Bazel` followed by a newline. Exact contents were asserted. |
| Missing required provider | Analysis failed with `'//:plain_file' does not have mandatory providers: 'GreetingInfo'`. |

The metadata-absence check requires a fresh output directory; an output from a
previous explicit metadata build may remain on disk. The verification does not
infer current action execution merely from an existing output file.

## Evidence and scope

The fixture's API usage is supported by these Bazel 9.3.1 sources:

- [Rule implementation, dependency attributes, and providers](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md):
  the `GreetingInfo` instance carries analysis information and a generated `File`
  to the consumer through a provider-constrained dependency.
- [Action API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/StarlarkActionFactoryApi.java):
  `declare_file`, `expand_template`, and `write` declare artifacts and producing
  actions. The generated greeting is the consumer action's template input.
- [DefaultInfo API](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/src/main/java/com/google/devtools/build/lib/starlarkbuildapi/DefaultInfoApi.java):
  default output files and runfiles are separate provider fields.
- [Output groups](https://github.com/bazelbuild/bazel/blob/fee2bf2d1c14bc2096068a4d46f1842472092044/site/en/extending/rules.md#requesting-output-files):
  the metadata artifact is selected explicitly through its output group.

Runtime verification covers this fixture on Linux x86_64. It checks runfiles
provider contents and merging, not executable runfiles lookup, manifest-based
lookup, Windows behavior, or toolchain selection. It uses only built-in actions;
process spawning, sandbox behavior, and remote execution remain outside its scope.
