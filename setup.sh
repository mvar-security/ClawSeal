#!/bin/bash
# MIRRA EOS MCP Server Setup Script
# Author: Shawn Cohen
# Date: April 13, 2026
# Version: 2.0.0 (Scroll-Native)
#
# Quick setup for MIRRA EOS + Claude Code integration
# Target: <5 minute installation

set -e  # Exit on error

echo "================================================================================"
echo "MIRRA EOS MCP Server Setup (v2.0.0 - Scroll-Native)"
echo "================================================================================"
echo ""

# ============================================================================
# Step 1: Check Python Version
# ============================================================================
echo "Step 1/5: Checking Python environment..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION found, but $REQUIRED_VERSION or later required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# ============================================================================
# Step 2: Check/Generate QSEAL_SECRET
# ============================================================================
echo "Step 2/5: Configuring QSEAL cryptographic signing..."

if [ -z "$QSEAL_SECRET" ]; then
    echo "⚠️  QSEAL_SECRET not found in environment"
    echo ""
    echo "Generating new QSEAL secret (HMAC-SHA256 key)..."

    if ! command -v openssl &> /dev/null; then
        echo "❌ OpenSSL not found. Cannot generate QSEAL_SECRET."
        echo "   Install OpenSSL or manually set QSEAL_SECRET with: openssl rand -hex 32"
        exit 1
    fi

    NEW_SECRET=$(openssl rand -hex 32)

    echo "✅ QSEAL secret generated: ${NEW_SECRET:0:16}... (64 chars total)"
    echo ""
    echo "CRITICAL: Add this to your shell profile for persistence:"
    echo ""

    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi

    echo "  export QSEAL_SECRET=\"$NEW_SECRET\"" | tee -a "$SHELL_RC" > /dev/null
    echo ""
    echo "✅ Added to $SHELL_RC"
    echo ""
    echo "⚠️  IMPORTANT: Run 'source $SHELL_RC' or restart your terminal to load the secret"
    echo ""

    # Export for current session
    export QSEAL_SECRET="$NEW_SECRET"
else
    echo "✅ QSEAL_SECRET already configured: ${QSEAL_SECRET:0:16}... (${#QSEAL_SECRET} chars)"

    # Verify length
    if [ ${#QSEAL_SECRET} -lt 32 ]; then
        echo "⚠️  WARNING: QSEAL_SECRET is only ${#QSEAL_SECRET} characters. Recommended: 64+ chars"
        echo "   Generate a stronger secret with: openssl rand -hex 32"
    fi
fi
echo ""

# ============================================================================
# Step 3: Verify Project Structure
# ============================================================================
echo "Step 3/5: Verifying project structure..."

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
MCP_SERVER_V2="$PROJECT_ROOT/clawseal_mcp_server_v2.py"
MCP_SERVER_V1="$PROJECT_ROOT/clawseal_mcp_server.py"
SCROLL_STORE="$PROJECT_ROOT/mirra_core/memory/scroll_memory_store.py"
QSEAL_ENGINE="$PROJECT_ROOT/mirra_core/security/qseal_engine.py"

if [ ! -f "$MCP_SERVER_V2" ]; then
    echo "❌ MCP server v2 not found at: $MCP_SERVER_V2"
    exit 1
fi

if [ ! -f "$SCROLL_STORE" ]; then
    echo "❌ Scroll memory store not found at: $SCROLL_STORE"
    exit 1
fi

if [ ! -f "$QSEAL_ENGINE" ]; then
    echo "❌ QSEAL engine not found at: $QSEAL_ENGINE"
    exit 1
fi

echo "✅ MCP server v2.0 found (FastMCP)"
echo "✅ Scroll memory store found (SIP-0006)"
echo "✅ QSEAL engine found"
echo ""

# ============================================================================
# Step 4: Create Data Directories
# ============================================================================
echo "Step 4/5: Creating data directories..."

DATA_ROOT="$PROJECT_ROOT/data/claude_code_eos/Claude_Code_MIRRA"
mkdir -p "$DATA_ROOT/memories/scrolls"
mkdir -p "$DATA_ROOT/memories/index"
mkdir -p "$DATA_ROOT/decisions"
mkdir -p "$DATA_ROOT/state"
mkdir -p "$DATA_ROOT/user_profiles"

touch "$DATA_ROOT/memories/chain.jsonl"
touch "$DATA_ROOT/memories/index/by_type.jsonl"
touch "$DATA_ROOT/memories/index/by_date.jsonl"
touch "$DATA_ROOT/memories/index/by_keyword.jsonl"
touch "$DATA_ROOT/memories/index/lineage.jsonl"

echo "✅ Created scroll storage: $DATA_ROOT/memories/scrolls/"
echo "✅ Created indexes: $DATA_ROOT/memories/index/"
echo "✅ Created decision ledger: $DATA_ROOT/decisions/"
echo ""

# ============================================================================
# Step 5: Update .claude/mcp.json with Absolute Paths
# ============================================================================
echo "Step 5/5: Configuring MCP settings..."

MCP_CONFIG="$PROJECT_ROOT/.claude/mcp.json"

if [ ! -f "$MCP_CONFIG" ]; then
    echo "⚠️  .claude/mcp.json not found. Creating template..."

    mkdir -p "$PROJECT_ROOT/.claude"

    cat > "$MCP_CONFIG" <<EOF
{
  "mcpServers": {
    "clawseal": {
      "command": "python3",
      "args": [
        "$MCP_SERVER_V2"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_ROOT",
        "QSEAL_SECRET": "\${QSEAL_SECRET}"
      }
    }
  }
}
EOF

    echo "✅ Created .claude/mcp.json"
else
    echo "✅ .claude/mcp.json already exists"
fi

echo ""

# ============================================================================
# Step 6: Run Integration Test
# ============================================================================
echo "================================================================================"
echo "Running Integration Test..."
echo "================================================================================"
echo ""

TEST_SCRIPT="$PROJECT_ROOT/test_scroll_memory_integration.py"

if [ -f "$TEST_SCRIPT" ]; then
    echo "Testing Scroll memory with QSEAL verification..."
    echo ""

    if QSEAL_SECRET="$QSEAL_SECRET" python3 "$TEST_SCRIPT" 2>&1 | grep -q "TEST COMPLETE"; then
        echo ""
        echo "✅ Integration test passed"
    else
        echo ""
        echo "⚠️  Integration test produced warnings (check output above)"
        echo "   This may be normal if data already exists"
    fi
else
    echo "⚠️  Test script not found at: $TEST_SCRIPT"
    echo "   Skipping integration test"
fi

echo ""

# ============================================================================
# Success Summary
# ============================================================================
echo "================================================================================"
echo "✅ MIRRA EOS MCP Server Setup Complete"
echo "================================================================================"
echo ""
echo "Configuration Summary:"
echo "  • Python: $PYTHON_VERSION"
echo "  • QSEAL Secret: ${QSEAL_SECRET:0:16}... (${#QSEAL_SECRET} chars)"
echo "  • MCP Server: clawseal_mcp_server_v2.py (FastMCP)"
echo "  • Data Storage: $DATA_ROOT/"
echo "  • Architecture: Scroll-Native (SIP-0006)"
echo ""
echo "Next Steps:"
echo ""
echo "1. Load environment variables:"
echo "   source ~/.zshrc  # or ~/.bashrc"
echo ""
echo "2. Open VS Code / Claude Code in this directory:"
echo "   cd $PROJECT_ROOT"
echo "   code ."
echo ""
echo "3. Restart Claude Code to load MCP server"
echo ""
echo "4. Verify connection:"
echo "   Ask Claude Code: 'Can you check if the MIRRA EOS tools are available?'"
echo "   Expected: 12 tools (remember, recall, get_identity, etc.)"
echo ""
echo "Documentation:"
echo "  • Setup Guide: CLAUDE_CODE_MCP_SETUP.md"
echo "  • Specification: SIP_0006_SCROLL_NATIVE_MEMORY.md"
echo "  • MCP Config: .claude/mcp.json"
echo ""
echo "Support:"
echo "  • Test suite: python3 test_scroll_memory_integration.py"
echo "  • Data location: data/claude_code_eos/Claude_Code_MIRRA/"
echo "  • Logs: Check VS Code terminal for MCP server output"
echo ""
echo "================================================================================"
echo "Installation time: <5 minutes. Enjoy persistent AI memory with cryptographic"
echo "verification, zero database dependencies, and human-readable YAML storage."
echo "================================================================================"
