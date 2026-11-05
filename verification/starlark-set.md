# Bazel 9.3.1 baseline probe

Checked 2026-11-05 on Linux x86_64.

Official binary: https://github.com/bazelbuild/bazel/releases/download/9.3.1/bazel-9.3.1-linux-x86_64

Checksum source: https://github.com/bazelbuild/bazel/releases/download/9.3.1/bazel-9.3.1-linux-x86_64.sha256

Verified SHA-256: `7f775b54bbec487efaf0f49ccda1d2ed02cd34f582edfdd6aeeec76e39ef585c`.

Fixture: [examples/starlark-set](../examples/starlark-set/).

The commands below were run from `/workspace/scratch/bazel-probe`, which held the
downloaded binary and original fixture. The source and generated module lock were
then copied unchanged into this draft. To repeat, use the fixture directory and
substitute the verified binary's path for `./bazel-9.3.1`.

```sh
./bazel-9.3.1 --ignore_all_rc_files --batch version
./bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts build //:sets
./bazel-9.3.1 --ignore_all_rc_files --batch --host_jvm_args=-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts aquery //:sets --output=text
cat bazel-bin/sets.txt
```

Version reports `Build label: 9.3.1`, built `Wed Oct 21 00:49:41 2026`.

Build passed. The rule exercises `set([...])`, deduplication, `len`, membership, `add`, set union `|`, and `sorted`; declares an output with `ctx.actions.declare_file`; registers `ctx.actions.write`; returns `DefaultInfo(files = depset([out]))`.

The generated output is:

```text
alpha
beta
delta
gamma
```

`aquery` reports a `FileWrite` action for `//:sets`, execution platform `@@platforms//host:host`, no inputs, output `bazel-out/k8-fastbuild/bin/sets.txt`.

No Starlark feature flags, compatibility flags, or repository rc files were used. A JVM truststore override was required because the binary's embedded JDK did not trust the environment's HTTPS proxy CA. TLS verification remained enabled. The probe declares no external dependencies, but Bazel resolves its default platform dependency through BCR. This probe does not establish compatibility for any external ruleset or remote execution service.
