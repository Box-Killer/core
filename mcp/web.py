import webview
from mcp.server.fastmcp import FastMCP, Context
import multiprocessing
import json
import os # 导入 os 模块，用于获取进程 ID

# 创建一个 MCP 服务器实例
mcp = FastMCP("Ask UI")

# 全局字典，用于存储活跃的会话实例
sessions: dict[str, 'Session'] = {}

class Session:
    """
    管理一个 WebView 窗口会话，并在单独的进程中运行它。
    """
    def __init__(self, client_id: str, **kwargs):
        self.client_id: str = client_id
        self.kwargs = kwargs
        # 创建一个队列，用于子进程向父进程传递结果
        self.result_queue = multiprocessing.Queue()
        # 创建并启动一个新进程来运行 WebView
        self.process = multiprocessing.Process(target=self._run_webview_process, args=(self.result_queue, self.kwargs))
        self.process.start()
        # 将当前会话实例存储到全局字典中
        sessions[client_id] = self
        print(f"主进程 {os.getpid()}: 启动了新的 WebView 进程 {self.process.pid}，客户端 ID: {self.client_id}")

    def _run_webview_process(self, result_queue, kwargs):
        """
        此方法在新进程中运行，负责创建和启动 WebView 窗口。
        """
        print(f"子进程 {os.getpid()}: WebView 进程已启动。")

        class JSAPI:
            """
            此内部类作为 WebView 的 JavaScript API，用于处理来自 JS 的调用。
            它在新进程中运行。
            """
            def __init__(self, queue_ref):
                self.queue_ref = queue_ref
                self.window_ref = None # 存储 WebView 窗口对象的引用

            def set_window(self, window_obj):
                """设置 WebView 窗口对象的引用"""
                self.window_ref = window_obj

            def close_window(self):
                """
                从 JavaScript 调用此方法以关闭 WebView 窗口并返回结果。
                """
                try:
                    if self.window_ref:
                        # 评估 JavaScript 以获取 window._result 的值
                        result = self.window_ref.evaluate_js("window._result;")
                        if result is not None:
                            # 将结果序列化为 JSON 字符串并放入队列
                            self.queue_ref.put(json.dumps(result))
                            print(f"子进程 {os.getpid()}: 结果已放入队列: {result}")
                        else:
                            # 如果没有结果，则放入 None
                            self.queue_ref.put(None)
                            print(f"子进程 {os.getpid()}: 未返回结果，放入 None。")
                    else:
                        # 如果窗口引用不存在，也放入 None
                        self.queue_ref.put(None)
                        print(f"子进程 {os.getpid()}: 窗口引用不存在，放入 None。")
                except Exception as e:
                    print(f"子进程 {os.getpid()}: 获取结果或放入队列时出错: {e}")
                    self.queue_ref.put(None) # 确保即使出错也能放入 None，以免阻塞父进程
                finally:
                    if self.window_ref:
                        # 销毁窗口，这将导致此子进程终止
                        self.window_ref.destroy()
                        print(f"子进程 {os.getpid()}: WebView 窗口已销毁。")

        # 在子进程中创建 JSAPI 实例，并传入结果队列
        js_api_instance = JSAPI(result_queue)

        # 在新进程中创建 WebView 窗口
        window = webview.create_window(
            kwargs.get("title", ""),
            html=kwargs.get("html"),
            js_api=js_api_instance, # 将 JSAPI 实例传递给 WebView
            width=kwargs.get("width", 600),
            height=kwargs.get("height", 500),
            resizable=kwargs.get("resizable", True),
            min_size=kwargs.get("min_size", (400, 300)),
            # debug=True, # 调试模式可能会影响多进程兼容性，此处暂时移除
        )
        # 将创建的窗口对象设置到 JSAPI 实例中，以便其可以操作窗口
        js_api_instance.set_window(window)
        
        # 启动 WebView，这将阻塞此子进程直到窗口关闭
        webview.start()
        print(f"子进程 {os.getpid()}: webview.start() 已完成。")

    def get_result(self) -> dict | str:
        """
        获取 WebView 窗口返回的结果。
        如果窗口仍在运行，则返回提示信息；否则，从队列中获取结果。
        """
        if self.process.is_alive():
            # 如果子进程仍在运行，说明窗口尚未关闭
            return "窗口正在运行中，请稍后再试"
        else:
            # 如果子进程已终止，尝试从队列中获取结果
            if not self.result_queue.empty():
                result_str = self.result_queue.get()
                if result_str is not None:
                    # 反序列化 JSON 字符串为字典
                    return json.loads(result_str)
                else:
                    return "窗口已关闭，但未返回结果"
            else:
                # 如果进程已终止但队列为空，表示窗口可能被用户手动关闭，或未设置结果
                return "窗口已关闭，但未返回结果"

    def terminate_session(self):
        """
        终止子进程并清理会话资源。
        在主进程中调用。
        """
        print(f"主进程 {os.getpid()}: 正在终止 WebView 进程 {self.process.pid}，客户端 ID: {self.client_id}")
        if self.process.is_alive():
            self.process.terminate() # 强制终止子进程
            self.process.join() # 等待子进程完全终止
        if self.client_id in sessions:
            del sessions[self.client_id] # 从全局字典中移除会话
        print(f"主进程 {os.getpid()}: WebView 进程 {self.process.pid} 已终止并清理。")


@mcp.tool()
def ask_ui(
    *,
    html: str,
    title: str = "用户信息输入",
    width: int = 600,
    height: int = 500,
    resizable: bool = True,
    min_size: tuple[int, int] = (400, 300),
    context: Context,
) -> dict | str:
    """
    弹出一个 WebView 窗口，并获取用户输入。参数为 HTML。

    要求：
    - 返回值可能为空，
    - HTML 里可以包含 JS 脚本，可以访问网络资源
    - JS 脚本中可以通过设置 window._result 来返回结果
    - 使用 pywebview.api.close_window() 来关闭窗口
    - 在需要的情况下，推荐使用非常丰富且直观的交互方式，可能包括曲线滑动条等等

    示例：
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css">
        <title>用户信息输入</title>
        <script>
            function submit() {
                window._result = {
                    user_name: document.getElementById('user_name').value,
                };
                pywebview.api.close_window();
            }
        </script>
    </head>
    <body>
        <div>
            <h1>用户信息输入</h1>
            <div>
                <label for="user_name">用户名</label>
                <input type="text" id="user_name" name="user_name" placeholder="请输入用户名">
                <button onclick="submit()">确定</button>
            </div>
        </body>
    </html>
    """
    print(f"主进程 {os.getpid()}: ask_ui 工具被调用，客户端 ID: {context.client_id}")

    if context.client_id in sessions:
        # 如果该客户端已存在会话，则先终止旧会话以清理资源
        print(f"主进程 {os.getpid()}: 发现现有会话，正在终止旧会话。")
        sessions[context.client_id].terminate_session()
        # terminate_session 内部会从 sessions 字典中删除会话

    # 创建一个新的会话实例，这将启动一个新的进程
    session = Session(
        context.client_id,
        title=title,
        html=html,
        width=width,
        height=height,
        resizable=resizable,
        min_size=min_size,
    )
    
    # 首次调用 get_result 通常会返回“窗口正在运行中...”
    # 用户需要再次调用 continue_ask_ui 来获取最终结果
    return session.get_result()

@mcp.tool()
def continue_ask_ui(context: Context) -> dict | str:
    """
    此工具可以继续尝试获取之前的 ask_ui 调用的结果。
    """
    print(f"主进程 {os.getpid()}: continue_ask_ui 工具被调用，客户端 ID: {context.client_id}")

    if context.client_id not in sessions:
        raise ValueError("窗口不存在。请重新调用 ask_ui 工具")

    session = sessions[context.client_id]
    result = session.get_result()

    # 如果子进程已不再活跃（即窗口已关闭），则清理会话资源
    if not session.process.is_alive():
        print(f"主进程 {os.getpid()}: 检测到 WebView 进程已终止，正在清理会话。")
        session.terminate_session() # 此方法会从全局字典中删除会话

    return result

multiprocessing.freeze_support()
session = Session(
    "test",
    title="test",
    html="<h1>Hello, World!</h1><p>这是一个 pywebview 示例。</p>",
)
