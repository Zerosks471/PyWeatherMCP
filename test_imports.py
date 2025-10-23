import sys
cat > test_imports.py << 'EOF'
print("Testing imports...", file=sys.stderr)

try:
    from typing import Any
    print("✓ typing", file=sys.stderr)
except Exception as e:
    print(f"✗ typing: {e}", file=sys.stderr)

try:
    import httpx
    print("✓ httpx", file=sys.stderr)
except Exception as e:
    print(f"✗ httpx: {e}", file=sys.stderr)

try:
    from mcp.server.fastmcp import FastMCP
    print("✓ mcp.server.fastmcp", file=sys.stderr)
except Exception as e:
    print(f"✗ mcp.server.fastmcp: {e}", file=sys.stderr)

print("All imports checked", file=sys.stderr)
EOF
