<template>
  <div class="min-h-screen flex flex-col">
    <!-- 头部 -->
    <header class="flex flex-row justify-between text-gufeng_2 p-4 w-full bg-gufeng_3">
      <div class="tracking-wide text-xl drop-shadow-xl">
        ⛺演示标题
      </div>
      <div class="flex space-x-4 place-self-center">
        <RouterLink to="/" class="text-white hover:text-gray-300">首页</RouterLink>
        <a href="#" class="text-white hover:text-gray-300">文章</a>
        <a href="#" class="text-white hover:text-gray-300">标签</a>
        <RouterLink to="/login&register" class="text-white hover:text-gray-300">登录注册</RouterLink>
        <RouterLink to="/user/me" class="text-white hover:text-gray-300">用户</RouterLink>
        <RouterLink to="/about" class="text-white hover:text-gray-300">关于</RouterLink>
      </div>
    </header>

    <!-- 中间内容区 -->
    <main class="flex-1 p-4 w-full bg-gufeng_1 ">
      <RouterView />
    </main>
    <!-- 底部 -->
    <footer class="text-gufeng_2  p-4 w-full bg-gufeng_4">
      <div class="place-self-center">
        作者:小朱
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped></style>
