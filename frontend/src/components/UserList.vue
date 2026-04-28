<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
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

// 加载更多用户的函数
const loadMoreUsers = async () => {
  console.debug('加载用户')
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

// 滚动时加载的函数
const loadMore = async (_index: number, done: CallableFunction) => {
  const usersLoaded = await loadMoreUsers()
  done(usersLoaded > 0 ? false : true)
}

// 排序参数变更时重置的函数
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

onBeforeMount(async () => {
  await loadMoreUsers()
})
</script>

<template>
  <div class="column q-pa-md">
    <!-- Header -->
    <div class="row justify-end q-mb-md">
      <!-- 排序选择器 -->
      <q-select
        v-model="sortBy"
        :options="[
          { label: '按创建日期', value: UsersSortField.CREATED_AT },
          { label: '按用户名', value: UsersSortField.USERNAME }
        ]"
        emit-value
        map-options
        label="排序方式"
        @update:model-value="handleSelectorChange"
        class="col-3"
        outlined
        dense
        bg-color="white"
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
        class="col-3 q-ml-md"
        outlined
        dense
        bg-color="white"
      />
    </div>

    <!-- 用户列表 -->
    <q-list separator padding>
      <!-- 无限滚动 -->
      <q-infinite-scroll @load="loadMore" :offset="10">
        <!-- 用户 -->
        <div v-for="user in users" :key="user._id!" class="row bg-white q-mb-lg q-pa-md rounded-borders shadow-1">
          <!-- 头像和用户名 -->
          <router-link :to="{ name: 'user', params: { id: user._id } }" class="user-link col-2">
            <UserInfoCard :user="user" />
          </router-link>
          <!-- 用户信息 -->
          <div class="col-grow q-mx-md">
            <div class="row items-center">
              <div class="text-h6 text-dark">{{ user.username }}</div>
              <div class="text-subtitle2 q-ml-sm text-grey-6">
                ({{ user.role ?? '账号未确认' }})
              </div>
              <div v-if="user.disabled" class="text-subtitle2 q-ml-sm text-negative">
                [已封禁]
              </div>
            </div>
            <div class="text-subtitle2 text-grey-7">{{ user.email }}</div>
            <div class="text-subtitle2 text-grey-7">评论数：{{ user.comments_count ?? 'NULL' }}</div>
          </div>
          <!-- 操作 -->
          <div v-if="currentUserIsAdmin" class="col-2">
            <div class="text-center text-dark text-weight-bold">管理员操作</div>
            <q-separator class="q-mb-sm" />
            <q-btn
              v-if="!user.disabled"
              class="q-mb-sm full-width"
              label="封禁"
              @click="handleDisableUserButton(user._id!)"
              flat
              no-caps
              color="negative"
            />
          </div>
        </div>
      </q-infinite-scroll>
    </q-list>
  </div>
</template>

<style scoped>
.user-link {
  text-decoration: none;
}
</style>
