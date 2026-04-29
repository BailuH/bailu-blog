<script setup lang="ts">
import type { UserDocument } from '@/client'
import { computed } from 'vue'

export interface Props {
  user?: UserDocument | null
  small?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  small: () => false
})

const avatarSizeStyle = computed(() => {
  return props.small ? '44px' : '88px'
})

const roleBadge = computed(() => {
  if (!props.user?.role) return null
  if (props.user.role === 'Admin') return { text: '管理员', color: 'admin' }
  if (props.user.role === 'Author') return { text: '作者', color: 'author' }
  return { text: '读者', color: 'reader' }
})
</script>

<template>
  <div v-if="user" class="user-info-card" :class="{ 'user-info-card--small': small }">
    <router-link :to="{ name: 'user', params: { id: user._id } }" class="user-avatar-link">
      <q-avatar :size="avatarSizeStyle" class="user-avatar">
        <img :src="user?.avatar_url || '/favicon.ico'" />
      </q-avatar>
    </router-link>

    <template v-if="!props.small">
      <router-link
        :to="{ name: 'user', params: { id: user._id } }"
        class="user-username"
      >
        {{ user?.username }}
      </router-link>
      <span v-if="roleBadge" :class="['user-role', `user-role--${roleBadge.color}`]">
        {{ roleBadge.text }}
      </span>
    </template>
  </div>
</template>

<style scoped>
.user-info-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 8px;
}

.user-info-card--small {
  gap: 0;
  padding: 0;
}

.user-avatar-link {
  display: block;
  transition: transform 0.25s ease;
}

.user-avatar-link:hover {
  transform: scale(1.06);
}

.user-avatar {
  border: 3px solid #f1f5f9;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.user-avatar-link:hover .user-avatar {
  border-color: #bfdbfe;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.15);
}

.user-username {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #0f172a;
  text-align: center;
  transition: color 0.2s ease;
}

.user-username:hover {
  color: #2563eb;
}

.user-role {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.user-role--admin {
  background: #fef2f2;
  color: #ef4444;
}

.user-role--author {
  background: #eff6ff;
  color: #2563eb;
}

.user-role--reader {
  background: #f0fdf4;
  color: #10b981;
}
</style>
