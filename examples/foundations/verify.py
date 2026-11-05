"""Run the foundation checks with a verified Bazel 9.3.1 executable."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bazel", type=Path, help="Path to a verified Bazel 9.3.1 executable")
    args = parser.parse_args()
    binary = args.bazel.resolve(strict=True)
    fixture = Path(__file__).resolve().parent
    # /tmp is outside the repository; this verifier is exercised on Linux.
    temporary = tempfile.TemporaryDirectory(prefix="bazel-foundations-", dir="/tmp")
    output_base = temporary.name
    try:
        base = [
            str(binary),
            "--ignore_all_rc_files",
            "--batch",
            "--output_base=" + output_base,
        ]
        truststore = os.environ.get("BAZEL_JAVA_TRUSTSTORE")
        if truststore:
            base.append("--host_jvm_args=-Djavax.net.ssl.trustStore=" + truststore)

        def run(*arguments, expect_failure=False):
            result = subprocess.run(base + list(arguments), cwd=fixture, text=True, capture_output=True)
            if expect_failure:
                assert result.returncode != 0, "Expected an analysis failure"
            else:
                assert result.returncode == 0, result.stdout + result.stderr
            return result

        assert "Build label: 9.3.1" in run("version").stdout
        run("build", "//:report")
        output = Path(run("info", "bazel-bin").stdout.strip())
        assert output.joinpath("greeting.txt").read_bytes() == b"Hello, Bazel!\n"
        assert output.joinpath("report.txt").read_bytes() == b"Greetings, Bazel!\n"
        assert not output.joinpath("greeting.metadata.txt").exists()

        labels = run("query", "deps(//:report)").stdout.splitlines()
        assert set(labels) == {"//:greeting", "//:message.tpl", "//:report", "//:runtime.txt"}
        files = run("cquery", "//:report", "--output=files").stdout.splitlines()
        assert len(files) == 1 and files[0].endswith("/report.txt"), files

        actions = run("aquery", "deps(//:report)", "--output=text").stdout
        assert actions.count("Mnemonic: TemplateExpand") == 2, actions
        assert "Mnemonic: FileWrite" in actions and "greeting.metadata.txt" in actions, actions
        assert "Inputs: [" + files[0].removesuffix("report.txt") + "greeting.txt]" in actions, actions
        assert "Inputs: [message.tpl]" in actions, actions

        runfiles = run(
            "cquery", "//:report", "--output=starlark",
            '--starlark:expr=[f.short_path for f in providers(target)["DefaultInfo"].default_runfiles.files.to_list()]',
        ).stdout
        assert json.loads(runfiles) == ["runtime.txt"], runfiles
        run("build", "//:greeting", "--output_groups=metadata")
        assert output.joinpath("greeting.metadata.txt").read_bytes() == b"person=Bazel\n"
        failure = run("build", "//:bad_provider", expect_failure=True)
        assert "'//:plain_file' does not have mandatory providers: 'GreetingInfo'" in failure.stderr
        print("PASS: exact outputs, default-output selection, query/cquery/aquery, runfiles, and provider rejection")
    finally:
        # Remove only convenience links generated into this run's output base.
        for link in fixture.glob("bazel-*"):
            if link.is_symlink() and link.resolve(strict=False).is_relative_to(Path(output_base)):
                link.unlink()
        temporary.cleanup()


if __name__ == "__main__":
    main()
