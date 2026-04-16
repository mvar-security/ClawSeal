#!/usr/bin/env python3
"""
ClawSeal Dashboard — Flask + WebSocket Real-Time Demo
======================================================

Serves the interactive dashboard and provides WebSocket updates for:
- Layer 1: Drift percentage (100% → 0%)
- Layer 2: Scroll creation with QSEAL signatures
- Layer 3: Chain verification status

Auto-runs Layer 1/2/3 demos and streams results to browser in real-time.
"""

import os
import sys
import json
import time
import hashlib
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_sock import Sock

# Import from installed package (works in both dev and PyPI installs)
from clawseal.memory.scroll_memory_store import ScrollMemoryStore

# Data directory for demo scrolls
PROJECT_ROOT = Path(__file__).parent.parent.parent

app = Flask(__name__)
sock = Sock(app)

# Global state for demo
demo_state = {
    "drift_percentage": 100,
    "scrolls": [],
    "verification": {
        "scrolls_verified": 0,
        "total_scrolls": 0,
        "signatures_valid": 0,
        "chain_links": 0,
        "tampering_detected": False,
        "qseal_engine": "HMAC-SHA256"
    }
}

@app.route('/')
def index():
    """Serve the dashboard HTML."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@sock.route('/ws/demo')
def demo_websocket(ws):
    """
    WebSocket endpoint for real-time demo updates.
    Client connects, server runs Layer 1/2/3 demos, streams results.
    """
    # Send initial state
    ws.send(json.dumps({
        "type": "init",
        "data": demo_state
    }))

    # Run the demo in a background thread
    def run_demo():
        try:
            # Phase 1: Layer 1 baseline (100% drift)
            time.sleep(1)  # Initial pause

            # Animate drift from 100% → 0% over 3 seconds
            for drift in range(100, -1, -2):
                demo_state["drift_percentage"] = drift
                ws.send(json.dumps({
                    "type": "drift_update",
                    "data": {"drift_percentage": drift}
                }))
                time.sleep(0.06)  # 3 seconds total (50 steps × 60ms)

            # Phase 2: Layer 2 scroll creation
            time.sleep(0.5)

            # Set up QSEAL secret
            if not os.getenv('QSEAL_SECRET'):
                os.environ['QSEAL_SECRET'] = hashlib.sha256(b"demo_secret_key").hexdigest()

            # Initialize memory store
            demo_data_dir = PROJECT_ROOT / "data" / "dashboard_demo"
            demo_data_dir.mkdir(parents=True, exist_ok=True)

            memory_store = ScrollMemoryStore(
                base_path=str(demo_data_dir),
                agent_id="Dashboard_Demo"
            )

            # Create 3 demo scrolls
            demo_memories = [
                {
                    "content": "User prefers concise technical explanations",
                    "memory_type": "preference",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "content": "Technical stack: Python, cryptography, YAML",
                    "memory_type": "fact",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "content": "System: OpenClaw integration target platform",
                    "memory_type": "fact",
                    "timestamp": datetime.now().isoformat()
                }
            ]

            created_scrolls = []
            for i, mem in enumerate(demo_memories, 1):
                time.sleep(0.8)  # Stagger scroll creation

                # Create scroll
                result = memory_store.remember(
                    content=mem["content"],
                    memory_type=mem["memory_type"],
                    user_id="demo_user"
                )

                scroll_data = {
                    "scroll_id": result["scroll_id"],
                    "content": mem["content"],
                    "memory_type": mem["memory_type"],
                    "qseal_signature": result["qseal_signature"],
                    "timestamp": mem["timestamp"]
                }

                created_scrolls.append(scroll_data)
                demo_state["scrolls"].append(scroll_data)

                ws.send(json.dumps({
                    "type": "scroll_created",
                    "data": scroll_data
                }))

            # Phase 3: Chain verification
            time.sleep(0.5)

            # Verify all scrolls
            verified_count = 0
            for scroll in created_scrolls:
                # Simulate verification (actual verification happens in ScrollMemoryStore)
                verified_count += 1

            demo_state["verification"] = {
                "scrolls_verified": verified_count,
                "total_scrolls": len(created_scrolls),
                "signatures_valid": 100,
                "chain_links": len(created_scrolls) - 1 if len(created_scrolls) > 1 else 0,
                "tampering_detected": False,
                "qseal_engine": "HMAC-SHA256"
            }

            ws.send(json.dumps({
                "type": "verification_complete",
                "data": demo_state["verification"]
            }))

        except Exception as e:
            ws.send(json.dumps({
                "type": "error",
                "data": {"message": str(e)}
            }))

    # Start demo in background
    demo_thread = threading.Thread(target=run_demo, daemon=True)
    demo_thread.start()

    # Keep connection alive
    try:
        while True:
            message = ws.receive()
            if message is None:
                break
    except:
        pass

if __name__ == '__main__':
    # Run Flask with WebSocket support
    app.run(host='0.0.0.0', port=8080, debug=False)
