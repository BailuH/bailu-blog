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
  await AuthService.login(username.value, password.value)
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-logo">
          <q-avatar size="48px">
            <img src="../../images/eye-red.png" />
          </q-avatar>
        </div>
        <h2 class="auth-title">创建账号</h2>
        <p class="auth-subtitle">开始你的博客之旅</p>
      </div>

      <q-form class="auth-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <q-input
            v-model="username"
            placeholder="输入用户名"
            outlined
            dense
            class="auth-input"
          >
            <template v-slot:prepend>
              <q-icon name="person_outline" class="input-icon" />
            </template>
          </q-input>
        </div>

        <div class="form-group">
          <label class="form-label">邮箱</label>
          <q-input
            v-model="email"
            placeholder="your@email.com"
            outlined
            dense
            class="auth-input"
          >
            <template v-slot:prepend>
              <q-icon name="mail_outline" class="input-icon" />
            </template>
          </q-input>
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <q-input
            v-model="password"
            type="password"
            placeholder="设置密码"
            outlined
            dense
            class="auth-input"
          >
            <template v-slot:prepend>
              <q-icon name="lock_outline" class="input-icon" />
            </template>
          </q-input>
        </div>

        <div class="form-group">
          <label class="form-label">确认密码</label>
          <q-input
            v-model="confirmPassword"
            type="password"
            placeholder="再次输入密码"
            outlined
            dense
            class="auth-input"
          >
            <template v-slot:prepend>
              <q-icon name="lock_outline" class="input-icon" />
            </template>
          </q-input>
        </div>

        <q-btn
          unelevated
          size="md"
          color="accent"
          type="submit"
          class="auth-submit"
          label="注册"
          no-caps
        />

        <div class="auth-footer">
          <span class="text-grey-6">已有账号？</span>
          <router-link to="/login" class="auth-link">立即登录</router-link>
        </div>
      </q-form>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  padding: 24px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 24px;
  padding: 40px 36px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 16px 48px rgba(0, 0, 0, 0.03);
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.auth-logo :deep(.q-avatar) {
  transition: transform 0.3s ease;
}

.auth-logo :deep(.q-avatar:hover) {
  transform: scale(1.1) rotate(-4deg);
}

.auth-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.auth-subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
}

.auth-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
  border-color: #e2e8f0;
  min-height: 48px;
  transition: all 0.2s ease;
}

.auth-input :deep(.q-field__control:hover) {
  border-color: #cbd5e1;
}

.auth-input :deep(.q-field--focused .q-field__control) {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
  background: #ffffff;
}

.input-icon {
  color: #94a3b8;
}

.auth-submit {
  height: 48px;
  border-radius: 12px !important;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
  transition: all 0.2s ease;
  margin-top: 8px;
}

.auth-submit:hover {
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.auth-footer {
  text-align: center;
  margin-top: 8px;
  font-size: 0.88rem;
}

.auth-link {
  color: #2563eb;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.2s ease;
}

.auth-link:hover {
  color: #1d4ed8;
}

@media (max-width: 768px) {
  .auth-card {
    padding: 28px 24px;
    border-radius: 20px;
  }
  
  .auth-title {
    font-size: 1.3rem;
  }
}
</style>
