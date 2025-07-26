import webview

def main():
    # 创建一个 Webview 窗口
    # 第一个参数是窗口的标题
    # 第二个参数可以是 URL、HTML 字符串或文件路径
    webview.create_window('我的第一个 Webview 窗口', html='<h1>Hello, World!</h1><p>这是一个 pywebview 示例。</p>')

    # 启动 Webview 应用程序的 GUI 循环
    # 这会阻塞主线程，直到窗口关闭
    webview.start()

if __name__ == '__main__':
    main()