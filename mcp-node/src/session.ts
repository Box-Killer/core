import webview from "webview";
import { spawn } from "child_process";
import { createServer } from "http";
import { getRandomPort } from "get-port-please";

export async function createSession(html: string, options: any) {
  const port = await getRandomPort();
  let resolve: (value: any) => void;
  const promise = new Promise((_resolve) => {
    resolve = _resolve;
  });
  const server = createServer(async (req, res) => {
    if (req.method === "POST") {
      const body = [];
      for await (const chunk of req) {
        body.push(chunk);
      }
      const bodyString = Buffer.concat(body).toString();

      session.result = JSON.parse(bodyString);
      session.child.kill();

      res.writeHead(200, { "Content-Type": "text/plain" });
      res.end("OK");
      resolve(true);
    } else {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(
        html +
          `<script>
window.$submit = async function(data) {
  const response = await fetch("/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
</script>`
      );
    }
  });
  const child = spawn(
    webview.binaryPath,
    webview.optionsToArgv({
      ...options,
      url: `http://localhost:${port}`,
    })
  );
  server.listen(port);
  const session = {
    child,
    port,
    result: null,
    getResult: () => {
      if (session.result) {
        return JSON.stringify(session.result);
      }
      if (child.exitCode === null) {
        return "User is still interacting with the UI.";
      }
      return "No result";
    },
    isFinished: () => {
      return session.result !== null || child.exitCode !== null;
    },
    promise,
  };
  return session;
}
