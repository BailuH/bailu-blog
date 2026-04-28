<script setup lang="ts">
import { DefaultService } from '@/client'
import AuthService from '@/services/AuthService'
import { Notify } from 'quasar'
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleSubmit = async () => {
  // 检查密码是否匹配
  if (password.value != confirmPassword.value) {
    Notify.create('密码不匹配')
    return
  }

  const registerResponse = await DefaultService.registerUserRegisterPost({
    username: username.value,
    password: password.value,
    email: email.value
  })

  Notify.create('注册成功。已创建账号：' + registerResponse.username)
  // 注册成功后自动登录
  await AuthService.login(username.value, password.value)
}
</script>

<template>
  <div>
    <q-card square class="shadow-1" style="width: 400px; max-width: 90vw;">
      <q-card-section class="bg-white border-bottom">
        <h4 class="text-dark q-my-md text-weight-bold">注册</h4>
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
          v-model="email"
          label="E-mail"
          clearable
          :input-style="{ fontSize: '18px' }"
          outlined
          dense
          class="q-mb-md"
        >
          <template v-slot:prepend><q-icon name="mail" class="text-grey-6" /></template>
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

        <q-input
          v-model="confirmPassword"
          type="password"
          label="确认密码"
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
            label="注册"
            no-caps
        /></q-card-actions>
      </q-form>
    </q-card>
  </div>
</template>

<style scoped>
.border-bottom {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
