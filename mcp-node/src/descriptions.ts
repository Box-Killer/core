export const createDesc = `
弹出一个 WebView 窗口，并获取用户输入。参数为 HTML。

要求：
- 界面要求非常美观，交互形式要非常直观恰当丰富，使用 tailwindcss，风格为 geist UI;
- 注意窗口宽度为 720px，高度必须要和body高度一致，body高度必须在样式中固定写出，并足够大甚至略大，必须让用户不需要滚动页面;
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
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <title>用户信息输入</title>
  <script>
    function submit() {
      alert('submit');
      window.$submit({
        username: document.getElementById('username').value
      });
    }
  </script>
</head>
<body style="height: 720px;" class="flex items-center justify-center">
  <div class="bg-white/50 backdrop-blur-sm p-8 rounded-xl border border-gray-200/50 shadow-lg">
    <h2 class="text-2xl font-semibold text-center text-gray-900 mb-8">用户信息输入</h2>
    <div class="mb-6">
      <label for="username" class="block text-gray-700 text-sm font-medium mb-3">用户名</label>
      <input type="text" id="username" name="username" placeholder="请输入用户名" required class="w-full px-4 py-3 text-gray-900 bg-white/80 border border-gray-300/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900/20 focus:border-gray-900/30 transition-all duration-200">
    </div>
    <button type="button" onclick="submit()" class="w-full bg-gray-900 hover:bg-gray-800 text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900/20 transition-all duration-200">
      确定
    </button>
  </div>
</body>
</html>
`

export const continueDesc = `
当调用 create-ask-ui 工具后，用户没有立刻给出结果，则可以调用该工具来再次尝试获取结果。
该工具可以连续多次调用，直到用户给出结果。
`
