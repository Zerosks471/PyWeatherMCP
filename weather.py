from typing import Any
import httpx
import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
MEMORY_FILE = "weather_memory.json"

# Helper function for API requests


async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# Memory functions


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"searches": [], "favorites": []}


def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Resource: Server info


@mcp.resource("weather://info")
def get_server_info() -> str:
    """Information about this weather server"""
    return """
Weather MCP Server v1.0
=======================
Data Source: National Weather Service API
Coverage: United States only
Last Updated: October 2025

Available Tools:
- get_alerts: Weather alerts by state
- get_forecast: 5-day forecast by coordinates
- save_favorite: Save favorite locations
- get_favorites: View saved locations
- get_history: View search history

This server remembers your favorite locations and search history.
"""

# Resource: Usage statistics


@mcp.resource("weather://stats")
def get_stats() -> str:
    """Get usage statistics"""
    memory = load_memory()
    return f"""
Usage Statistics
================
Total searches: {len(memory['searches'])}
Favorite locations: {len(memory['favorites'])}
"""

# Tool 1: Get weather alerts


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    # Save to history
    memory = load_memory()
    memory['searches'].append({
        "type": "alerts",
        "state": state,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(memory)

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts"

    if not data["features"]:
        return f"No active alerts for {state}"

    alerts = []
    for feature in data["features"]:
        props = feature["properties"]
        alert = f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description')}
"""
        alerts.append(alert)

    return f"[Weather MCP Server] Alerts for {state}\n" + "\n---\n".join(alerts)

# Tool 2: Get weather forecast


@mcp.tool()
async def get_forecast(latitude: float, longitude: float, location_name: str = "Unknown") -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        location_name: Name of the location (optional)
    """
    # Save to history
    memory = load_memory()
    memory['searches'].append({
        "type": "forecast",
        "location": location_name,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(memory)

    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data"

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast"

    periods = forecast_data["properties"]["periods"][:5]
    forecast = []

    for period in periods:
        forecast.append(f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
""")

    return f"[Weather MCP Server] Forecast for {location_name}\n" + "\n".join(forecast)

# Tool 3: Save favorite location


@mcp.tool()
def save_favorite(name: str, latitude: float, longitude: float) -> str:
    """Save a favorite location for quick access.

    Args:
        name: Name of the location
        latitude: Latitude
        longitude: Longitude
    """
    memory = load_memory()

    # Check if already exists
    for fav in memory['favorites']:
        if fav['name'] == name:
            return f"Location '{name}' already saved as favorite"

    memory['favorites'].append({
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "added": datetime.now().isoformat()
    })
    save_memory(memory)

    return f"[Weather MCP Server] Saved '{name}' to favorites"

# Tool 4: Get favorites


@mcp.tool()
def get_favorites() -> str:
    """Get all saved favorite locations"""
    memory = load_memory()

    if not memory['favorites']:
        return "[Weather MCP Server] No favorite locations saved yet"

    favorites = ["[Weather MCP Server] Your Favorite Locations:\n"]
    for fav in memory['favorites']:
        favorites.append(
            f"• {fav['name']} ({fav['latitude']}, {fav['longitude']})")

    return "\n".join(favorites)

# Tool 5: Get history


@mcp.tool()
def get_history(limit: int = 10) -> str:
    """Get recent search history.

    Args:
        limit: Number of recent searches to show (default 10)
    """
    memory = load_memory()

    if not memory['searches']:
        return "[Weather MCP Server] No search history yet"

    recent = memory['searches'][-limit:]
    history = ["[Weather MCP Server] Recent Searches:\n"]

    for search in reversed(recent):
        timestamp = datetime.fromisoformat(
            search['timestamp']).strftime("%Y-%m-%d %H:%M")
        if search['type'] == 'alerts':
            history.append(f"• {timestamp}: Alerts for {search['state']}")
        else:
            history.append(
                f"• {timestamp}: Forecast for {search.get('location', 'Unknown')}")

    return "\n".join(history)

# Tool 6: Clear memory


@mcp.tool()
def clear_history() -> str:
    """Clear all search history (keeps favorites)"""
    memory = load_memory()
    memory['searches'] = []
    save_memory(memory)
    return "[Weather MCP Server] Search history cleared"

# Prompt: Quick weather check


@mcp.prompt()
def quick_weather_prompt() -> str:
    """Template for quick weather checks"""
    return """I'd like to check the weather. Here are my favorite locations:
{favorites}

Which location would you like to check?"""


# Run the server
if __name__ == "__main__":
    mcp.run(transport='stdio')
