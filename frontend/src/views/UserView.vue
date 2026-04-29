<script setup lang="ts">
import { DefaultService, type UserDocument } from '@/client'
import UserCard from '@/components/UserCard.vue'
import AuthService from '@/services/AuthService'
import { useUserStore } from '@/stores/UserStore'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const user = ref<UserDocument>()
const editable = ref<boolean>(false)
const isProfile = ref<boolean>(false)

const route = useRoute()

onMounted(async () => {
  const current_user = useUserStore().user

  if (route.path == '/profile') {
    AuthService.update_user_info()
    user.value = current_user
    isProfile.value = true
    editable.value = true
  } else {
    const userId = route.params.id.toString()
    if (userId == current_user?._id) {
      isProfile.value = true
    }
    const userResponse = await DefaultService.getUserByIdUsersUserIdGet(userId)
    user.value = userResponse.user
    editable.value = current_user?.role == 'Admin' ? true : false
  }
})
</script>

<template>
  <q-page v-if="user" class="profile-page">
    <!-- Cover Banner -->
    <div class="profile-cover">
      <!-- [预留] 用户封面背景图 -->
      <div class="profile-cover-image">
        <div class="cover-placeholder">
          <q-icon name="panorama" size="2.5rem" color="blue-3" />
          <span class="cover-placeholder-text">[预留] 用户封面背景图</span>
          <span class="cover-placeholder-hint">建议尺寸 1200×240，可设置个性封面</span>
        </div>
      </div>
      <div class="profile-cover-overlay"></div>
    </div>

    <!-- Profile Content -->
    <div class="profile-content">
      <UserCard :isProfile="isProfile" :editable="editable" :user="user" />
    </div>
  </q-page>
</template>

<style scoped>
.profile-page {
  padding: 0 0 48px;
}

/* ===== Cover Banner ===== */
.profile-cover {
  position: relative;
  width: 100%;
  height: 220px;
  border-radius: 0 0 24px 24px;
  overflow: hidden;
  margin-bottom: -40px;
}

.profile-cover-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 50%, #dbeafe 100%);
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #94a3b8;
}

.cover-placeholder-text {
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
}

.cover-placeholder-hint {
  font-size: 0.75rem;
  color: #94a3b8;
}

.profile-cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: linear-gradient(to top, #ffffff, transparent);
  pointer-events: none;
}

/* ===== Profile Content ===== */
.profile-content {
  position: relative;
  z-index: 1;
}

@media (max-width: 768px) {
  .profile-cover {
    height: 160px;
    border-radius: 0 0 20px 20px;
    margin-bottom: -24px;
  }

  .cover-placeholder-text {
    font-size: 0.82rem;
  }
}
</style>
