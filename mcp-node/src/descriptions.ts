export const createDesc = `
弹出一个 WebView 窗口，并获取用户输入。参数为 HTML。

要求：
- 界面要求非常美观，交互形式要非常直观恰当丰富，可使用CSS或外部库;
- 注意窗口大小(一般为 1024, 768)和 padding;
- HTML 里可以包含 JS 脚本，可以访问网络资源;
- 使用 window.$submit 来提交结果并关闭窗口;
- 在需要的情况下，推荐使用非常丰富且直观的交互方式，可能包括曲线滑动条等等;
- 最好不要使用 <form> 标签;

示例：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户信息输入</title>
    <script>
        function submit() {
            window.$submit({
                user_name: document.getElementById('user_name').value,
            });
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
`

export const continueDesc = `
当调用 create-ask-ui 工具后，用户没有立刻给出结果，则可以调用该工具来再次尝试获取结果。
该工具可以连续多次调用，直到用户给出结果。
`
