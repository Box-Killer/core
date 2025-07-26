import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { createSession } from "./session.ts";
import { createDesc, continueDesc } from "./descriptions.ts";

// Create an MCP server
const server = new McpServer({
  name: "ask-ui-server",
  version: "1.0.0",
});

const sessions = new Map<string, Awaited<ReturnType<typeof createSession>>>();

server.registerTool(
  "ask-ui",
  {
    title: "Ask UI",
    description: createDesc,
    inputSchema: {
      html: z.string(),
      title: z.string().default("Ask UI"),
      width: z.number().default(1024),
      height: z.number().default(768),
    },
  },
  async ({ html, title, width, height }, extra) => {
    const sessionId = extra.sessionId ?? "";
    const oldSession = sessions.get(sessionId);
    if (oldSession && !oldSession.isFinished()) {
      throw new Error("Last session is not finished");
    }
    const session = await createSession(html, {
      title: title,
      width: width,
      height: height,
    });
    sessions.set(sessionId, session);

    // await new Promise((resolve) => setTimeout(resolve, 10000));
    await session.promise;

    return {
      content: [{ type: "text", text: session.getResult() }],
    };
  }
);

server.registerTool(
  "continue-ask-ui",
  {
    title: "Continue Ask UI",
    description: continueDesc,
    inputSchema: {},
  },
  async ({}, extra) => {
    const sessionId = extra.sessionId ?? "";
    const session = sessions.get(sessionId);
    if (!session) {
      throw new Error("Session not found");
    }
    return {
      content: [{ type: "text", text: session.getResult() }],
    };
  }
);

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
