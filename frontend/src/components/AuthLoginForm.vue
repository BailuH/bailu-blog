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
  <q-card square class="shadow-1" style="width: 400px; max-width: 90vw;">
    <q-card-section class="bg-white border-bottom">
      <h4 class="text-dark q-my-md text-weight-bold">登录账号</h4>
    </q-card-section>

    <q-form class="q-px-md q-pt-md" @submit.prevent="handleSubmit">
      <q-input
        v-model="username"
        label="用户名"
        clearable
        :input-style="{ fontSize: '18px' }"
        outlined
        dense
        class="q-mb-md"
      >
        <template v-slot:prepend><q-icon name="face" class="text-grey-6" /></template>
      </q-input>
      <q-input
        v-model="password"
        type="password"
        label="密码"
        clearable
        :input-style="{ fontSize: '18px' }"
        outlined
        dense
        class="q-mb-md"
      >
        <template v-slot:prepend><q-icon name="lock" class="text-grey-6" /></template>
      </q-input>

      <q-card-actions class="q-px-lg">
        <q-btn
          unelevated
          size="md"
          color="accent"
          type="submit"
          class="full-width text-white"
          label="登录"
          no-caps
      /></q-card-actions>

      <div v-if="isDevMode" class="q-mt-lg">
        <!-- 开发模式提示：测试账号的密码和用户名均为 admin、author、reader -->
        <div class="text-subtitle1 q-mb-xs text-dark text-weight-bold">测试账号</div>
        <!-- Quasar 列表 -->
        <q-list>
          <q-item v-for="user in ['admin', 'author', 'reader']" :key="user" dense>
            <q-item-section>
              <q-item-label class="text-grey-7">{{ user }}:{{ user }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-form>
  </q-card>
</template>

<style scoped>
.border-bottom {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
