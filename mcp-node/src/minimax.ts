// 定义请求体和响应的类型接口
interface Message {
  sender_type: "USER" | "BOT" | "SYSTEM"; // 增加 SYSTEM 类型
  sender_name: string;
  text: string;
}

interface BotSetting {
  bot_name: string;
  content: string;
}

interface ReplyConstraints {
  sender_type: "BOT";
  sender_name: string;
}

interface RequestBody {
  model: string;
  tokens_to_generate: number;
  reply_constraints: ReplyConstraints;
  messages: Message[];
  bot_setting: BotSetting[];
}

interface Choice {
  messages: Message[];
}

interface ResponseData {
  reply: string;
  choices: Choice[];
  // 还可以根据实际API响应添加其他字段，例如 base_resp, usage 等
}

/**
 * 从 MiniMax 模型获取单次聊天回复。
 *
 * @param apiKey MiniMax API Key。
 * @param groupId 您的 MiniMax Group ID。
 * @param systemPrompt 模型的系统提示（Bot Setting Content）。
 * @param userPrompt 用户的当前输入。
 * @returns 模型的回复字符串。
 * @throws Error 如果 API 请求失败或返回错误。
 */
export async function getMinimaxChatReply(
  apiKey: string,
  groupId: string,
  systemPrompt: string,
  userPrompt: string
): Promise<string> {
  if (!apiKey || !groupId || !userPrompt) {
    throw new Error("API Key, Group ID 和 User Prompt 不能为空。");
  }

  const url: string = `https://api.minimaxi.com/v1/text/chatcompletion_pro?GroupId=${groupId}`;

  const headers: HeadersInit = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  };

  const requestBody: RequestBody = {
    model: "MiniMax-Text-01",
    tokens_to_generate: 81920,
    reply_constraints: { sender_type: "BOT", sender_name: "HTML生成器" },
    messages: [
      // 这里的 messages 只包含本次对话的相关信息
      { sender_type: "USER", sender_name: "要求者", text: userPrompt },
    ],
    bot_setting: [
      {
        bot_name: "HTML生成器",
        content: systemPrompt,
      },
    ],
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json(); // 尝试解析错误详情
      throw new Error(
        `API 请求失败！状态码: ${response.status}, 详情: ${JSON.stringify(
          errorData
        )}`
      );
    }

    const data: ResponseData = await response.json();
    if (!data.reply) {
      // 有些API在成功响应时也可能没有'reply'字段，需要根据实际情况调整
      throw new Error("API 响应中未找到 'reply' 字段。");
    }
    return data.reply;
  } catch (error) {
    console.error("获取 MiniMax 聊天回复时发生错误:", error);
    throw error; // 重新抛出错误以便调用者处理
  }
}
