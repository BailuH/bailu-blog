<script setup lang="ts">
import AuthLoginForm from '@/components/AuthLoginForm.vue'
</script>

<template>
  <q-page class="auth-page">
    <div class="auth-layout">
      <!-- Left: Brand Section -->
      <div class="auth-brand">
        <div class="auth-brand-content">
          <q-avatar size="64px" class="auth-brand-logo">
            <img src="../../images/eye-red.png" />
          </q-avatar>
          <h1 class="auth-brand-title">
            我的博客
          </h1>
          <p class="auth-brand-desc">
            一个专注于技术分享与思想交流的空间。
            登录后，你可以创作文章、参与讨论、与作者们互动。
          </p>

          <!-- [预留] 品牌插图区域 -->
          <div class="auth-brand-illustration">
            <div class="illustration-placeholder">
              <q-icon name="draw" size="3rem" color="blue-3" />
              <span class="illustration-text">[预留] 品牌插图</span>
              <span class="illustration-hint">建议放置与写作/技术相关的插图</span>
            </div>
          </div>

          <div class="auth-brand-features">
            <div class="brand-feature">
              <q-icon name="edit_note" size="1.2rem" color="blue-5" />
              <span>自由创作</span>
            </div>
            <div class="brand-feature">
              <q-icon name="chat" size="1.2rem" color="blue-5" />
              <span>深度讨论</span>
            </div>
            <div class="brand-feature">
              <q-icon name="share" size="1.2rem" color="blue-5" />
              <span>知识分享</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Form Section -->
      <div class="auth-form-section">
        <AuthLoginForm />
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.auth-page {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
}

.auth-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  gap: 48px;
  padding: 24px;
  align-items: center;
}

/* ===== Brand Section ===== */
.auth-brand {
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-brand-content {
  max-width: 400px;
}

.auth-brand-logo {
  margin-bottom: 24px;
  border: 4px solid #f1f5f9;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.auth-brand-logo:hover {
  transform: scale(1.05) rotate(-3deg);
}

.auth-brand-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.auth-brand-desc {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.7;
  margin: 0 0 28px 0;
}

/* Illustration Placeholder */
.auth-brand-illustration {
  margin-bottom: 28px;
}

.illustration-placeholder {
  width: 100%;
  aspect-ratio: 4 / 3;
  max-height: 240px;
  border-radius: 20px;
  border: 2px dashed #e2e8f0;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #94a3b8;
}

.illustration-text {
  font-size: 0.88rem;
  font-weight: 600;
  color: #64748b;
}

.illustration-hint {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Features */
.auth-brand-features {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.brand-feature {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  color: #475569;
  font-size: 0.85rem;
  font-weight: 500;
}

/* ===== Form Section ===== */
.auth-form-section {
  display: flex;
  justify-content: center;
}

.auth-form-section :deep(.auth-card) {
  max-width: none;
  width: 100%;
}

@media (max-width: 900px) {
  .auth-layout {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .auth-brand {
    order: 2;
  }

  .auth-form-section {
    order: 1;
  }

  .auth-brand-illustration {
    display: none;
  }

  .auth-brand-title {
    font-size: 1.6rem;
  }

  .auth-brand-content {
    text-align: center;
  }

  .auth-brand-features {
    justify-content: center;
  }
}
</style>
