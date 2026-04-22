#!/usr/bin/env python3
"""
ClawSeal — Unified CLI Entry Point
===================================

Subcommand dispatcher routing to existing doctor and quickstart logic.

Usage:
    clawseal --version              Print version
    clawseal --help                 Show this help
    clawseal doctor                 Run health check
    clawseal quickstart             Interactive setup wizard

Backward compatibility:
    clawseal-doctor                 Still available as direct alias
    clawseal-quickstart             Still available as direct alias
"""

import sys
import importlib.metadata


def print_version():
    """Print ClawSeal version from package metadata."""
    try:
        version = importlib.metadata.version('clawseal')
        print(f"ClawSeal version {version}")
    except importlib.metadata.PackageNotFoundError:
        print("ClawSeal (development version)")


def print_help():
    """Print help message."""
    print(__doc__)


def route_to_doctor():
    """Route to existing doctor command."""
    from clawseal.cli.doctor import main as doctor_main
    doctor_main()


def route_to_quickstart():
    """Route to existing quickstart command."""
    from clawseal.cli.quickstart import main as quickstart_main
    quickstart_main()


def main():
    """Main entry point for unified clawseal command."""
    # Handle no arguments
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    # Handle flags
    if sys.argv[1] == '--version':
        print_version()
        sys.exit(0)
    elif sys.argv[1] in ('--help', '-h', 'help'):
        print_help()
        sys.exit(0)

    # Handle subcommands
    subcommand = sys.argv[1]

    if subcommand == 'doctor':
        # Remove 'doctor' from argv so doctor.main() sees clean args
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        route_to_doctor()
    elif subcommand == 'quickstart':
        # Remove 'quickstart' from argv so quickstart.main() sees clean args
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        route_to_quickstart()
    else:
        # Unknown subcommand
        print(f"Error: Unknown subcommand '{subcommand}'")
        print()
        print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
