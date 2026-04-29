<script setup lang="ts">
import { type ArticleDocumentResponse, DefaultService } from '@/client'
import ArticleEditor from '@/components/ArticleEditor.vue'
import { onBeforeMount, ref } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

const createMode = ref<boolean>(false)
const editMode = ref<boolean>(false)
const article = ref<ArticleDocumentResponse>()

const route = useRoute()

async function resolveView() {
  if (route.path == '/create-article') {
    createMode.value = true
  } else {
    const articleResponse = await DefaultService.readArticleArticlesArticleIdGet(
      route.params.id.toString()
    )
    article.value = articleResponse.article
    editMode.value = true
  }
}

onBeforeMount(() => {
  resolveView()
})

onBeforeRouteUpdate(() => {
  resolveView()
})
</script>

<template>
  <q-page class="editor-page">
    <!-- Top Banner -->
    <div class="editor-banner">
      <div class="editor-banner-content">
        <div class="editor-banner-icon">
          <q-icon :name="createMode ? 'edit_note' : 'edit'" size="1.5rem" color="white" />
        </div>
        <div class="editor-banner-text">
          <h1 class="editor-banner-title">
            {{ createMode ? '创作新文章' : '编辑文章' }}
          </h1>
          <p class="editor-banner-desc">
            {{ createMode ? '从灵感开始，记录你的每一个想法' : '打磨文字，让表达更加精准有力' }}
          </p>
        </div>
      </div>
      <!-- Steps indicator -->
      <div class="editor-steps">
        <div class="step step--active">
          <div class="step-num">1</div>
          <span class="step-label">撰写内容</span>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'step--active': !createMode }">
          <div class="step-num">2</div>
          <span class="step-label">设置封面</span>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'step--active': !createMode }">
          <div class="step-num">3</div>
          <span class="step-label">添加标签</span>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'step--active': !createMode }">
          <div class="step-num">4</div>
          <span class="step-label">发布</span>
        </div>
      </div>
    </div>

    <!-- [预留] 编辑器顶部横幅图片位 -->
    <div class="editor-image-banner">
      <div class="editor-image-placeholder">
        <q-icon name="panorama" size="2rem" color="blue-3" />
        <span class="editor-image-placeholder-text">[预留] 编辑器顶部横幅图片</span>
        <span class="editor-image-placeholder-hint">建议尺寸 1200×180，可为空</span>
      </div>
    </div>

    <!-- Editor Component -->
    <div class="editor-body">
      <ArticleEditor v-if="createMode" create-mode />
      <ArticleEditor v-if="editMode" edit-mode :article-to-edit="article" />
    </div>
  </q-page>
</template>

<style scoped>
.editor-page {
  padding: 8px 0 48px;
}

/* ===== Banner ===== */
.editor-banner {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  border-radius: 24px;
  padding: 32px 36px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  position: relative;
  overflow: hidden;
}

.editor-banner::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.15) 0%, transparent 60%);
  pointer-events: none;
}

.editor-banner-content {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.editor-banner-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(37, 99, 235, 0.2);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.editor-banner-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 4px 0;
}

.editor-banner-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin: 0;
}

/* Steps */
.editor-steps {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.step-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.step--active .step-num {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

.step-label {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
  white-space: nowrap;
}

.step--active .step-label {
  color: rgba(255, 255, 255, 0.85);
}

.step-connector {
  width: 24px;
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1px;
}

/* ===== Image Banner ===== */
.editor-image-banner {
  margin-bottom: 24px;
}

.editor-image-placeholder {
  width: 100%;
  height: 120px;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #94a3b8;
}

.editor-image-placeholder-text {
  font-size: 0.88rem;
  font-weight: 600;
  color: #64748b;
}

.editor-image-placeholder-hint {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* ===== Editor Body ===== */
.editor-body {
  /* ArticleEditor has its own card styling */
}

@media (max-width: 768px) {
  .editor-banner {
    flex-direction: column;
    align-items: flex-start;
    padding: 24px;
  }

  .editor-steps {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .editor-banner-title {
    font-size: 1.25rem;
  }
}
</style>
