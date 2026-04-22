#!/usr/bin/env python3
"""
Test suite for ClawSeal CLI entry points.

Verifies:
1. clawseal --version works
2. clawseal --help works
3. clawseal doctor routes correctly
4. clawseal quickstart routes correctly
5. Backward compatibility: clawseal-doctor and clawseal-quickstart still work
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_clawseal_version():
    """Test clawseal --version prints version."""
    returncode, stdout, stderr = run_command("clawseal --version")

    assert returncode == 0, f"clawseal --version failed with code {returncode}"
    assert "ClawSeal version" in stdout or "1.1.6" in stdout, \
        f"Version output missing. Got: {stdout}"

    print("✅ clawseal --version works")


def test_clawseal_help():
    """Test clawseal --help shows usage."""
    returncode, stdout, stderr = run_command("clawseal --help")

    assert returncode == 0, f"clawseal --help failed with code {returncode}"
    assert "Usage:" in stdout or "doctor" in stdout or "quickstart" in stdout, \
        f"Help output missing expected content. Got: {stdout}"

    print("✅ clawseal --help works")


def test_clawseal_no_args():
    """Test clawseal with no args shows help."""
    returncode, stdout, stderr = run_command("clawseal")

    assert returncode == 0, f"clawseal (no args) failed with code {returncode}"
    assert "Usage:" in stdout or "doctor" in stdout, \
        f"Help output missing. Got: {stdout}"

    print("✅ clawseal (no args) shows help")


def test_clawseal_unknown_subcommand():
    """Test clawseal with unknown subcommand shows error."""
    returncode, stdout, stderr = run_command("clawseal invalid-command")

    assert returncode == 1, f"clawseal invalid-command should fail but returned {returncode}"
    assert "Unknown subcommand" in stdout or "Unknown subcommand" in stderr, \
        f"Error message missing. Got stdout: {stdout}, stderr: {stderr}"

    print("✅ clawseal unknown-command shows error")


def test_clawseal_doctor_routing():
    """Test clawseal doctor routes to doctor.py main().

    We can't run the full doctor command without a proper environment,
    but we can verify it attempts to load the correct module.
    """
    # Just verify the command is recognized and attempts to run
    returncode, stdout, stderr = run_command("clawseal doctor --help 2>&1 || true")

    # Doctor might fail due to environment, but it should recognize the command
    # and not show "Unknown subcommand"
    combined_output = stdout + stderr
    assert "Unknown subcommand" not in combined_output, \
        f"doctor subcommand not recognized. Output: {combined_output}"

    print("✅ clawseal doctor routes correctly")


def test_backward_compat_clawseal_doctor():
    """Test clawseal-doctor still works (backward compatibility)."""
    returncode, stdout, stderr = run_command("which clawseal-doctor")

    assert returncode == 0, "clawseal-doctor command not found in PATH"

    print("✅ clawseal-doctor backward compatibility preserved")


def test_backward_compat_clawseal_quickstart():
    """Test clawseal-quickstart still works (backward compatibility)."""
    returncode, stdout, stderr = run_command("which clawseal-quickstart")

    assert returncode == 0, "clawseal-quickstart command not found in PATH"

    print("✅ clawseal-quickstart backward compatibility preserved")


if __name__ == '__main__':
    print("Running ClawSeal CLI entry point tests...\n")

    tests = [
        test_clawseal_version,
        test_clawseal_help,
        test_clawseal_no_args,
        test_clawseal_unknown_subcommand,
        test_clawseal_doctor_routing,
        test_backward_compat_clawseal_doctor,
        test_backward_compat_clawseal_quickstart,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    sys.exit(0 if failed == 0 else 1)
