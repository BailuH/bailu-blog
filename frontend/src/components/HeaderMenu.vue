<script setup lang="ts">
import { type UserDocument } from '@/client'

const props = defineProps<{ currentUser?: UserDocument }>()
</script>

<template>
  <q-toolbar class="header-toolbar">
    <q-toolbar-title class="row items-center no-wrap">
      <q-avatar size="34px" class="q-mr-sm logo-avatar">
        <img src="../../images/eye-red.png" />
      </q-avatar>
      <router-link
        :to="{ name: 'home' }"
        class="header-brand"
      >
        我的博客
      </router-link>
      <span class="header-byline">by BAILU</span>
    </q-toolbar-title>

    <q-space />

    <div v-if="!currentUser" class="row items-center nav-links">
      <q-btn
        :to="{ name: 'login' }"
        flat
        no-caps
        label="登录"
        class="nav-btn"
      />
      <q-btn
        :to="{ name: 'register' }"
        unelevated
        no-caps
        label="注册"
        class="nav-btn nav-btn--primary"
        color="accent"
        text-color="white"
      />
    </div>
    <div v-else class="row items-center nav-links">
      <div v-if="currentUser.role == 'Admin' || currentUser.role == 'Author'" class="row items-center">
        <q-btn
          :to="{ name: 'create-article' }"
          label="写文章"
          flat
          no-caps
          class="nav-btn nav-btn--accent"
          icon="edit"
        />
      </div>
      <div v-if="currentUser.role == 'Admin'" class="row items-center">
        <q-btn
          :to="{ name: 'gpt-writer' }"
          label="GptWriter"
          flat
          no-caps
          class="nav-btn nav-btn--accent"
          icon="auto_fix_high"
        />
      </div>
      <q-btn
        :to="{ name: 'home' }"
        flat
        no-caps
        label="全部文章"
        class="nav-btn"
        icon="article"
      />
      <q-btn
        :to="{name: 'users'}"
        flat
        no-caps
        label="用户"
        class="nav-btn"
        icon="people"
      />
      <q-btn
        :to="{ name: 'profile' }"
        flat
        no-caps
        class="nav-btn nav-btn--user"
      >
        <q-avatar size="26px" class="q-mr-xs">
          <img :src="currentUser.avatar_url || '/favicon.ico'" />
        </q-avatar>
        <span>{{ currentUser.username }}</span>
      </q-btn>
      <q-btn
        :to="{ name: 'logout' }"
        flat
        no-caps
        label="退出"
        class="nav-btn nav-btn--muted"
        icon="logout"
      />
    </div>
  </q-toolbar>
</template>

<style scoped>
.header-toolbar {
  background: #0f172a;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  padding: 8px 24px;
  min-height: 64px;
}

.header-brand {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  color: white;
  text-decoration: none;
  letter-spacing: -0.02em;
  transition: color 0.2s ease;
}

.header-brand:hover {
  color: #2563eb;
}

.header-byline {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 8px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.logo-avatar {
  transition: transform 0.3s ease;
}

.logo-avatar:hover {
  transform: scale(1.08) rotate(-4deg);
}

.nav-links {
  gap: 4px;
}

.nav-btn {
  color: #475569;
  font-weight: 500;
  font-size: 0.875rem;
  padding: 6px 14px;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: rgba(37, 99, 235, 0.06);
  color: #2563eb;
}

.nav-btn--primary {
  padding: 6px 18px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

.nav-btn--primary:hover {
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.nav-btn--accent {
  color: #2563eb;
}

.nav-btn--accent:hover {
  background: rgba(37, 99, 235, 0.08);
}

.nav-btn--user {
  color: white;
  font-weight: 600;
}

.nav-btn--muted {
  color: #94a3b8;
}

.nav-btn--muted:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.06);
}

@media (max-width: 768px) {
  .header-toolbar {
    padding: 8px 12px;
  }
  
  .nav-btn {
    padding: 6px 8px;
    font-size: 0.8rem;
  }
  
  .nav-btn--primary {
    padding: 6px 12px;
  }
  
  .header-byline {
    display: none;
  }
}
</style>
