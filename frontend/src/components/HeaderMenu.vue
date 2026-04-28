<script setup lang="ts">
import { type UserDocument } from '@/client'

const props = defineProps<{ currentUser?: UserDocument }>()
</script>

<template>
  <q-toolbar class="text-dark">
    <q-toolbar-title class="row items-center">
      <q-avatar size="36px" class="q-mr-sm">
        <img src="../../images/eye-red.png" />
      </q-avatar>
      <q-btn
        :to="{ name: 'home' }"
        stretch
        flat
        no-caps
        class="text-weight-bold text-dark"
        label="我的博客"
      />
      <span class="text-caption text-grey-6">by BAILU</span>
    </q-toolbar-title>

    <q-space />

    <div v-if="!currentUser" class="row">
      <q-btn
        :to="{ name: 'login' }"
        stretch
        flat
        no-caps
        label="登录"
        class="text-dark"
      />
      <q-btn
        :to="{ name: 'register' }"
        stretch
        flat
        no-caps
        label="注册"
        class="text-dark"
      />
    </div>
    <div v-else class="row">
      <!-- 当用户为管理员或作者时显示的区块 -->
      <div v-if="currentUser.role == 'Admin' || currentUser.role == 'Author'">
        <q-btn
          :to="{ name: 'create-article' }"
          label="写文章"
          flat
          no-caps
          class="text-accent"
        />
      </div>
      <!-- 当用户为管理员时显示的区块 -->
      <div v-if="currentUser.role == 'Admin'">
        <q-btn
          :to="{ name: 'gpt-writer' }"
          label="GptWriter"
          flat
          no-caps
          class="text-accent"
        />
      </div>
      <!-- 对所有用户显示的区块 -->
      <q-btn
        :to="{ name: 'home' }"
        stretch
        flat
        no-caps
        label="全部文章"
        class="text-dark"
      />
      <q-btn
        :to="{name: 'users'}"
        stretch
        flat
        no-caps
        label="用户"
        class="text-dark"
      />
      <q-btn
        :to="{ name: 'profile' }"
        stretch
        flat
        no-caps
        class="text-dark"
      >
        {{ currentUser.username }}
      </q-btn>
      <q-btn
        :to="{ name: 'logout' }"
        stretch
        flat
        no-caps
        label="退出"
        class="text-dark"
      />
    </div>
  </q-toolbar>
</template>
