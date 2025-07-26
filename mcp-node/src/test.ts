import * as readline from 'readline';

// 定义请求体和响应的类型接口
interface Message {
  sender_type: 'USER' | 'BOT';
  sender_name: string;
  text: string;
}

interface BotSetting {
  bot_name: string;
  content: string;
}

interface ReplyConstraints {
  sender_type: 'BOT';
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
}

/**
 * 启动一个与 MiniMax 模型的交互式聊天会话。
 * 从环境变量中获取 Group ID 和 API Key。
 * 使用原生的 fetch API 进行 HTTP 请求。
 */
async function startMinimaxChat() {
  // 从环境变量获取 Group ID 和 API Key
  const groupId: string = process.env.MINIMAX_GROUP_ID || '';
  const apiKey: string = process.env.MINIMAX_API_KEY || '';

  // 检查是否设置了环境变量
  if (!groupId || !apiKey) {
    console.error('错误：请设置 MINIMAX_GROUP_ID 和 MINIMAX_API_KEY 环境变量。');
    process.exit(1);
  }

  const url: string = `https://api.minimaxi.com/v1/text/chatcompletion_pro?GroupId=${groupId}`;

  const headers: HeadersInit = { // 使用 HeadersInit 类型
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  };

  const requestBody: RequestBody = {
    model: 'MiniMax-Text-01',
    tokens_to_generate: 8192,
    reply_constraints: { sender_type: 'BOT', sender_name: 'MM智能助理' },
    messages: [],
    bot_setting: [
      {
        bot_name: 'MM智能助理',
        content: 'MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。',
      },
    ],
  };

  // 创建 readline 接口用于获取用户输入
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('开始与 MM 智能助理聊天 (输入 Ctrl+C 退出)。');

  // 定义一个内部异步函数来处理每一轮的聊天交互
  const chatLoop = async () => {
    while (true) {
      const line: string = await new Promise((resolve) => {
        rl.question('发言: ', (input) => {
          resolve(input);
        });
      });

      // 将当次输入内容作为用户的一轮对话添加到 messages
      requestBody.messages.push({ sender_type: 'USER', sender_name: '小明', text: line });

      try {
        // 使用 fetch API 发送 POST 请求
        const response = await fetch(url, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(requestBody) // fetch 的 body 需要是字符串化后的 JSON
        });

        // 检查响应是否成功
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP 错误！状态码: ${response.status}, 详情: ${errorText}`);
        }

        const data: ResponseData = await response.json(); // 解析 JSON 响应
        const reply = data.reply;
        console.log(`reply: ${reply}`);

        // 将当次的 AI 回复内容加入 messages
        requestBody.messages.push(...data.choices[0].messages);
      } catch (error) {
        console.error('请求失败:', (error as Error).message); // 类型断言为 Error
        // 遇到错误时，可以选择退出循环或继续
      }
    }
  };

  // 启动聊天循环
  chatLoop();

  // 监听程序退出信号，确保 readline 接口被关闭
  process.on('SIGINT', () => {
    console.log('聊天结束。');
    rl.close();
    process.exit();
  });
}

// 调用异步函数启动聊天会话
startMinimaxChat();