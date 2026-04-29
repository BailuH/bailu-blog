<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderMenu from './components/HeaderMenu.vue'
import { useUserStore } from './stores/UserStore'

const userStore = useUserStore()
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="site-layout">
    <q-header reveal class="site-header">
      <HeaderMenu :currentUser="userStore.user" />
    </q-header>

    <q-page-container class="column items-center">
      <div class="content-width">
        <RouterView />
      </div>
    </q-page-container>
  </q-layout>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

.site-layout {
  background-color: #ffffff;
  font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
}

/* 网站全部内容宽度限制 */
.content-width {
  width: 100%;
  max-width: 960px;
  padding: 0 24px;
}

@media (max-width: 768px) {
  .content-width {
    padding: 0 16px;
  }
}

/* 全局链接样式 */
a {
  color: #2563eb;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #1d4ed8;
}

/* 引用块样式 */
blockquote {
  margin: 0 0 1rem;
  border-left: 3px solid #2563eb;
  padding-left: 1.25rem;
  color: #475569;
  font-style: italic;
}

/* 多行文本截断 */
.line-clamp-5 {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Quasar 全局组件微调 */
.q-field--outlined .q-field__control {
  border-radius: 10px !important;
}

.q-btn {
  border-radius: 10px !important;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.q-chip {
  border-radius: 8px !important;
  font-weight: 500;
}

.q-card {
  border-radius: 16px !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 8px 24px rgba(0, 0, 0, 0.04) !important;
}

.q-dialog .q-card {
  border-radius: 20px !important;
}

.q-pagination .q-btn {
  border-radius: 10px !important;
}

/* 输入框聚焦状态 */
.q-field--focused .q-field__control::after {
  border-color: #2563eb !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* md-editor 样式微调 */
.md-editor {
  border-radius: 12px !important;
  border: 1px solid #e2e8f0 !important;
}

/* 页面标题字体 */
h1, h2, h3, h4, h5, h6,
.text-h1, .text-h2, .text-h3, .text-h4, .text-h5, .text-h6 {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
  font-weight: 700;
  color: #0f172a;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
