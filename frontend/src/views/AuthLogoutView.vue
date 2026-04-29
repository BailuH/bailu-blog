<script setup lang="ts">
import AuthService from '@/services/AuthService'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const countdown = ref(2)
const router = useRouter()

onMounted(() => {
  AuthService.logout()
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      router.push('/')
    }
  }, 1000)
})
</script>

<template>
  <q-page class="logout-page">
    <div class="logout-card">
      <div class="logout-icon-wrapper">
        <q-icon name="logout" size="2.5rem" color="white" />
      </div>
      <h1 class="logout-title">正在退出</h1>
      <p class="logout-desc">感谢你的访问，期待下次再见</p>
      <div class="logout-progress">
        <div class="logout-progress-bar"></div>
      </div>
      <p class="logout-redirect">
        {{ countdown }} 秒后自动跳转至首页...
      </p>
      <router-link to="/" class="logout-link">
        立即返回首页
      </router-link>
    </div>
  </q-page>
</template>

<style scoped>
.logout-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.logout-card {
  text-align: center;
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

.logout-icon-wrapper {
  width: 72px;
  height: 72px;
  border-radius: 24px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 12px 32px rgba(37, 99, 235, 0.35);
  }
}

.logout-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.logout-desc {
  color: #94a3b8;
  font-size: 1rem;
  margin: 0 0 28px 0;
}

.logout-progress {
  width: 200px;
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  margin: 0 auto 16px;
  overflow: hidden;
}

.logout-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
  border-radius: 2px;
  animation: progress 2s linear forwards;
}

@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.logout-redirect {
  color: #94a3b8;
  font-size: 0.85rem;
  margin: 0 0 16px 0;
}

.logout-link {
  display: inline-flex;
  align-items: center;
  padding: 10px 24px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.logout-link:hover {
  background: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
}
</style>
