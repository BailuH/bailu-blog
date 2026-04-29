<script setup lang="ts">
import GptWriterForm from '@/components/GptWriterForm.vue'
</script>

<template>
  <q-page class="gpt-page">
    <!-- Top Banner -->
    <div class="gpt-banner">
      <div class="gpt-banner-left">
        <div class="gpt-banner-icon">
          <q-icon name="auto_fix_high" size="2rem" color="white" />
        </div>
        <div class="gpt-banner-text">
          <h1 class="gpt-banner-title">AI 写作助手</h1>
          <p class="gpt-banner-desc">
            基于 GPT 技术，根据你的主题快速生成文章草稿。
            让创作从灵感开始，而非空白页面。
          </p>
        </div>
      </div>

      <!-- [预留] AI 助手插图 -->
      <div class="gpt-banner-visual">
        <div class="gpt-visual-placeholder">
          <q-icon name="smart_toy" size="3rem" color="blue-3" />
          <span class="gpt-visual-text">[预留] AI 助手插图</span>
          <span class="gpt-visual-hint">建议放置与 AI/写作相关的插图</span>
        </div>
      </div>
    </div>

    <!-- Features Grid -->
    <div class="gpt-features">
      <div class="gpt-feature">
        <div class="gpt-feature-icon">
          <q-icon name="bolt" size="1.3rem" color="blue-6" />
        </div>
        <h3 class="gpt-feature-title">快速生成</h3>
        <p class="gpt-feature-desc">输入主题，数秒即可获取完整文章草稿</p>
      </div>
      <div class="gpt-feature">
        <div class="gpt-feature-icon">
          <q-icon name="tune" size="1.3rem" color="green-6" />
        </div>
        <h3 class="gpt-feature-title">灵活定制</h3>
        <p class="gpt-feature-desc">自由添加标签与关键词，精准控制内容方向</p>
      </div>
      <div class="gpt-feature">
        <div class="gpt-feature-icon">
          <q-icon name="edit" size="1.3rem" color="orange-6" />
        </div>
        <h3 class="gpt-feature-title">一键编辑</h3>
        <p class="gpt-feature-desc">生成后直接进入编辑器，随时修改完善</p>
      </div>
    </div>

    <!-- Form -->
    <GptWriterForm />
  </q-page>
</template>

<style scoped>
.gpt-page {
  padding: 8px 0 48px;
}

/* ===== Banner ===== */
.gpt-banner {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 32px;
  align-items: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  border-radius: 24px;
  padding: 36px 40px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
}

.gpt-banner::before {
  content: '';
  position: absolute;
  top: -40%;
  right: -5%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.12) 0%, transparent 60%);
  pointer-events: none;
}

.gpt-banner-left {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.gpt-banner-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
  flex-shrink: 0;
}

.gpt-banner-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 6px 0;
}

.gpt-banner-desc {
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
  max-width: 420px;
}

/* Banner Visual */
.gpt-banner-visual {
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.gpt-visual-placeholder {
  width: 100%;
  aspect-ratio: 1;
  max-height: 180px;
  border-radius: 20px;
  border: 2px dashed rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.3);
}

.gpt-visual-text {
  font-size: 0.82rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
}

.gpt-visual-hint {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.3);
}

/* ===== Features ===== */
.gpt-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.gpt-feature {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  padding: 24px;
  text-align: center;
  transition: all 0.25s ease;
}

.gpt-feature:hover {
  border-color: #e2e8f0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.gpt-feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #f8fafc;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

.gpt-feature-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.gpt-feature-desc {
  color: #94a3b8;
  font-size: 0.82rem;
  line-height: 1.5;
  margin: 0;
}

@media (max-width: 768px) {
  .gpt-banner {
    grid-template-columns: 1fr;
    padding: 28px 24px;
  }

  .gpt-banner-visual {
    display: none;
  }

  .gpt-banner-title {
    font-size: 1.3rem;
  }

  .gpt-features {
    grid-template-columns: 1fr;
  }
}
</style>
