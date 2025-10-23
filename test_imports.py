import sys

print("Testing imports...", file=sys.stderr)

try:
    from typing import Any
    # Test that Any is available
    _ = Any
    print("✓ typing", file=sys.stderr)
except Exception as e:
    print(f"✗ typing: {e}", file=sys.stderr)

try:
    import httpx
    # Test that httpx is available
    _ = httpx.__version__
    print("✓ httpx", file=sys.stderr)
except Exception as e:
    print(f"✗ httpx: {e}", file=sys.stderr)

try:
    from mcp.server.fastmcp import FastMCP
    # Test that FastMCP is available
    _ = FastMCP
    print("✓ mcp.server.fastmcp", file=sys.stderr)
except Exception as e:
    print(f"✗ mcp.server.fastmcp: {e}", file=sys.stderr)

print("All imports checked", file=sys.stderr)
