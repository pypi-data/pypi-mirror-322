# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=duplicate-code
import os
import subprocess

script_path = os.path.realpath(__file__)
testdir = os.path.dirname(script_path)
cmd = ["python", "-c", "import biophony; biophony.fastqgen_cli()"]

def test_help():
    for opt in ["-h", "--help"]:
        with subprocess.Popen(cmd + [opt], stdout=subprocess.PIPE) as proc:
            assert proc.wait() == 0

def test_default_params():
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        assert proc.wait() == 0
        lines = proc.stdout.readlines()
        assert len(lines) > 0

def test_n_reads():
    for n in range(4):
        with subprocess.Popen(cmd + ["-c", str(n)], stdout=subprocess.PIPE
                              ) as proc:
            assert proc.wait() == 0
            lines = proc.stdout.readlines()
            assert len(lines) == n * 4
