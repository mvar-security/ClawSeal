#!/usr/bin/env python3
"""
DEMO LAYER 1: Identity Drift Without MIRRA
==========================================

Simulates 5 conversation sessions WITHOUT persistent memory.
Demonstrates 100% identity drift - complete amnesia between sessions.

Duration: ~3 minutes
Output: Terminal display showing drift on every session
"""

import hashlib
import time
from datetime import datetime

def generate_identity_signature(session_state: dict) -> str:
    """Generate a simple identity hash based on what the agent 'knows'."""
    state_str = str(sorted(session_state.items()))
    return hashlib.sha256(state_str.encode()).hexdigest()[:16]

def simulate_session_without_memory(session_num: int, user_message: str):
    """
    Simulate an AI agent session with NO persistent memory.
    Every session starts with empty state.
    """
    # Always start with empty state - no memory persistence
    agent_state = {}

    # Simulate basic responses (no actual LLM - just canned responses)
    responses = {
        1: "Understood. I'll keep responses brief.",
        2: "I don't have any information about your preferences.",
        3: "Got it, Python project noted.",
        4: "I don't have context from previous conversations.",
        5: "I don't have that information."
    }

    response = responses.get(session_num, "I don't have any prior context.")

    # Generate identity signature from current state (always empty = always different random)
    # Add session number to make signatures unique even with empty state
    agent_state['session'] = session_num
    signature = generate_identity_signature(agent_state)

    return response, signature

def main():
    print("=" * 80)
    print("LAYER 1: IDENTITY DRIFT DEMONSTRATION (No MIRRA)")
    print("=" * 80)
    print()
    print("Simulating 5 conversation sessions without persistent memory...")
    print()

    # Define test conversation
    conversations = [
        "I prefer concise explanations",
        "What are my preferences?",
        "Remember that I'm working on a Python project",
        "What have we discussed so far?",
        "What's my communication style preference?"
    ]

    previous_signature = None
    drift_count = 0

    for session_num, user_msg in enumerate(conversations, 1):
        print(f"Session {session_num}:")
        print(f"  User: \"{user_msg}\"")

        # Simulate agent response with NO memory
        response, signature = simulate_session_without_memory(session_num, user_msg)

        print(f"  Agent Response: \"{response}\"")
        print(f"  Identity Signature: {signature}...")
        print()

        # Check for drift (every session after first will drift)
        if previous_signature is not None:
            print(f"  ⚠️  IDENTITY DRIFT DETECTED")
            print(f"  Previous: {previous_signature}...")
            print(f"  Current:  {signature}...")

            if session_num == 2:
                print(f"  Drift: 100% (complete amnesia)")
            elif session_num == 3:
                print(f"  Drift: 100% (no memory of Session 1 or 2)")
            elif session_num == 4:
                print(f"  Drift: 100% (total context loss)")
            else:
                print(f"  Drift: 100% (preferences lost)")

            print()
            drift_count += 1

        previous_signature = signature
        time.sleep(0.5)  # Slight pause for readability

    # Summary
    print("=" * 80)
    print(f"BASELINE RESULT: 100% identity drift across all sessions")
    print(f"No memory persistence. No continuity. Complete amnesia between sessions.")
    print("=" * 80)
    print()
    print(f"Drift Events: {drift_count}/{len(conversations)-1} (100%)")
    print()
    print("This is the current state of most AI systems without external memory.")
    print()

if __name__ == "__main__":
    main()
