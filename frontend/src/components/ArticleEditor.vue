<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse } from '@/client'
import router from '@/router'
import { Notify } from 'quasar'
import { ref } from 'vue'
import { MdEditor } from 'md-editor-v3'

export interface Props {
  articleToEdit?: ArticleDocumentResponse
  createMode?: boolean
  editMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  createMode: () => false,
  editMode: () => false
})

const titleRef = ref<string>(
  props.articleToEdit?.title ? props.articleToEdit.title : ''
)
const conentRef = ref<string>(
  props.articleToEdit?.content ? props.articleToEdit.content : ''
)
const tagsRef = ref<string[]>(
  props.articleToEdit?.tags ? props.articleToEdit.tags : []
)
const previewImageURLRef = ref<string | null>(props.articleToEdit?.preview_image_url ?? null)
const newTag = ref<string>('')

const articleDeleteDialog = ref<boolean>(false)
const previewImageDialog = ref<boolean>(false)

async function handleArticleSave() {
  if (props.createMode) {
    const createArticleResponse = await DefaultService.createArticleArticlesPost({
      title: titleRef.value,
      content: conentRef.value,
      tags: tagsRef.value,
      preview_image_url: previewImageURLRef.value
    })
    Notify.create('新文章已创建，正在跳转')
    router.push('/article/' + createArticleResponse.article._id)
  } else if (props.editMode) {
    const updateArticleResponse = await DefaultService.updateArticleArticlesArticleIdPut(
      props.articleToEdit?._id ?? '',
      {
        title: titleRef.value,
        content: conentRef.value,
        tags: tagsRef.value,
        preview_image_url: previewImageURLRef.value
      }
    )
    Notify.create('文章更新成功，正在跳转')
    router.push('/article/' + updateArticleResponse.article._id)
  }
}

function getDefaultPreviewImages() {
  return [
    'https://as1.ftcdn.net/v2/jpg/02/90/89/76/1000_F_290897614_7RdAsk2GmumcGWZ2qklmV74hKlNmznSx.jpg',
    'https://as2.ftcdn.net/v2/jpg/01/70/93/27/1000_F_170932733_VOHGeaH5AjrVCXBVryEwVgwhArv2wNNH.jpg',
    'https://as1.ftcdn.net/v2/jpg/05/35/47/38/1000_F_535473874_OWCa2ohzXXNZgqnlzF9QETsnbrSO9pFS.jpg',
    'https://as2.ftcdn.net/v2/jpg/02/90/89/76/1000_F_290897614_7RdAsk2GmumcGWZ2qklmV74hKlNmznSx.jpg',
    'https://as1.ftcdn.net/v2/jpg/05/48/56/38/1000_F_548563894_s5tGFJjPhc7lp5uG4iJkR77QbgvrKr9e.jpg'
  ]
}

async function handleArticleDelete() {
  await DefaultService.deleteArticleArticlesArticleIdDelete(props.articleToEdit?._id!)
  Notify.create('文章已删除')
  router.push('/')
}

function handleAddTag() {
  if (newTag.value && !tagsRef.value.includes(newTag.value)) {
    tagsRef.value.push(newTag.value)
    newTag.value = ''
  }
}

function handleRemoveTag(tag: string) {
  const idx = tagsRef.value.indexOf(tag)
  if (idx > -1) tagsRef.value.splice(idx, 1)
}
</script>

<template>
  <div class="editor-page">
    <div class="editor-card">
      <!-- Title -->
      <div class="form-section">
        <label class="section-label">文章标题</label>
        <q-input
          v-model="titleRef"
          placeholder="输入一个引人注目的标题..."
          outlined
          dense
          class="title-input"
        />
      </div>

      <!-- Content -->
      <div class="form-section">
        <label class="section-label">正文内容</label>
        <MdEditor
          v-model="conentRef"
          language="zh-CN"
          placeholder="开始写作..."
          class="content-editor"
        />
      </div>

      <!-- Preview Image -->
      <div class="form-section">
        <label class="section-label">封面图片</label>
        <div class="preview-image-section">
          <q-input
            v-model="previewImageURLRef"
            placeholder="图片链接地址"
            outlined
            dense
            class="image-url-input"
          />
          <button
            @click="previewImageDialog = true"
            class="gallery-btn"
          >
            <q-icon name="collections" size="1.1rem" />
            图库
          </button>
        </div>
        <div v-if="previewImageURLRef" class="preview-image-container">
          <img :src="previewImageURLRef" class="preview-image" />
        </div>
      </div>

      <!-- Tags -->
      <div class="form-section">
        <label class="section-label">标签</label>
        <div class="tags-section">
          <div class="tags-list">
            <span
              v-for="tag in tagsRef"
              :key="tag"
              class="tag-chip"
            >
              {{ tag }}
              <button @click="handleRemoveTag(tag)" class="tag-remove">
                <q-icon name="close" size="0.75rem" />
              </button>
            </span>
          </div>
          <div class="tag-add-row">
            <q-input
              v-model="newTag"
              placeholder="添加标签"
              outlined
              dense
              class="tag-input"
              @keyup.enter="handleAddTag"
            />
            <button @click="handleAddTag" class="add-tag-btn">
              <q-icon name="add" size="1rem" />
            </button>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="editor-actions">
        <button @click="handleArticleSave" class="save-btn">
          <q-icon name="save" size="1.1rem" />
          {{ createMode ? '发布文章' : '保存修改' }}
        </button>
        <button
          v-if="editMode"
          @click="articleDeleteDialog = true"
          class="delete-btn"
        >
          <q-icon name="delete_outline" size="1.1rem" />
          删除文章
        </button>
      </div>
    </div>

    <!-- Delete dialog -->
    <q-dialog v-model="articleDeleteDialog">
      <q-card class="dialog-card">
        <q-card-section class="dialog-body">
          <div class="dialog-icon">
            <q-icon name="warning_amber" size="2.5rem" color="warning" />
          </div>
          <h3 class="dialog-title">确认删除？</h3>
          <p class="dialog-desc">
            删除后文章将无法恢复，此操作不可撤销。
          </p>
        </q-card-section>
        <q-card-actions class="dialog-actions">
          <button @click="articleDeleteDialog = false" class="dialog-btn dialog-btn--cancel">
            取消
          </button>
          <button @click="handleArticleDelete" class="dialog-btn dialog-btn--danger">
            确认删除
          </button>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Image gallery dialog -->
    <q-dialog v-model="previewImageDialog">
      <q-card class="dialog-card">
        <q-card-section>
          <h3 class="dialog-title">选择封面图片</h3>
          <div class="image-grid">
            <button
              v-for="imageUrl in getDefaultPreviewImages()"
              :key="imageUrl"
              @click="previewImageURLRef = imageUrl; previewImageDialog = false"
              class="image-choice"
            >
              <img :src="imageUrl" />
            </button>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<style scoped>
.editor-page {
  padding: 8px 0 40px;
  animation: fadeInUp 0.4s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.editor-header {
  margin-bottom: 28px;
}

.editor-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.editor-subtitle {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0;
}

.editor-card {
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #f1f5f9;
  padding: 32px;
}

.form-section {
  margin-bottom: 28px;
}

.form-section:last-of-type {
  margin-bottom: 0;
}

.section-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.title-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
  min-height: 52px;
  font-size: 1.05rem;
}

.title-input :deep(.q-field--focused .q-field__control) {
  background: #ffffff;
}

.content-editor {
  border-radius: 12px;
  overflow: hidden;
}

.content-editor :deep(.md-editor) {
  border-radius: 12px !important;
  border: 1px solid #e2e8f0 !important;
}

/* Preview image */
.preview-image-section {
  display: flex;
  gap: 10px;
}

.image-url-input {
  flex: 1;
}

.image-url-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
}

.gallery-btn {
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
  white-space: nowrap;
}

.gallery-btn:hover {
  background: #f8fafc;
  border-color: #2563eb;
  color: #2563eb;
}

.preview-image-container {
  margin-top: 16px;
  border-radius: 12px;
  overflow: hidden;
  max-height: 200px;
}

.preview-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
}

/* Tags */
.tags-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 10px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 0.85rem;
  font-weight: 500;
}

.tag-remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: none;
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.tag-remove:hover {
  background: #2563eb;
  color: #ffffff;
}

.tag-add-row {
  display: flex;
  gap: 8px;
}

.tag-input {
  max-width: 200px;
}

.tag-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #f8fafc;
}

.add-tag-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.add-tag-btn:hover {
  background: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
}

/* Actions */
.editor-actions {
  display: flex;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
  margin-top: 8px;
}

.save-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 12px;
  border: none;
  background: #2563eb;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.save-btn:hover {
  background: #1d4ed8;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.delete-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 12px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #ef4444;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.delete-btn:hover {
  background: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
}

/* Dialogs */
.dialog-card {
  border-radius: 20px !important;
  padding: 8px;
  min-width: 360px;
}

.dialog-body {
  text-align: center;
  padding: 24px 20px 16px;
}

.dialog-icon {
  margin-bottom: 12px;
}

.dialog-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.dialog-desc {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}

.dialog-actions {
  display: flex;
  gap: 10px;
  padding: 12px 20px 16px;
  justify-content: center;
}

.dialog-btn {
  padding: 10px 24px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  border: none;
}

.dialog-btn--cancel {
  background: #f1f5f9;
  color: #475569;
}

.dialog-btn--cancel:hover {
  background: #e2e8f0;
}

.dialog-btn--danger {
  background: #ef4444;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}

.dialog-btn--danger:hover {
  background: #dc2626;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 8px;
}

.image-choice {
  padding: 8px;
  border-radius: 12px;
  border: 2px solid #f1f5f9;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
}

.image-choice:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.12);
  transform: scale(1.03);
}

.image-choice img {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .editor-card {
    padding: 20px;
    border-radius: 16px;
  }
  
  .editor-title {
    font-size: 1.4rem;
  }
  
  .editor-actions {
    flex-direction: column;
  }
  
  .save-btn,
  .delete-btn {
    width: 100%;
    justify-content: center;
  }
  
  .preview-image-section {
    flex-direction: column;
  }
  
  .tag-input {
    max-width: none;
  }
  
  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
