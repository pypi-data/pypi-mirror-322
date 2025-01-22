# chinese-holidays MCP server

Query information about Chinese holidays

### Tools

1. `get-all-holidays`: Get all holidays for a year
2. `is-holiday`: Check if a date is a holiday

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "chinese-holidays": {
      "command": "uv",
      "args": [
        "--directory",
        "the absolute path of chinese-holidays",
        "run",
        "chinese-holidays"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "chinese-holidays": {
      "command": "uvx",
      "args": [
        "chinese-holidays"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
  ```
</details>