# mcp-ask-ui

A [MCP](https://modelcontextprotocol.io/) server giving agent the ability to create custom UI for user data input.

## Server Config

```json
{
  "mcpServers": {
    "ask-ui": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-ask-ui"
      ],
      "env": {
        "MOONSHOT_API_KEY": "",
        "PPIO_API_KEY": "",
        "MINIMAX_API_KEY": ""
      }
    }
  }
}
```
