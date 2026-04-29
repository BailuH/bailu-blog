<script setup lang="ts">
import { type ArticleDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { useUserStore } from '@/stores/UserStore'
import moment from 'moment'
import { computed, onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'
import { MdPreview } from 'md-editor-v3'

const props = defineProps<{
  article: ArticleDocumentResponse | undefined
}>()

const route = useRoute()

const formattedDate = ref<string>(moment(props.article?.created_at).format('YYYY年M月D日'))
const isAllowedToEdit = ref<boolean>(false)

const editLink = computed(() => {
  return route.path + '/edit'
})

onBeforeMount(async () => {
  const currentUser = useUserStore().user
  if (currentUser?.role == 'Admin' || props.article?.author?._id == currentUser?._id) {
    isAllowedToEdit.value = true
  }
})
</script>

<template>
  <div class="article-detail">
    <!-- Hero section with cover image -->
    <div
      v-if="article?.preview_image_url"
      class="article-hero"
      :style="{ backgroundImage: 'url(' + article?.preview_image_url + ')' }"
    >
      <div class="article-hero-overlay">
        <div class="article-hero-content">
          <div class="article-hero-meta">
            <router-link
              :to="{ name: 'user', params: { id: article?.author?._id } }"
              class="article-hero-author"
            >
              <q-avatar size="36px" class="q-mr-sm">
                <img :src="article?.author?.avatar_url || '/favicon.ico'" />
              </q-avatar>
              <span>{{ article?.author?.username }}</span>
            </router-link>
            <span class="article-hero-date">{{ formattedDate }}</span>
          </div>
          <h1 class="article-hero-title">{{ article?.title }}</h1>
          <div v-if="article?.tags" class="article-hero-tags">
            <router-link
              v-for="tag in article?.tags"
              :key="tag"
              :to="{ name: 'home', query: { tag: tag } }"
            >
              <span class="hero-tag">{{ tag }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Title section without cover image -->
    <div v-else class="article-header-no-image">
      <div class="article-header-meta">
        <router-link
          :to="{ name: 'user', params: { id: article?.author?._id } }"
          class="article-header-author"
        >
          <q-avatar size="40px" class="q-mr-sm">
            <img :src="article?.author?.avatar_url || '/favicon.ico'" />
          </q-avatar>
          <span>{{ article?.author?.username }}</span>
        </router-link>
        <span class="article-header-date">{{ formattedDate }}</span>
      </div>
      <h1 class="article-header-title">{{ article?.title }}</h1>
      <div v-if="article?.tags" class="article-header-tags">
        <router-link
          v-for="tag in article?.tags"
          :key="tag"
          :to="{ name: 'home', query: { tag: tag } }"
        >
          <span class="header-tag">{{ tag }}</span>
        </router-link>
      </div>
    </div>

    <!-- Article content -->
    <div class="article-content-card">
      <MdPreview :modelValue="article?.content || ''" language="zh-CN" />

      <div v-if="isAllowedToEdit" class="article-edit-bar">
        <q-btn
          :to="editLink"
          flat
          no-caps
          class="edit-btn"
          icon="edit"
          label="编辑文章"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-detail {
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.article-hero {
  position: relative;
  width: 100%;
  height: 420px;
  border-radius: 24px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
  margin-bottom: 32px;
}

.article-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.9) 0%, rgba(15, 23, 42, 0.3) 50%, rgba(15, 23, 42, 0.1) 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 40px;
}

.article-hero-content {
  max-width: 720px;
}

.article-hero-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.article-hero-author {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.article-hero-author:hover {
  color: #93c5fd;
}

.article-hero-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
}

.article-hero-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.2;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}

.article-hero-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.hero-tag {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.hero-tag:hover {
  background: #2563eb;
  color: #ffffff;
}

/* Header without image */
.article-header-no-image {
  padding: 40px 0 32px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 32px;
}

.article-header-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.article-header-author {
  display: flex;
  align-items: center;
  color: #475569;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.article-header-author:hover {
  color: #2563eb;
}

.article-header-date {
  color: #94a3b8;
  font-size: 0.85rem;
}

.article-header-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.25;
  margin: 0 0 16px 0;
}

.article-header-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.header-tag {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.header-tag:hover {
  background: #2563eb;
  color: #ffffff;
}

/* Content card */
.article-content-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px;
  border: 1px solid #f1f5f9;
}

.article-content-card :deep(.md-editor) {
  border: none !important;
  background: transparent !important;
}

.article-content-card :deep(.md-editor .md-editor-preview-wrapper) {
  padding: 0 !important;
}

.article-content-card :deep(.md-editor h1),
.article-content-card :deep(.md-editor h2),
.article-content-card :deep(.md-editor h3) {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  color: #0f172a;
  margin-top: 2em;
  margin-bottom: 0.8em;
}

.article-content-card :deep(.md-editor p) {
  color: #475569;
  line-height: 1.85;
  margin-bottom: 1.2em;
}

.article-content-card :deep(.md-editor code) {
  background: #f8fafc;
  color: #2563eb;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.article-content-card :deep(.md-editor pre) {
  background: #0f172a;
  border-radius: 12px;
  padding: 20px;
  overflow-x: auto;
}

.article-content-card :deep(.md-editor pre code) {
  background: transparent;
  color: #e2e8f0;
  padding: 0;
}

.article-content-card :deep(.md-editor img) {
  border-radius: 12px;
  max-width: 100%;
}

.article-edit-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
}

.edit-btn {
  color: #2563eb;
  font-weight: 500;
  border-radius: 10px;
  padding: 8px 20px;
  transition: all 0.2s ease;
}

.edit-btn:hover {
  background: rgba(37, 99, 235, 0.06);
}

@media (max-width: 768px) {
  .article-hero {
    height: 300px;
    border-radius: 16px;
  }
  
  .article-hero-overlay {
    padding: 24px;
  }
  
  .article-hero-title {
    font-size: 1.6rem;
  }
  
  .article-header-no-image {
    padding: 24px 0 20px;
  }
  
  .article-header-title {
    font-size: 1.5rem;
  }
  
  .article-content-card {
    padding: 24px;
    border-radius: 16px;
  }
}
</style>
