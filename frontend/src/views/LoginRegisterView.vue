<template>
  <main>
    <div class="container">
      <div class="login-register-form">
        <!-- 登录表单 -->
        <form v-if="isLogin" @submit.prevent="handleLogin">
          <h2>用户登录</h2>
          <div class="form-group">
            <label for="loginUsername">用户名</label>
            <input type="text" id="loginUsername" v-model="loginForm.username" required>
          </div>
          <div class="form-group">
            <label for="loginPassword">密码</label>
            <input type="password" id="loginPassword" v-model="loginForm.password" required>
          </div>
          <button type="submit">登录</button>
          <p>还没有账号？<a href="#" @click="toggleForm">立即注册</a></p>
        </form>

        <!-- 注册表单 -->
        <form v-else @submit.prevent="handleRegister">
          <h2>用户注册</h2>
          <div class="form-group">
            <label for="registerUsername">用户名</label>
            <input type="text" id="registerUsername" v-model="registerForm.username" required>
          </div>
          <div class="form-group">
            <label for="registerEmail">邮箱</label>
            <input type="email" id="registerEmail" v-model="registerForm.email" required>
          </div>
          <div class="form-group">
            <label for="registerPassword">密码</label>
            <input type="password" id="registerPassword" v-model="registerForm.password" required>
          </div>
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input type="password" id="confirmPassword" v-model="registerForm.confirmPassword" required>
          </div>
          <button type="submit">注册</button>
          <p>已有账号？<a href="#" @click="toggleForm">返回登录</a></p>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axiosInstance from '@/axios';
import Cookies from 'js-cookie'

// 是否显示登录表单
const isLogin = ref(true);

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
});

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// 切换表单
const toggleForm = () => {
  isLogin.value = !isLogin.value;
};

// 处理登录
const handleLogin = () => {
  console.log('登录表单提交:', loginForm);

  // 构造符合要求的请求体
  const params = new URLSearchParams();
  params.append('grant_type', 'password'); // 固定值
  params.append('username', loginForm.username); // 用户名
  params.append('password', loginForm.password); // 密码

  // 发送请求
  axiosInstance.post('/user/auth/token', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded' // 设置正确的 Content-Type
    }
  })
    .then(function (response) {
      console.log('登录成功:', response.data);
      Cookies.set('access_token', response.data.access_token, { expires: 7 }); // 7 天后过期
      Cookies.set('token_type', response.data.token_type, { expires: 7 });

      console.log('Token 已保存到 Cookies');
    })
    .catch(function (error) {
      if (error.response) {
        // 打印详细的错误信息
        console.error('登录失败:', error.response.data);
      } else {
        console.error('请求失败:', error.message);
      }
    });
};

// 处理注册
const handleRegister = () => {
  console.log('注册表单提交:', registerForm);
  axiosInstance.post('/user/auth/register', {
    "name": registerForm.username,
    "email": registerForm.email,
    "password": registerForm.password,
  })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.form {
  display: block;
  transition: all 0.3s ease;
}

.form h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.form button:hover {
  background-color: #0056b3;
}

.form p {
  text-align: center;
  margin-top: 10px;
}

.form p a {
  color: #007bff;
  text-decoration: none;
}

.form p a:hover {
  text-decoration: underline;
}
</style>
