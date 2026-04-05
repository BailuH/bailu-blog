<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AuthService from '@/services/AuthService'

// reactive state
const username = ref('')
const password = ref('')
const isDevMode = ref(false)

async function handleSubmit() {
  await AuthService.login(username.value, password.value)
}

onMounted(() => {
  isDevMode.value = import.meta.env.MODE === 'development'
  console.log('isDevMode', import.meta.env.MODE)
})
</script>

<template>
  <q-card square class="shadow-24" style="width: 400px; height: 550px">
    <q-card-section class="bg-primary">
      <h4 class="text-white q-my-md">登录账号</h4>
    </q-card-section>

    <q-form class="q-px-md q-pt-md" @submit.prevent="handleSubmit">
      <q-input
        v-model="username"
        label="用户名"
        clearable
        :input-style="{ fontSize: '25px' }"
      >
        <template v-slot:prepend><q-icon name="face" /></template>
      </q-input>
      <q-input
        v-model="password"
        type="password"
        label="密码"
        clearable
        :input-style="{ fontSize: '25px' }"
      >
        <template v-slot:prepend><q-icon name="lock" /></template>
      </q-input>

      <q-card-actions class="q-px-lg">
        <q-btn
          unelevated
          size="lg"
          color="secondary"
          type="submit"
          class="full-width text-white"
          label="登录"
      /></q-card-actions>

      <div v-if="isDevMode" class="q-mt-lg">
        <!-- 开发模式提示：测试账号的密码和用户名均为 admin、author、reader -->
        <div class="text-h6 q-mb-xs">测试账号</div>
        <!-- Quasar 列表 -->
        <q-list>
          <q-item v-for="user in ['admin', 'author', 'reader']" :key="user" dense>
            <q-item-section>
              <q-item-label>{{ user }}:{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-form>
  </q-card>
</template>
