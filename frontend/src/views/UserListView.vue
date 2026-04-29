<script setup lang="ts">
import { DefaultService } from '@/client'
import UserList from '@/components/UserList.vue'
import { onBeforeMount, ref } from 'vue'

const totalUsers = ref(0)
const totalAuthors = ref(0)
const totalAdmins = ref(0)

onBeforeMount(async () => {
  try {
    const res = await DefaultService.listUsersUsersGet(0, 100)
    totalUsers.value = res.users.length
    totalAuthors.value = res.users.filter((u: any) => u.role === 'Author').length
    totalAdmins.value = res.users.filter((u: any) => u.role === 'Admin').length
  } catch {
    // ignore
  }
})
</script>

<template>
  <q-page class="users-page">
    <!-- Top Banner -->
    <div class="users-banner">
      <div class="users-banner-content">
        <div class="users-banner-text">
          <h1 class="users-banner-title">社区成员</h1>
          <p class="users-banner-desc">
            认识每一位为社区贡献力量的创作者与思考者
          </p>
        </div>

        <!-- [预留] 社区成员横幅插图 -->
        <div class="users-banner-visual">
          <div class="banner-placeholder">
            <q-icon name="groups" size="3rem" color="blue-3" />
            <span class="banner-placeholder-text">[预留] 社区插图</span>
            <span class="banner-placeholder-hint">建议放置多人协作/社区主题插图</span>
          </div>
        </div>
      </div>

      <!-- Stats Bar -->
      <div class="users-stats">
        <div class="users-stat">
          <div class="users-stat-icon-wrapper users-stat-icon--total">
            <q-icon name="people" size="1.3rem" />
          </div>
          <div class="users-stat-info">
            <span class="users-stat-value">{{ totalUsers }}</span>
            <span class="users-stat-label">总用户</span>
          </div>
        </div>
        <div class="users-stat-divider"></div>
        <div class="users-stat">
          <div class="users-stat-icon-wrapper users-stat-icon--author">
            <q-icon name="edit_note" size="1.3rem" />
          </div>
          <div class="users-stat-info">
            <span class="users-stat-value">{{ totalAuthors }}</span>
            <span class="users-stat-label">作者</span>
          </div>
        </div>
        <div class="users-stat-divider"></div>
        <div class="users-stat">
          <div class="users-stat-icon-wrapper users-stat-icon--admin">
            <q-icon name="shield" size="1.3rem" />
          </div>
          <div class="users-stat-info">
            <span class="users-stat-value">{{ totalAdmins }}</span>
            <span class="users-stat-label">管理员</span>
          </div>
        </div>
      </div>
    </div>

    <!-- User List Component -->
    <UserList />
  </q-page>
</template>

<style scoped>
.users-page {
  padding: 8px 0 48px;
}

/* ===== Banner ===== */
.users-banner {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #eff6ff 100%);
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  padding: 36px;
  margin-bottom: 32px;
  overflow: hidden;
  position: relative;
}

.users-banner::before {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.users-banner-content {
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 32px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.users-banner-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.users-banner-desc {
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
  max-width: 400px;
}

/* Banner Visual */
.users-banner-visual {
  display: flex;
  justify-content: center;
}

.banner-placeholder {
  width: 100%;
  aspect-ratio: 1;
  max-height: 200px;
  border-radius: 20px;
  border: 2px dashed #dbeafe;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #94a3b8;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.06);
}

.banner-placeholder-text {
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
}

.banner-placeholder-hint {
  font-size: 0.72rem;
  color: #94a3b8;
}

/* ===== Stats ===== */
.users-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid #e2e8f0;
}

.users-stat {
  display: flex;
  align-items: center;
  gap: 12px;
}

.users-stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.users-stat-icon--total {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.users-stat-icon--author {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.users-stat-icon--admin {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
}

.users-stat-info {
  display: flex;
  flex-direction: column;
}

.users-stat-value {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
}

.users-stat-label {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 500;
  margin-top: 2px;
}

.users-stat-divider {
  width: 1px;
  height: 40px;
  background: #e2e8f0;
}

@media (max-width: 768px) {
  .users-banner {
    padding: 24px;
  }

  .users-banner-content {
    grid-template-columns: 1fr;
  }

  .users-banner-visual {
    display: none;
  }

  .users-banner-title {
    font-size: 1.5rem;
  }

  .users-stats {
    gap: 16px;
    flex-wrap: wrap;
  }

  .users-stat-divider {
    display: none;
  }
}
</style>
