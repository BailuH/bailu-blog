<template>
  <q-page class="not-found-page">
    <div class="not-found-content">
      <div class="not-found-icon">
        <q-icon name="search_off" size="4rem" color="grey-4" />
      </div>
      <h1 class="not-found-title">404</h1>
      <h2 class="not-found-subtitle">页面未找到</h2>
      <p class="not-found-desc">您访问的页面不存在或已被移除。</p>
      <router-link to="/" class="not-found-link">
        <q-icon name="arrow_back" size="1rem" class="q-mr-sm" />
        返回首页
      </router-link>
    </div>
  </q-page>
</template>

<style scoped>
.not-found-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.not-found-content {
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

.not-found-icon {
  margin-bottom: 20px;
}

.not-found-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 5rem;
  font-weight: 800;
  color: #e2e8f0;
  line-height: 1;
  margin: 0 0 8px 0;
}

.not-found-subtitle {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.not-found-desc {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0 0 24px 0;
}

.not-found-link {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  border-radius: 12px;
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
}

.not-found-link:hover {
  background: #1d4ed8;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
  color: #ffffff;
}
</style>
