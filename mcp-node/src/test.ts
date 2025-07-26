import { createSession } from "./session.ts";

const config = {
  html: `
  <!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css">
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
  <main class="container">
    <h1>用户登录</h1>
    <label for="username">用户名</label>
    <input type="text" id="username" name="username" placeholder="请输入用户名" required>
    <label for="password">密码</label>
    <input type="password" id="password" name="password" placeholder="请输入密码" required>
    <button type="button" onclick="submit()">登录</button>

  </main>
</body>
</html>
`,
  title: "用户登录",
  width: 400,
  height: 350,
};

console.log(config.html);

createSession(config.html, {
  ...config,
});
