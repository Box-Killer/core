

import tkinter as tk
from tkinter import ttk, messagebox
from mcp.server.fastmcp import FastMCP
import textwrap
from ttkthemes import ThemedTk
import os

# Create an MCP server
mcp = FastMCP("Ask UI")


def setup_modern_style(root):
    """设置现代化的样式"""
    style = ttk.Style()
    
    # 尝试使用更现代的主题
    available_themes = style.theme_names()
    modern_themes = ['azure', 'breeze', 'equilux', 'arc', 'smog']
    
    # 选择可用的现代主题
    selected_theme = None
    for theme in modern_themes:
        if theme in available_themes:
            selected_theme = theme
            break
    
    if selected_theme:
        style.theme_use(selected_theme)
    else:
        # 如果没有现代主题，使用默认主题并自定义样式
        style.theme_use('clam')
    
    # 自定义样式配置
    style.configure('Modern.TFrame', background='#f0f0f0')
    style.configure('Modern.TLabel', 
                   background='#f0f0f0', 
                   font=('Segoe UI', 10),
                   foreground='#2c3e50')
    style.configure('Modern.TButton', 
                   font=('Segoe UI', 10, 'bold'),
                   padding=(20, 10),
                   background='#3498db',
                   foreground='white')
    style.configure('Modern.TEntry', 
                   font=('Segoe UI', 10),
                   padding=(10, 8),
                   fieldbackground='white',
                   borderwidth=2,
                   relief='solid')
    
    # 配置根窗口样式
    root.configure(bg='#f0f0f0')
    
    # 设置窗口图标（如果有的话）
    try:
        # 尝试设置一个现代化的图标
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    return style


def create_modern_frame(parent, title=None):
    """创建现代化的框架"""
    frame = ttk.Frame(parent, style='Modern.TFrame')
    
    if title:
        title_label = ttk.Label(frame, text=title, style='Modern.TLabel')
        title_label.pack(pady=(10, 5))
    
    return frame


@mcp.tool()
def ask_ui(code: str) -> dict:
    """
弹出一个美化的 Tkinter 窗口，获取用户输入。

要求：
- code 里必须定义 main 函数，作为窗口的逻辑
- main 函数的参数是按关键字传入的 root, tk, ttk, style, create_modern_frame
- main 函数的返回值是获取的用户输入字典
- 你可以自定义按钮、输入框、标签等控件，实现任意交互

示例：
def main(root, tk, ttk, style, create_modern_frame):
    root.title("用户信息输入")
    root.geometry("400x300")
    
    # 创建主框架
    main_frame = create_modern_frame(root, "用户信息输入")
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # 用户名输入
    name_frame = ttk.Frame(main_frame)
    name_frame.pack(fill='x', pady=10)
    ttk.Label(name_frame, text="用户名：", style='Modern.TLabel').pack(anchor='w')
    name_entry = ttk.Entry(name_frame, style='Modern.TEntry')
    name_entry.pack(fill='x', pady=(5, 0))
    
    # 邮箱输入
    email_frame = ttk.Frame(main_frame)
    email_frame.pack(fill='x', pady=10)
    ttk.Label(email_frame, text="邮箱：", style='Modern.TLabel').pack(anchor='w')
    email_entry = ttk.Entry(email_frame, style='Modern.TEntry')
    email_entry.pack(fill='x', pady=(5, 0))
    
    # 按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=20)
    
    def submit():
        if name_entry.get().strip() and email_entry.get().strip():
            root.quit()
        else:
            messagebox.showwarning("警告", "请填写完整信息！")
    
    submit_btn = ttk.Button(button_frame, text="提交", 
                           style='Modern.TButton', command=submit)
    submit_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = ttk.Button(button_frame, text="取消", 
                           style='Modern.TButton', command=root.quit)
    cancel_btn.pack(side='right')
    
    root.mainloop()
    
    return {
        "user_name": name_entry.get(),
        "email": email_entry.get()
    }
"""
    # Preprocess code
    code = textwrap.dedent(code)

    # Run code
    local_vars = {}
    global_vars = {}

    exec(code, global_vars, local_vars)
    main_fn = local_vars.get("main", global_vars.get("main", None))

    # 创建美化的根窗口
    root = ThemedTk()
    
    # 设置窗口属性
    root.title("现代化用户界面")
    root.geometry("500x400")
    root.resizable(True, True)
    
    # 设置现代化样式
    style = setup_modern_style(root)
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    try:
        result = main_fn(
            root=root,
            tk=tk,
            ttk=ttk,
            style=style,
            create_modern_frame=create_modern_frame,
        )
    except Exception as e:
        messagebox.showerror("错误", f"界面运行出错：{str(e)}")
        result = {"error": str(e)}
    finally:
        root.destroy()
    
    return result


if __name__ == "__main__":
    mcp.run()
