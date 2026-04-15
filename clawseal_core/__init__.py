"""
ClawSeal — Cryptographic Memory for AI Agents

Stateless LLMs become stateful agents with tamper-evident memory,
zero database dependencies.

Copyright 2026 Shawn Cohen
Licensed under Apache-2.0
"""

__version__ = "1.0.2"
__author__ = "Shawn Cohen"
__license__ = "Apache-2.0"

from clawseal.memory.scroll_memory_store import ScrollMemoryStore

__all__ = ["ScrollMemoryStore", "__version__"]
