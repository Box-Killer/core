# mcp-ask-ui

A [MCP](https://modelcontextprotocol.io/) server that enables agents to ask users questions via custom user interfaces.

## Server Config

```json
{
  "mcpServers": {
    "ask-ui": {
      "command": "npx",
      "args": ["-y", "mcp-ask-ui"],
      "env": {
        "MOONSHOT_API_KEY": "all keys are optional",
        "PPIO_API_KEY": "all keys are optional",
        "MINIMAX_API_KEY": "all keys are optional"
      }
    }
  }
}
```
