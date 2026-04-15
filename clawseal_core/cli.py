#!/usr/bin/env python3
"""
ClawSeal CLI — Command-line interface for ClawSeal memory management

Commands:
  clawseal init   — Initialize ClawSeal environment (generate QSEAL_SECRET, setup venv)
  clawseal verify — Verify ClawSeal installation and configuration
  clawseal demo   — Run the three-layer demo

Copyright 2026 Shawn Cohen
Licensed under Apache-2.0
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def init_command():
    """Initialize ClawSeal environment"""
    print("🔧 ClawSeal Initialization")
    print("=" * 60)

    # Check if QSEAL_SECRET already exists
    existing_secret = os.getenv("QSEAL_SECRET")
    if existing_secret and existing_secret != "test_secret_key_for_demo":
        print(f"✅ QSEAL_SECRET already set (length: {len(existing_secret)})")
        print("   Skipping secret generation.")
    else:
        print("\n📝 Step 1: Generate QSEAL_SECRET (256-bit)")
        print("-" * 60)

        # Generate 256-bit secret using openssl
        try:
            result = subprocess.run(
                ["openssl", "rand", "-hex", "32"],
                capture_output=True,
                text=True,
                check=True
            )
            new_secret = result.stdout.strip()
            print(f"✅ Generated: {new_secret[:16]}...{new_secret[-16:]}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating secret: {e}")
            print("   Install openssl: brew install openssl (macOS) or apt install openssl (Linux)")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ openssl command not found")
            print("   Install openssl: brew install openssl (macOS) or apt install openssl (Linux)")
            sys.exit(1)

        # Determine shell profile
        home = Path.home()
        shell = os.getenv("SHELL", "")

        if "zsh" in shell:
            profile = home / ".zshrc"
        elif "bash" in shell:
            profile = home / ".bashrc"
        else:
            profile = home / ".profile"

        print(f"\n📝 Step 2: Add to shell profile ({profile})")
        print("-" * 60)

        # Check if already in profile
        if profile.exists():
            with open(profile, "r") as f:
                content = f.read()
                if "QSEAL_SECRET" in content:
                    print("⚠️  QSEAL_SECRET already exists in shell profile")
                    print("   Manual action required:")
                    print(f"   1. Open {profile}")
                    print("   2. Replace old QSEAL_SECRET with:")
                    print(f'      export QSEAL_SECRET="{new_secret}"')
                else:
                    # Append to profile
                    with open(profile, "a") as f:
                        f.write(f"\n# ClawSeal QSEAL_SECRET (generated {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()})\n")
                        f.write(f'export QSEAL_SECRET="{new_secret}"\n')
                    print(f"✅ Added QSEAL_SECRET to {profile}")
        else:
            # Create new profile
            with open(profile, "w") as f:
                f.write(f'# ClawSeal QSEAL_SECRET\nexport QSEAL_SECRET="{new_secret}"\n')
            print(f"✅ Created {profile} with QSEAL_SECRET")

        print(f"\n⚠️  IMPORTANT: Reload your shell or run:")
        print(f"   source {profile}")

    print("\n✅ ClawSeal initialization complete!")
    print("\nNext steps:")
    print("  1. Reload shell: source ~/.zshrc (or ~/.bashrc)")
    print("  2. Verify: clawseal verify")
    print("  3. Run demo: clawseal demo")


def verify_command():
    """Verify ClawSeal installation and configuration"""
    print("🔍 ClawSeal Verification")
    print("=" * 60)

    errors = []

    # Check Python version
    print("\n1. Python version:")
    py_version = sys.version_info
    if py_version >= (3, 10):
        print(f"   ✅ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print(f"   ❌ Python {py_version.major}.{py_version.minor}.{py_version.micro} (requires 3.10+)")
        errors.append("Python version too old")

    # Check QSEAL_SECRET
    print("\n2. QSEAL_SECRET:")
    secret = os.getenv("QSEAL_SECRET")
    if not secret:
        print("   ❌ Not set")
        errors.append("QSEAL_SECRET not set")
    elif secret == "test_secret_key_for_demo":
        print("   ⚠️  Using demo secret (DO NOT use in production)")
    elif len(secret) >= 32:
        print(f"   ✅ Set (length: {len(secret)})")
    else:
        print(f"   ⚠️  Set but short (length: {len(secret)}, recommend 64+)")

    # Check PyYAML
    print("\n3. PyYAML dependency:")
    try:
        import yaml
        print(f"   ✅ PyYAML {yaml.__version__} installed")
    except ImportError:
        print("   ❌ PyYAML not installed")
        errors.append("PyYAML not installed")

    # Check openssl
    print("\n4. OpenSSL binary:")
    try:
        result = subprocess.run(
            ["openssl", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"   ✅ {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ openssl not found")
        errors.append("openssl not installed")

    # Check ClawSeal package
    print("\n5. ClawSeal package:")
    try:
        from clawseal import ScrollMemoryStore, __version__
        print(f"   ✅ ClawSeal {__version__} importable")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        errors.append("ClawSeal package not importable")

    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ Verification failed ({len(errors)} errors)")
        for error in errors:
            print(f"   • {error}")
        sys.exit(1)
    else:
        print("✅ All checks passed!")
        print("\nClawSeal is ready to use.")


def demo_command():
    """Run the three-layer demo"""
    print("🚀 ClawSeal Three-Layer Demo")
    print("=" * 60)

    # Check if we're in the ClawSeal repository
    if not Path("run_full_demo.sh").exists():
        print("❌ Error: run_full_demo.sh not found")
        print("   This command must be run from the ClawSeal repository root.")
        print("   Clone: git clone https://github.com/mvar-security/ClawSeal.git")
        sys.exit(1)

    # Check QSEAL_SECRET
    secret = os.getenv("QSEAL_SECRET")
    if not secret:
        print("❌ Error: QSEAL_SECRET not set")
        print("   Run: clawseal init")
        sys.exit(1)

    print("\nRunning three-layer demo...\n")

    # Run the demo script
    try:
        subprocess.run(["bash", "run_full_demo.sh"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Demo failed with exit code {e.returncode}")
        sys.exit(1)

    print("\n✅ Demo complete!")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="clawseal",
        description="ClawSeal — Cryptographic Memory for AI Agents",
        epilog="Documentation: https://github.com/mvar-security/ClawSeal"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ClawSeal 1.0.2"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize ClawSeal environment (generate QSEAL_SECRET)"
    )

    # verify command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify ClawSeal installation and configuration"
    )

    # demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run the three-layer demo"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_command()
    elif args.command == "verify":
        verify_command()
    elif args.command == "demo":
        demo_command()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
