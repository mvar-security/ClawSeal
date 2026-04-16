#!/usr/bin/env python3
"""
ClawSeal Doctor — Health Check Command
========================================

Diagnoses ClawSeal installation and runtime environment.
Inspired by Microsoft AGT health check pattern.

Usage:
    clawseal doctor
"""

import os
import sys
import subprocess
import hashlib
from pathlib import Path
from typing import Tuple, List


class HealthCheck:
    """Health check result."""
    def __init__(self, name: str, status: str, message: str):
        self.name = name
        self.status = status  # "✅", "⚠️", "❌"
        self.message = message


def check_python_version() -> HealthCheck:
    """Check Python version >= 3.10."""
    version = sys.version_info
    if version >= (3, 10):
        return HealthCheck(
            "Python Version",
            "✅",
            f"Python {version.major}.{version.minor}.{version.micro}"
        )
    else:
        return HealthCheck(
            "Python Version",
            "❌",
            f"Python {version.major}.{version.minor} (requires >= 3.10)"
        )


def check_qseal_mode() -> HealthCheck:
    """Check QSEAL_SECRET configuration."""
    secret = os.getenv('QSEAL_SECRET')

    if not secret:
        return HealthCheck(
            "QSEAL Mode",
            "⚠️",
            "No QSEAL_SECRET set (will use demo mode)"
        )

    # Check if it's the demo secret
    demo_secret = hashlib.sha256(b"clawseal_demo_secret").hexdigest()
    if secret == demo_secret:
        return HealthCheck(
            "QSEAL Mode",
            "⚠️",
            "Demo mode (not production-ready)"
        )

    # Check secret strength
    if len(secret) < 32:
        return HealthCheck(
            "QSEAL Mode",
            "⚠️",
            f"Weak secret (length: {len(secret)}, recommend >= 64 hex chars)"
        )

    return HealthCheck(
        "QSEAL Mode",
        "✅",
        f"Production mode (secret length: {len(secret)} chars)"
    )


def check_pyyaml() -> HealthCheck:
    """Check PyYAML dependency."""
    try:
        import yaml
        version = getattr(yaml, '__version__', 'unknown')
        return HealthCheck(
            "PyYAML",
            "✅",
            f"Installed (version {version})"
        )
    except ImportError:
        return HealthCheck(
            "PyYAML",
            "❌",
            "Not installed (pip install PyYAML)"
        )


def check_flask() -> HealthCheck:
    """Check Flask dependency."""
    try:
        import flask
        version = getattr(flask, '__version__', 'unknown')
        return HealthCheck(
            "Flask",
            "✅",
            f"Installed (version {version})"
        )
    except ImportError:
        return HealthCheck(
            "Flask",
            "❌",
            "Not installed (pip install Flask)"
        )


def check_flask_sock() -> HealthCheck:
    """Check flask-sock dependency."""
    try:
        import flask_sock
        return HealthCheck(
            "Flask-Sock",
            "✅",
            "Installed (WebSocket support enabled)"
        )
    except ImportError:
        return HealthCheck(
            "Flask-Sock",
            "❌",
            "Not installed (pip install flask-sock)"
        )


def check_openssl() -> HealthCheck:
    """Check OpenSSL availability."""
    try:
        result = subprocess.run(
            ["openssl", "version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return HealthCheck(
                "OpenSSL",
                "✅",
                version
            )
        else:
            return HealthCheck(
                "OpenSSL",
                "⚠️",
                "Command failed (cryptographic operations may be limited)"
            )
    except FileNotFoundError:
        return HealthCheck(
            "OpenSSL",
            "⚠️",
            "Not found in PATH (cryptographic operations may be limited)"
        )
    except Exception as e:
        return HealthCheck(
            "OpenSSL",
            "⚠️",
            f"Check failed: {e}"
        )


def check_dashboard_server() -> HealthCheck:
    """Check if dashboard server is accessible."""
    try:
        import urllib.request
        import json

        req = urllib.request.Request(
            "http://localhost:8080/health",
            headers={"User-Agent": "ClawSeal-Doctor/1.0"}
        )

        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return HealthCheck(
                    "Dashboard Server",
                    "✅",
                    f"Running (status: {data.get('status', 'unknown')})"
                )
            else:
                return HealthCheck(
                    "Dashboard Server",
                    "⚠️",
                    f"Unexpected status: {response.status}"
                )
    except urllib.error.URLError:
        return HealthCheck(
            "Dashboard Server",
            "⚠️",
            "Not running (start with: clawseal-quickstart)"
        )
    except Exception as e:
        return HealthCheck(
            "Dashboard Server",
            "❌",
            f"Health check failed: {e}"
        )


def check_clawseal_import() -> HealthCheck:
    """Check if ClawSeal core can be imported."""
    try:
        from clawseal import ScrollMemoryStore, __version__
        return HealthCheck(
            "ClawSeal Core",
            "✅",
            f"Installed (version {__version__})"
        )
    except ImportError as e:
        return HealthCheck(
            "ClawSeal Core",
            "❌",
            f"Import failed: {e}"
        )


def run_all_checks() -> List[HealthCheck]:
    """Run all health checks."""
    return [
        check_python_version(),
        check_clawseal_import(),
        check_pyyaml(),
        check_flask(),
        check_flask_sock(),
        check_qseal_mode(),
        check_openssl(),
        check_dashboard_server(),
    ]


def print_results(checks: List[HealthCheck]):
    """Print health check results."""
    print("=" * 80)
    print("CLAWSEAL HEALTH CHECK")
    print("=" * 80)
    print()

    max_name_len = max(len(check.name) for check in checks)

    for check in checks:
        print(f"{check.status}  {check.name:<{max_name_len}}  {check.message}")

    print()
    print("=" * 80)

    # Count statuses
    passed = sum(1 for c in checks if c.status == "✅")
    warnings = sum(1 for c in checks if c.status == "⚠️")
    failed = sum(1 for c in checks if c.status == "❌")

    print(f"SUMMARY: {passed} passed, {warnings} warnings, {failed} failed")
    print("=" * 80)
    print()

    # Exit code based on failures
    if failed > 0:
        print("❌ Some critical checks failed. ClawSeal may not work correctly.")
        print()
        return 1
    elif warnings > 0:
        print("⚠️  Some checks have warnings. Review recommendations above.")
        print()
        return 0
    else:
        print("✅ All checks passed! ClawSeal is ready to use.")
        print()
        return 0


def main():
    """Run the doctor command."""
    checks = run_all_checks()
    exit_code = print_results(checks)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
