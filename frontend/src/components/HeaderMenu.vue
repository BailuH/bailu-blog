<script setup lang="ts">
import { type UserDocument } from '@/client'

const props = defineProps<{ currentUser?: UserDocument }>()
</script>

<template>
  <q-toolbar>
    <q-toolbar-title>
      <q-avatar>
        <img src="https://img.icons8.com/3d-fluency/94/disguised-face-1.png" />
      </q-avatar>
      <q-btn :to="{ name: 'home' }" stretch flat>fastapi-mongodb-vue-blog</q-btn>
      <router-link to="{ name: 'about' }" custom>by Desunovu</router-link>
    </q-toolbar-title>

    <q-space />

    <div v-if="!currentUser" class="row">
      <q-btn :to="{ name: 'login' }" stretch flat label="登录" />
      <q-btn :to="{ name: 'register' }" stretch flat label="注册" />
    </div>
    <div v-else class="row">
      <!-- 当用户为管理员或作者时显示的区块 -->
      <div v-if="currentUser.role == 'Admin' || currentUser.role == 'Author'" class="text-accent">
        <q-btn :to="{ name: 'create-article' }" label="写文章" flat />
      </div>
      <!-- 当用户为管理员时显示的区块 -->
      <div v-if="currentUser.role == 'Admin'" class="text-accent">
        <q-btn :to="{ name: 'gpt-writer' }" label="GptWriter" flat />
      </div>
      <!-- 对所有用户显示的区块 -->
      <q-btn :to="{ name: 'home' }" stretch flat label="全部文章" />
      <q-btn :to="{name: 'users'}" stretch flat label="用户" />
      <q-btn :to="{ name: 'profile' }" stretch flat>{{ currentUser.username }}</q-btn>
      <q-btn :to="{ name: 'logout' }" stretch flat label="退出" />
    </div>
  </q-toolbar>
</template>
