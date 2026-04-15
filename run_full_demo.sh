#!/bin/bash
# ClawSeal Three-Layer Demo Runner
# Executes all three demo layers in sequence
#
# Usage: ./run_full_demo.sh

set -e  # Exit on error

echo "================================================================================"
echo "CLAWSEAL THREE-LAYER DEMONSTRATION"
echo "================================================================================"
echo ""
echo "This demo proves three claims:"
echo "  1. AI agents without ClawSeal drift 100% (complete amnesia)"
echo "  2. ClawSeal maintains 0% drift (perfect continuity)"
echo "  3. QSEAL signatures provide cryptographic proof"
echo ""
echo "Total duration: ~8-10 minutes"
echo ""
echo "Press ENTER to begin..."
read

# Clean any previous demo data
echo "Cleaning previous demo data..."
rm -rf data/demo_with_clawseal
echo ""

# Set QSEAL secret for consistent signatures
export QSEAL_SECRET="test_secret_key_for_demo"

# ============================================================================
# LAYER 1: Identity Drift Without ClawSeal
# ============================================================================
echo "================================================================================"
echo "LAYER 1: IDENTITY DRIFT (WITHOUT CLAWSEAL)"
echo "================================================================================"
echo ""
python3 demo_layer1_baseline.py
echo ""
echo "Press ENTER to continue to Layer 2..."
read
echo ""

# ============================================================================
# LAYER 2: Identity Continuity With ClawSeal
# ============================================================================
echo "================================================================================"
echo "LAYER 2: IDENTITY CONTINUITY (WITH CLAWSEAL)"
echo "================================================================================"
echo ""
python3 demo_layer2_with_clawseal.py
echo ""
echo "Press ENTER to continue to Layer 3..."
read
echo ""

# ============================================================================
# LAYER 3: QSEAL Cryptographic Verification
# ============================================================================
echo "================================================================================"
echo "LAYER 3: CRYPTOGRAPHIC VERIFICATION (QSEAL)"
echo "================================================================================"
echo ""
python3 demo_layer3_verification.py
echo ""

# ============================================================================
# Final Summary
# ============================================================================
echo "================================================================================"
echo "DEMONSTRATION COMPLETE"
echo "================================================================================"
echo ""
echo "What We Proved:"
echo ""
echo "  Layer 1: Baseline AI agents have 100% identity drift"
echo "           ❌ No memory between sessions"
echo "           ❌ Complete amnesia"
echo ""
echo "  Layer 2: ClawSeal maintains 0% identity drift"
echo "           ✅ Perfect memory persistence"
echo "           ✅ Scroll-native YAML storage"
echo "           ✅ Human-readable, Git-friendly"
echo ""
echo "  Layer 3: QSEAL signatures provide cryptographic proof"
echo "           ✅ HMAC-SHA256 tamper-evident sealing"
echo "           ✅ Merkle-like signature chains"
echo "           ✅ Verifiable, auditable, undeniable"
echo ""
echo "Architecture:"
echo "  • Zero ChromaDB dependency"
echo "  • Zero vector database"
echo "  • Pure YAML + text search + QSEAL signatures"
echo "  • <5 minute installation (./setup.sh)"
echo ""
echo "Specification:"
echo "  • SIP-0006: Scroll-Native Memory Architecture"
echo "  • Author: Shawn Cohen"
echo "  • Date: April 13, 2026"
echo "  • Status: Production"
echo ""
echo "================================================================================"
echo "This isn't theory. This is running code. Dated today."
echo "================================================================================"
echo ""
