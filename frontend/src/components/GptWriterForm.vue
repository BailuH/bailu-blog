<script setup lang="ts">
import { ref } from 'vue'
import { DefaultService } from '@/client'
import router from '@/router'

const title = ref('')
const tagsString = ref('')
const keyPhrasesString = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  const gptGeneratorResponse = await DefaultService.generateArticleGptWriterPost({
    title: title.value,
    tags: [...tagsString.value.split(',').filter(t => t.trim()), 'ChatGPT generated'],
    key_phrases: keyPhrasesString.value.split(',').map((phrase) => phrase.trim()).filter(p => p)
  }).finally(() => {
    loading.value = false
  })

  const articleId = gptGeneratorResponse.article._id
  router.push({ name: 'edit-article', params: { id: articleId } })
}
</script>

<template>
  <div class="gpt-page">
    <div class="gpt-card">
      <div class="gpt-header">
        <div class="gpt-icon">
          <q-icon name="auto_fix_high" size="2rem" color="accent" />
        </div>
        <h2 class="gpt-title">AI 写作助手</h2>
        <p class="gpt-subtitle">输入主题，让 AI 为你生成文章草稿</p>
      </div>

      <div class="gpt-info">
        <q-icon name="info" size="1rem" class="info-icon" />
        <span>生成完成后，您将被自动跳转到文章编辑页面进行修改和完善。</span>
      </div>

      <q-form class="gpt-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label class="form-label">文章标题</label>
          <q-input
            v-model="title"
            placeholder="例如：深入理解 Vue 3 组合式 API"
            outlined
            dense
            class="gpt-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">标签（用逗号分隔）</label>
          <q-input
            v-model="tagsString"
            placeholder="例如：前端, Vue, 教程"
            outlined
            dense
            class="gpt-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">关键词（用逗号分隔）</label>
          <q-input
            v-model="keyPhrasesString"
            placeholder="例如：响应式原理, 生命周期, 性能优化"
            outlined
            dense
            class="gpt-input"
          />
        </div>

        <button
          type="submit"
          class="generate-btn"
          :disabled="loading || !title.trim()"
        >
          <q-spinner-oval v-if="loading" size="1.2rem" color="white" class="q-mr-sm" />
          <q-icon v-else name="auto_fix_high" size="1.1rem" class="q-mr-sm" />
          {{ loading ? '生成中...' : '生成文章' }}
        </button>
      </q-form>
    </div>
  </div>
</template>

<style scoped>
.gpt-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 24px;
  min-height: 60vh;
}

.gpt-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #f1f5f9;
  padding: 40px 36px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 16px 48px rgba(0, 0, 0, 0.03);
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.gpt-header {
  text-align: center;
  margin-bottom: 24px;
}

.gpt-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  margin-bottom: 16px;
}

.gpt-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.gpt-subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

.gpt-info {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
}

.info-icon {
  color: #3b82f6;
  flex-shrink: 0;
  margin-top: 2px;
}

.gpt-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
}

.gpt-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
  min-height: 48px;
}

.gpt-input :deep(.q-field--focused .q-field__control) {
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
}

.generate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 28px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
  margin-top: 8px;
}

.generate-btn:hover:not(:disabled) {
  box-shadow: 0 6px 24px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .gpt-card {
    padding: 28px 24px;
    border-radius: 20px;
  }
  
  .gpt-title {
    font-size: 1.3rem;
  }
}
</style>
