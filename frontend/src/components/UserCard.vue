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
const newRole = ref<RolesEnum>()

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
    props.user._id ?? props.user.id,
    {
      avatar_url: avatarUrl
    }
  )
  Notify.create(
    '已设置头像：' + updateAvatarResponse.user.avatar_url + '。请刷新页面'
  )
}

async function prepareAvatarDialog() {
  showAvatarDialog.value = true
  await loadAvatarsToChoose()
}

async function handleEmailUpdate() {
  const updateEmailResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user._id ?? props.user.id,
    {
      email: newEmail.value
    }
  )
  Notify.create('已设置邮箱：' + updateEmailResponse.user.email + '。请刷新页面')

  if (props.isProfile) {
    AuthService.update_user_info()
  }
}

async function handlePasswordUpdate() {
  await DefaultService.updateUserPasswordUsersUserIdPasswordPut(props.user._id ?? props.user.id, {
    old_password: oldPassword.value,
    new_password: newPassword.value
  })
  Notify.create('新密码已设置！')
}

async function handleRoleUpdate() {
  await DefaultService.changeUserRoleUsersUserIdRolePut(props.user?._id ?? '', {
    role: newRole.value
  })

  Notify.create('已设置角色：' + newRole.value)
}
</script>

<template>
  <q-item v-if="user" class="row justify-start items-start q-pt-lg bg-white rounded-borders shadow-1">
    <UserInfoCard :user="user" class="col" />

    <q-item-section class="col-grow items-start" style="overflow: auto">
      <q-item-label lines="1" class="row text-h5 text-dark">
        <div class="q-mr-md">
          {{ user?.email }}
        </div>
        <div v-if="!user?.role" class="text-negative">(未确认)</div>
      </q-item-label>
      <q-item-label class="text-caption text-grey-6">
        ***用户其他信息区域***
      </q-item-label>
    </q-item-section>

    <!-- 修改数据按钮区块 -->
    <q-item-actions class="column col-shrink">
      <q-btn
        v-if="editable"
        label="修改邮箱"
        @click="showEmailDialog = true"
        class="self-stretch"
        align="left"
        flat
        no-caps
        color="dark"
      />
      <q-btn
        v-if="editable"
        label="修改密码"
        @click="showPasswordDialog = true"
        class="self-stretch"
        align="left"
        flat
        no-caps
        color="dark"
      />
      <q-btn
        v-if="editable"
        label="修改头像"
        @click="prepareAvatarDialog"
        class="self-stretch"
        align="left"
        flat
        no-caps
        color="dark"
      />
      <q-select
        v-if="isAllowedToChangeUserRole"
        v-model="newRole"
        :options="Object.values(RolesEnum)"
        @update:model-value="handleRoleUpdate"
        label="设置角色"
        class="q-mx-md"
        outlined
        dense
      />
    </q-item-actions>

    <q-dialog v-model="showEmailDialog">
      <q-card class="bg-white" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="newEmail"
            label="新邮箱"
            clearable
            :input-style="{ fontSize: '20px' }"
            outlined
            dense
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-white">
          <q-btn label="修改" @click="handleEmailUpdate" v-close-popup flat no-caps color="accent" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showPasswordDialog">
      <q-card class="bg-white" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="oldPassword"
            label="旧密码"
            v-if="isProfile"
            clearable
            :input-style="{ fontSize: '20px' }"
            outlined
            dense
            class="q-mb-md"
          />
          <q-input
            v-model="newPassword"
            label="新密码"
            clearable
            :input-style="{ fontSize: '20px' }"
            outlined
            dense
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-white">
          <q-btn label="修改" @click="handlePasswordUpdate" v-close-popup flat no-caps color="accent" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showAvatarDialog">
      <q-card class="bg-white" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <!-- 居中显示"选择头像" -->
          <div class="text-center text-h6 text-dark q-mb-md">选择头像</div>
          <q-btn
            v-for="avatarUrl in [...avatarsToChoose, ...avatarsToChoose, ...avatarsToChoose]"
            :key="avatarUrl"
            @click="handleAvatarUpdate(avatarUrl)"
            v-close-popup
            flat
          >
            <img :src="avatarUrl" style="width: 100px" />
          </q-btn>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-item>
</template>
