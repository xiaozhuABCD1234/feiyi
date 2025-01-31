<template>
  <div class="about">
    <div>{{ userdata.id }}</div>
    <div>{{ userdata.username }}</div>
    <div>{{ userdata.email }}</div>
  </div>
</template>

<style></style>

<script setup lang="ts">
import axiosInstance from '@/axios';
import { reactive, onMounted } from 'vue';

const userdata = reactive({
  id: 0,
  username: '',
  email: ''
});

onMounted(() => {
  axiosInstance.get("user/auth/me")
    .then(function (response) {
      userdata.id = response.data.id;
      userdata.username = response.data.name;
      userdata.email = response.data.email;
    })
    .catch(function (error) {
      console.log(error);
    })
})

</script>
