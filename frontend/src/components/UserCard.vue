<script setup lang="ts">
import { DefaultService, RolesEnum, type UserDocument } from '@/client'
import AuthService from '@/services/AuthService'
import { Notify } from 'quasar'
import { computed, ref } from 'vue'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { useUserStore } from '@/stores/UserStore'

export interface Props {
  user?: UserDocument | null
  editable?: boolean
  isProfile?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isProfile: () => false,
  editable: () => false
})

const currentUser = useUserStore().user

const showEmailDialog = ref(false)
const showPasswordDialog = ref(false)
const showAvatarDialog = ref(false)
const newEmail = ref<string>()
const newPassword = ref<string>('')
const oldPassword = ref<string>('')
const avatarsToChoose = ref<string[]>([])
const newRole = ref<RolesEnum | null>(null)

const isAllowedToChangeUserRole = computed(() => {
  return props.user?.role != 'Admin' && currentUser?.role == 'Admin'
})

async function loadAvatarsToChoose() {
  const avatarsResponse = {
    avatars: [
      'https://cdn-icons-png.flaticon.com/512/149/149071.png',
      'https://cdn-icons-png.flaticon.com/512/149/149072.png',
      'https://cdn-icons-png.flaticon.com/512/149/149074.png'
    ]
  }
  avatarsToChoose.value = avatarsResponse.avatars
}

async function handleAvatarUpdate(avatarUrl: string) {
  const updateAvatarResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user?._id ?? (props.user as any).id,
    { avatar_url: avatarUrl }
  )
  Notify.create('已设置头像，请刷新页面')
}

async function prepareAvatarDialog() {
  showAvatarDialog.value = true
  await loadAvatarsToChoose()
}

async function handleEmailUpdate() {
  const updateEmailResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user?._id ?? (props.user as any).id,
    { email: newEmail.value }
  )
  Notify.create('已设置邮箱，请刷新页面')
  if (props.isProfile) {
    AuthService.update_user_info()
  }
}

async function handlePasswordUpdate() {
  await DefaultService.updateUserPasswordUsersUserIdPasswordPut((props.user as any)?._id ?? (props.user as any).id, {
    old_password: oldPassword.value,
    new_password: newPassword.value
  })
  Notify.create('新密码已设置！')
}

async function handleRoleUpdate() {
  await DefaultService.changeUserRoleUsersUserIdRolePut((props.user as any)?._id ?? '', {
    role: newRole.value!
  })
  Notify.create('已设置角色：' + newRole.value)
}
</script>

<template>
  <div v-if="user" class="user-profile-card">
    <!-- Profile Header -->
    <div class="profile-header">
      <div class="profile-avatar-section">
        <q-avatar size="96px" class="profile-avatar">
          <img :src="user.avatar_url || '/favicon.ico'" />
        </q-avatar>
        <div class="profile-info">
          <h2 class="profile-name">{{ user.username }}</h2>
          <div class="profile-meta">
            <span class="profile-email">{{ user.email }}</span>
            <span v-if="!(user as any)?.role" class="profile-status profile-status--unconfirmed">未确认</span>
            <span v-else-if="user.role === 'Admin'" class="profile-status profile-status--admin">管理员</span>
            <span v-else-if="user.role === 'Author'" class="profile-status profile-status--author">作者</span>
            <span v-else class="profile-status profile-status--reader">读者</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="editable || isAllowedToChangeUserRole" class="profile-actions">
      <div v-if="editable" class="action-buttons">
        <button @click="showEmailDialog = true" class="action-btn">
          <q-icon name="mail_outline" size="1.1rem" />
          <span>修改邮箱</span>
        </button>
        <button @click="showPasswordDialog = true" class="action-btn">
          <q-icon name="lock_outline" size="1.1rem" />
          <span>修改密码</span>
        </button>
        <button @click="prepareAvatarDialog" class="action-btn">
          <q-icon name="image" size="1.1rem" />
          <span>修改头像</span>
        </button>
      </div>
      <div v-if="isAllowedToChangeUserRole" class="role-selector">
        <q-select
          v-model="newRole"
          :options="Object.values(RolesEnum)"
          @update:model-value="handleRoleUpdate"
          label="设置角色"
          outlined
          dense
          class="role-select"
        />
      </div>
    </div>

    <!-- Stats -->
    <div class="profile-stats">
      <div class="stat-item">
        <span class="stat-value">{{ (user as any).comments_count ?? 0 }}</span>
        <span class="stat-label">评论</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-value">{{ user.role ?? '-' }}</span>
        <span class="stat-label">角色</span>
      </div>
    </div>

    <!-- Dialogs -->
    <q-dialog v-model="showEmailDialog">
      <q-card class="dialog-card">
        <q-card-section>
          <h3 class="dialog-title">修改邮箱</h3>
          <q-input
            v-model="newEmail"
            label="新邮箱"
            outlined
            dense
            class="dialog-input"
            type="email"
          />
        </q-card-section>
        <q-card-actions align="right" class="dialog-actions">
          <q-btn label="取消" v-close-popup flat no-caps class="dialog-cancel" />
          <q-btn label="保存" @click="handleEmailUpdate" v-close-popup unelevated no-caps color="accent" class="dialog-confirm" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showPasswordDialog">
      <q-card class="dialog-card">
        <q-card-section>
          <h3 class="dialog-title">修改密码</h3>
          <q-input
            v-if="isProfile"
            v-model="oldPassword"
            label="旧密码"
            type="password"
            outlined
            dense
            class="dialog-input"
          />
          <q-input
            v-model="newPassword"
            label="新密码"
            type="password"
            outlined
            dense
            class="dialog-input"
          />
        </q-card-section>
        <q-card-actions align="right" class="dialog-actions">
          <q-btn label="取消" v-close-popup flat no-caps class="dialog-cancel" />
          <q-btn label="保存" @click="handlePasswordUpdate" v-close-popup unelevated no-caps color="accent" class="dialog-confirm" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showAvatarDialog">
      <q-card class="dialog-card">
        <q-card-section>
          <h3 class="dialog-title">选择头像</h3>
          <div class="avatar-grid">
            <button
              v-for="avatarUrl in avatarsToChoose"
              :key="avatarUrl"
              @click="handleAvatarUpdate(avatarUrl)"
              v-close-popup
              class="avatar-choice"
            >
              <img :src="avatarUrl" />
            </button>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<style scoped>
.user-profile-card {
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #f1f5f9;
  overflow: hidden;
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.profile-header {
  padding: 40px 36px 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  border: 4px solid #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.profile-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.profile-email {
  color: #64748b;
  font-size: 0.9rem;
}

.profile-status {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.profile-status--unconfirmed {
  background: #fef3c7;
  color: #d97706;
}

.profile-status--admin {
  background: #fef2f2;
  color: #ef4444;
}

.profile-status--author {
  background: #eff6ff;
  color: #2563eb;
}

.profile-status--reader {
  background: #f0fdf4;
  color: #10b981;
}

.profile-actions {
  padding: 24px 36px;
  border-top: 1px solid #f1f5f9;
}

.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.action-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #2563eb;
}

.role-selector {
  margin-top: 16px;
}

.role-select {
  max-width: 200px;
}

.role-select :deep(.q-field__control) {
  border-radius: 12px !important;
}

.profile-stats {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px 36px;
  border-top: 1px solid #f1f5f9;
  background: #fafbfc;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
}

.stat-label {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: #e2e8f0;
}

/* Dialogs */
.dialog-card {
  border-radius: 20px !important;
  padding: 8px;
  min-width: 340px;
}

.dialog-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 16px 0;
}

.dialog-input {
  margin-bottom: 8px;
}

.dialog-input :deep(.q-field__control) {
  border-radius: 12px !important;
}

.dialog-actions {
  padding: 12px 16px 8px;
}

.dialog-cancel {
  color: #64748b;
  font-weight: 500;
  border-radius: 10px;
}

.dialog-confirm {
  border-radius: 10px;
  font-weight: 600;
}

.avatar-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.avatar-choice {
  padding: 12px;
  border-radius: 16px;
  border: 2px solid #f1f5f9;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.avatar-choice:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.15);
  transform: scale(1.04);
}

.avatar-choice img {
  width: 100%;
  height: auto;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .profile-header {
    padding: 28px 24px;
  }
  
  .profile-avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-name {
    font-size: 1.3rem;
  }
  
  .profile-actions {
    padding: 20px 24px;
  }
  
  .profile-stats {
    padding: 20px 24px;
  }
  
  .action-buttons {
    justify-content: center;
  }
}
</style>
