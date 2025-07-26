

import tkinter as tk
from tkinter import ttk
from mcp.server.fastmcp import FastMCP
import textwrap
from ttkthemes import ThemedTk

# Create an MCP server
mcp = FastMCP("Ask UI")


@mcp.tool()
def ask_ui(code: str) -> dict:
    """
弹出一个 Tkinter 窗口，获取用户输入。

要求：
- code 里必须定义 main 函数，作为窗口的逻辑
- main 函数的参数是按关键字传入的 root, tk, ttk
- main 函数的返回值是获取的用户输入字典
- 你可以自定义按钮、输入框、标签等控件，实现任意交互

示例：
def main(root, tk, ttk):
    root.deiconify()
    root.title("自定义输入")
    ttk.Label(root, text="请输入用户名：").pack()
    entry = ttk.Entry(root)
    entry.pack()
    ttk.Button(root, text="确定", command=lambda: root.quit()).pack()
    root.mainloop()
    return {
        "user_name": entry.get()
    }
"""
    # Preprocess code
    code = textwrap.dedent(code)

    # Run code
    local_vars = {}
    global_vars = {}

    exec(code, global_vars, local_vars)
    main_fn = local_vars.get("main", global_vars.get("main", None))

    root = ThemedTk(theme="yaru")
    # style = ttk.Style()

    # # 查看可用主题
    # print(style.theme_names())

    # # 尝试切换主题
    # style.theme_use("clam") 

    result = main_fn(
        root=root,
        tk=tk,
        ttk=ttk,
    )

    root.destroy()
    
    return result

if __name__ == "__main__":
    mcp.run()
