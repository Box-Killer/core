export const scheme = {
  // ...
};

export async function perform(
  prompt: string,
  options: {
    sendMessage: (data: any) => Promise<any>;
  }
) {
  // Call our LLM
  const response = await options.sendMessage(f1(prompt));
  return f2(response);
}

export async function createMcpServer() {
  const { McpServer, ResourceTemplate } = await import(
    "@modelcontextprotocol/sdk/server/mcp.js"
  );
  const { StdioServerTransport } = await import(
    "@modelcontextprotocol/sdk/server/stdio.js"
  );
  const { z } = await import("zod");

  // Create an MCP server
  const server = new McpServer({
    name: "demo-server",
    version: "1.0.0",
  });

  // Add an addition tool
  server.registerTool("add", scheme, perform);

  // Add a dynamic greeting resource
  server.registerResource(
    "greeting",
    new ResourceTemplate("greeting://{name}", { list: undefined }),
    {
      title: "Greeting Resource", // Display name for UI
      description: "Dynamic greeting generator",
    },
    async (uri, { name }) => ({
      contents: [
        {
          uri: uri.href,
          text: `Hello, ${name}!`,
        },
      ],
    })
  );

  // Start receiving messages on stdin and sending messages on stdout
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
