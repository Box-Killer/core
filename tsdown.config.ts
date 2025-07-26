import { defineConfig } from "tsdown";

export default defineConfig({
  entry: {
    "mcp-ask-ui": "src/server.ts",
  },
  outDir: "dist",
  format: "esm",
  target: "es2020",
  minify: true,
  banner: {
    js: "#!/usr/bin/env node",
  },
});
