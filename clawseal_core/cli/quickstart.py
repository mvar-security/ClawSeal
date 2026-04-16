#!/usr/bin/env python3
"""
ClawSeal Quickstart Command
============================

One-command demo: starts dashboard, runs Layer 1/2/3 demos, opens browser.

Usage:
    clawseal quickstart
"""

import os
import sys
import time
import hashlib
import webbrowser
import subprocess
import threading
from pathlib import Path

def check_qseal_secret():
    """Check if QSEAL_SECRET is set, generate demo key if not."""
    if not os.getenv('QSEAL_SECRET'):
        print("⚠️  QSEAL_SECRET not set")
        print("   Generating demo key for quickstart...")
        demo_secret = hashlib.sha256(b"clawseal_demo_secret").hexdigest()
        os.environ['QSEAL_SECRET'] = demo_secret
        print("   ✅ Demo key generated")
        print()
        print("   NOTE: For production use, set a secure QSEAL_SECRET:")
        print("   export QSEAL_SECRET=$(openssl rand -hex 32)")
        print()

def start_dashboard():
    """Start the Flask dashboard server."""
    print("🚀 Starting ClawSeal dashboard...")
    print()

    # Get dashboard app path
    dashboard_dir = Path(__file__).parent.parent / "dashboard"
    app_path = dashboard_dir / "app.py"

    if not app_path.exists():
        print(f"❌ Dashboard app not found at {app_path}")
        sys.exit(1)

    # Start Flask in subprocess
    process = subprocess.Popen(
        [sys.executable, str(app_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Wait for server to start (check for "Running on" in output)
    print("   Waiting for server to start...")
    for line in process.stdout:
        print(f"   {line.strip()}")
        if "Running on" in line or "WARNING" in line:
            break

    return process

def open_browser():
    """Open browser to dashboard."""
    print()
    print("🌐 Opening dashboard in browser...")
    time.sleep(1.5)  # Give server a moment to fully initialize
    webbrowser.open("http://localhost:8080")
    print("   ✅ Browser opened to http://localhost:8080")
    print()

def main():
    """Run the quickstart sequence."""
    print("=" * 80)
    print("CLAWSEAL QUICKSTART")
    print("=" * 80)
    print()
    print("This demo will:")
    print("  1. Start the ClawSeal dashboard server")
    print("  2. Open your browser to http://localhost:8080")
    print("  3. Run Layer 1/2/3 demos with real-time visualization")
    print()
    print("Watch the drift animate from 100% → 0% as ClawSeal activates.")
    print()

    # Check/generate QSEAL secret
    check_qseal_secret()

    # Start dashboard
    server_process = start_dashboard()

    # Open browser
    open_browser()

    print("=" * 80)
    print("DEMO RUNNING")
    print("=" * 80)
    print()
    print("   Dashboard: http://localhost:8080")
    print("   Press Ctrl+C to stop the server")
    print()

    try:
        # Keep process alive
        server_process.wait()
    except KeyboardInterrupt:
        print()
        print("🛑 Stopping dashboard...")
        server_process.terminate()
        server_process.wait()
        print("   ✅ Dashboard stopped")
        print()

if __name__ == "__main__":
    main()
