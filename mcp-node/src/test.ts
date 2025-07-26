import { createSession } from "./session.ts";

const config = {
  html: `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <title>用户登录</title>
  <script>
    function submit() {
      alert('submit');
      window.$submit({
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
      });
    }
  </script>
</head>
<body>
  <div class="bg-white/50 backdrop-blur-sm p-8 rounded-xl border border-gray-200/50 shadow-lg">
    <h2 class="text-2xl font-semibold text-center text-gray-900 mb-8">用户登录</h2>
    <div class="mb-6">
      <label for="username" class="block text-gray-700 text-sm font-medium mb-3">用户名</label>
      <input type="text" id="username" name="username" placeholder="请输入用户名" required class="w-full px-4 py-3 text-gray-900 bg-white/80 border border-gray-300/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900/20 focus:border-gray-900/30 transition-all duration-200">
    </div>
    <div class="mb-8">
      <label for="password" class="block text-gray-700 text-sm font-medium mb-3">密码</label>
      <input type="password" id="password" name="password" placeholder="请输入密码" required class="w-full px-4 py-3 text-gray-900 bg-white/80 border border-gray-300/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900/20 focus:border-gray-900/30 transition-all duration-200">
    </div>
    <button type="button" onclick="submit()" class="w-full bg-gray-900 hover:bg-gray-800 text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900/20 transition-all duration-200">
      登录
    </button>
  </div>
</body>
</html>
`,
  title: "用户登录",
  width: 720,
  height: 600,
};

console.log(config.html);

createSession(config.html, {
  ...config,
});
