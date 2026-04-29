<script setup lang="ts">
import { computed, ref } from 'vue'
import UserInfoCard from './UserInfoCard.vue'
import { DefaultService, UsersSortField, type UserDocument, SortDirection } from '@/client'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

const users = ref<UserDocument[]>([])
const limit = ref<number>(10)
const skip = ref<number>(0)
const sortBy = ref<UsersSortField>(UsersSortField.CREATED_AT)
const sortOrder = ref<SortDirection>(SortDirection._1)

const currentUserIsAdmin = computed(() => {
  return useUserStore().user?.role === 'Admin'
})

const loadMoreUsers = async () => {
  const usersResponse = await DefaultService.listUsersUsersGet(
    skip.value,
    limit.value,
    sortBy.value,
    sortOrder.value
  )
  users.value.push(...usersResponse.users)
  skip.value += limit.value
  return usersResponse.users.length
}

const loadMore = async (_index: number, done: CallableFunction) => {
  const usersLoaded = await loadMoreUsers()
  done(usersLoaded > 0 ? false : true)
}

const handleSelectorChange = async () => {
  users.value = []
  skip.value = 0
  limit.value = 10
  await loadMoreUsers()
}

const handleDisableUserButton = async (userId: string) => {
  await DefaultService.disableUserUsersUserIdDisablePut(userId)
  Notify.create('用户 ' + userId + ' 已被禁用')
}

// 初始加载由 q-infinite-scroll 自动触发，避免与 onBeforeMount 重复加载
</script>

<template>
  <div class="users-page">
    <!-- Header -->
    <div class="users-header">
      <h2 class="users-title">用户列表</h2>
      <div class="users-filters">
        <q-select
          v-model="sortBy"
          :options="[
            { label: '创建日期', value: UsersSortField.CREATED_AT },
            { label: '用户名', value: UsersSortField.USERNAME }
          ]"
          emit-value
          map-options
          label="排序"
          @update:model-value="handleSelectorChange"
          class="filter-select"
          outlined
          dense
        />
        <q-select
          v-model="sortOrder"
          :options="[
            { label: '升序', value: SortDirection['_1'] },
            { label: '降序', value: SortDirection['_-1'] }
          ]"
          emit-value
          map-options
          label="顺序"
          @update:model-value="handleSelectorChange"
          class="filter-select"
          outlined
          dense
        />
      </div>
    </div>

    <!-- Users list -->
    <q-infinite-scroll @load="loadMore" :offset="10" class="users-list">
      <div
        v-for="(user, index) in users"
        :key="user._id!"
        class="user-item"
        :style="{ animationDelay: `${index * 0.05}s` }"
      >
        <router-link :to="{ name: 'user', params: { id: user._id } }" class="user-avatar-link">
          <q-avatar size="56px" class="user-list-avatar">
            <img :src="user.avatar_url || '/favicon.ico'" />
          </q-avatar>
        </router-link>

        <div class="user-details">
          <div class="user-name-row">
            <router-link
              :to="{ name: 'user', params: { id: user._id } }"
              class="user-list-name"
            >
              {{ user.username }}
            </router-link>
            <span v-if="!user.role" class="role-badge role-badge--unconfirmed">未确认</span>
            <span v-else-if="user.role === 'Admin'" class="role-badge role-badge--admin">管理员</span>
            <span v-else-if="user.role === 'Author'" class="role-badge role-badge--author">作者</span>
            <span v-if="user.disabled" class="role-badge role-badge--banned">已封禁</span>
          </div>
          <div class="user-email">{{ user.email }}</div>
          <div class="user-stats-row">
            <span class="user-stat">
              <q-icon name="chat_bubble_outline" size="0.8rem" class="q-mr-xs" />
              {{ (user as any).comments_count ?? 0 }} 条评论
            </span>
          </div>
        </div>

        <div v-if="currentUserIsAdmin && !user.disabled" class="user-admin-actions">
          <button
            @click="handleDisableUserButton(user._id!)"
            class="ban-btn"
          >
            <q-icon name="block" size="0.9rem" />
            封禁
          </button>
        </div>
      </div>
    </q-infinite-scroll>
  </div>
</template>

<style scoped>
.users-page {
  padding: 16px 0;
  animation: fadeInUp 0.4s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.users-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.users-filters {
  display: flex;
  gap: 12px;
}

.filter-select {
  min-width: 130px;
}

.filter-select :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 24px;
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
  transition: all 0.25s ease;
  animation: fadeInUp 0.4s ease both;
}

.user-item:hover {
  border-color: #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.user-avatar-link {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.user-avatar-link:hover {
  transform: scale(1.06);
}

.user-list-avatar {
  border: 2px solid #f1f5f9;
  transition: border-color 0.2s ease;
}

.user-avatar-link:hover .user-list-avatar {
  border-color: #bfdbfe;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  flex-wrap: wrap;
}

.user-list-name {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #0f172a;
  transition: color 0.2s ease;
}

.user-list-name:hover {
  color: #2563eb;
}

.role-badge {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.role-badge--admin {
  background: #fef2f2;
  color: #ef4444;
}

.role-badge--author {
  background: #eff6ff;
  color: #2563eb;
}

.role-badge--unconfirmed {
  background: #fef3c7;
  color: #d97706;
}

.role-badge--banned {
  background: #fef2f2;
  color: #ef4444;
}

.user-email {
  color: #94a3b8;
  font-size: 0.85rem;
  margin-bottom: 4px;
}

.user-stats-row {
  display: flex;
  gap: 12px;
}

.user-stat {
  display: inline-flex;
  align-items: center;
  color: #64748b;
  font-size: 0.82rem;
  font-weight: 500;
}

.user-admin-actions {
  flex-shrink: 0;
}

.ban-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #ef4444;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.ban-btn:hover {
  background: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
}

@media (max-width: 768px) {
  .users-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-item {
    padding: 14px 16px;
  }
  
  .user-list-name {
    font-size: 0.95rem;
  }
}
</style>
