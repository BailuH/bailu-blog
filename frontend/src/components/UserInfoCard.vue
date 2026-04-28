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
  return props.small ? '50px' : '100px'
})
</script>

<template>
  <div
    v-if="user"
    avatar
    class="column items-center justify-start"
  >
    <q-avatar :size="avatarSizeStyle" rounded>
      <q-img :src="user?.avatar_url!" />
    </q-avatar>

    <template v-if="!props.small">
      <q-item-label
        lines="1"
        class="text-subtitle1 text-uppercase text-dark text-weight-bold q-my-sm"
      >
        {{ user?.username }}
      </q-item-label>
      <q-item-label lines="1" class="text-subtitle2 text-grey-6 text-weight-bold q-my-sm">
        <span v-if="user?.role == 'Author'" class="text-info">作者</span>
        <span v-else-if="user?.role == 'Admin'" class="text-negative">管理员</span>
      </q-item-label></template
    >
  </div>
</template>
