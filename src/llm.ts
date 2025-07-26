import OpenAI from "openai";
import { apiKey, baseURL, model, uiInstruction } from "./prompt.ts";

let client: OpenAI | null = null;

export async function callLLM(prompt: string, height: number) {
  const systemPrompt = `你是一个专业的 Web 构建者，你需要根据要求，编写 HTML，以获取用户输入。你只需要返回 HTML 字符串，不需要任何其他内容，不需要用代码块包裹。

${uiInstruction(`为 ${height}px`)}`;

  client ??= new OpenAI({
    apiKey: apiKey,
    baseURL: baseURL!,
  });

  const completion = await client.chat.completions.create({
    model: model!,
    messages: [
      {
        role: "system",
        content: systemPrompt,
      },
      { role: "user", content: prompt },
    ],
    temperature: 0.6,
  });

  return completion.choices[0].message.content;
}
