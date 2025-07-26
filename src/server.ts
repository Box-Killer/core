import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { createSession } from "./session.ts";
import { createDesc, continueDesc, hasAPI } from "./prompt.ts";
import { callLLM } from "./llm.ts";

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
      [hasAPI ? "prompt" : "html"]: z.string(),
      title: z.string().default("Ask UI"),
      // width: z.number().default(1024),
      height: z.number(),
    },
  },
  async (
    {
      html,
      prompt,
      title,
      // width,
      height,
    },
    extra
  ) => {
    const sessionId = extra.sessionId ?? "";
    const oldSession = sessions.get(sessionId);
    if (oldSession && !oldSession.isFinished()) {
      throw new Error("Last session is not finished");
    }
    if (html && prompt) {
      throw new Error("html and prompt cannot be set at the same time");
    }
    if (!html && !prompt) {
      throw new Error("html or prompt must be set");
    }
    const session = await createSession(
      (html ?? (await callLLM(prompt as string, height as number))) as string,
      {
        title: title,
        width: 720,
        height: (height as number) * 1.5,
      }
    );
    sessions.set(sessionId, session);

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
