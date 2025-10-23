# PyWeatherMCP

A Model Context Protocol (MCP) server that provides weather information using the National Weather Service API. This server offers weather alerts, forecasts, and location management features for MCP-compatible clients.

## Features

- 🌦️ **Weather Alerts**: Get active weather alerts for any US state
- 📍 **Weather Forecasts**: Get 5-day weather forecasts for any US location
- ⭐ **Favorite Locations**: Save and manage your favorite weather locations
- 📊 **Search History**: Track your weather queries
- 🔄 **Memory Persistence**: Automatically saves your preferences and history

## Prerequisites

- Python 3.14 or higher
- Internet connection (for API calls to National Weather Service)

## Installation

### Using uv (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pyweathermcp.git
   cd pyweathermcp
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

### Using pip

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pyweathermcp.git
   cd pyweathermcp
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Running the MCP Server

To run the weather MCP server:

```bash
python weather.py
```

The server will start and listen for MCP protocol messages via stdio.

### Available Tools

#### 1. Get Weather Alerts

Get active weather alerts for a US state.

**Parameters:**

- `state` (string): Two-letter US state code (e.g., "CA", "NY", "TX")

**Example:**

```python
get_alerts("CA")
```

#### 2. Get Weather Forecast

Get a 5-day weather forecast for a specific location.

**Parameters:**

- `latitude` (float): Latitude coordinate
- `longitude` (float): Longitude coordinate
- `location_name` (string, optional): Human-readable name for the location

**Example:**

```python
get_forecast(37.7749, -122.4194, "San Francisco, CA")
```

#### 3. Save Favorite Location

Save a location to your favorites for quick access.

**Parameters:**

- `name` (string): Name of the location
- `latitude` (float): Latitude coordinate
- `longitude` (float): Longitude coordinate

**Example:**

```python
save_favorite("Home", 40.7128, -74.0060)
```

#### 4. Get Favorite Locations

Retrieve all saved favorite locations.

**Example:**

```python
get_favorites()
```

#### 5. Get Search History

View your recent weather searches.

**Parameters:**

- `limit` (int, optional): Number of recent searches to show (default: 10)

**Example:**

```python
get_history(5)
```

#### 6. Clear Search History

Clear all search history while keeping favorites.

**Example:**

```python
clear_history()
```

### Available Resources

#### Server Information

Get information about the weather server and its capabilities.

**Resource URI:** `weather://info`

#### Usage Statistics

Get usage statistics including search count and favorite locations.

**Resource URI:** `weather://stats`

### Available Prompts

#### Quick Weather Check

A template prompt for quick weather checks using your favorite locations.

**Prompt:** `quick_weather_prompt`

## Data Storage

The server automatically creates and maintains a `weather_memory.json` file to store:

- Search history
- Favorite locations
- Usage statistics

This file is created automatically on first use and is excluded from version control.

## API Information

This server uses the **National Weather Service API** (https://api.weather.gov), which:

- Provides free weather data for the United States
- Requires no API key or authentication
- Has rate limits (please be respectful)
- Covers all US states and territories

## Error Handling

The server includes robust error handling:

- Network timeouts (30 seconds)
- Invalid coordinates or state codes
- API service unavailability
- Graceful fallbacks for missing data

## Development

### Project Structure

```
pyweathermcp/
├── weather.py          # Main MCP server implementation
├── main.py            # Simple entry point
├── test_imports.py    # Import testing utility
├── pyproject.toml     # Project configuration and dependencies
├── weather_memory.json # User data storage (auto-generated)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Dependencies

- `httpx>=0.28.1`: Modern HTTP client for API requests
- `mcp>=1.18.0`: Model Context Protocol server framework

### Testing Imports

To verify all dependencies are properly installed:

```bash
python test_imports.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/pyweathermcp/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Changelog

### v0.1.0

- Initial release
- Weather alerts and forecasts
- Favorite locations management
- Search history tracking
- Memory persistence

---

**Note:** This server is designed to work with MCP-compatible clients. Make sure your client supports the MCP protocol for the best experience.
