<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderMenu from './components/HeaderMenu.vue'
import { useUserStore } from './stores/UserStore'

const userStore = useUserStore()
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="WAL site-layout">
    <q-header reveal elevated class="bg-white text-dark">
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
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');

.site-layout {
  background-color: #e5e5e5;
  font-family: 'Open Sans', sans-serif;
}

.WAL {
  padding-top: 20px;
  padding-bottom: 20px;
}

/* 网站全部内容宽度限制（百分比） */
.content-width {
  min-width: 70%;
  max-width: 70%;
}

@media (max-width: 768px) {
  .content-width {
    min-width: 95%;
    max-width: 95%;
  }
}

/* 全局链接样式 */
a {
  color: #5e72e4;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #233dd2;
}

/* 引用块样式 */
blockquote {
  margin: 0 0 1rem;
  border-left: 2px solid rgba(136, 152, 170, 0.32);
  padding-left: 1rem;
  color: #525f7f;
}

/* 多行文本截断 */
.line-clamp-5 {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
