<script setup lang="ts">
import { type ArticleDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { ref } from 'vue'
import { onBeforeMount } from 'vue'
import { DefaultService } from '@/client'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import moment from 'moment'
import { MdPreview } from 'md-editor-v3'

const route = useRoute()

const articles = ref<ArticleDocumentResponse[]>([])
const searchText = ref('')
const freezedSearchText = ref('')
const limit = ref<number>(10)
const skip = ref<number>(0)
const page = ref<number>(1)
const maxPage = ref<number>(10)
const total = ref<number>(0)
const searchByTags = ref<boolean>(false)

const loadMoreArticles = async () => {
  console.debug('加载文章', skip.value, limit.value)
  const searchInput = freezedSearchText.value.length > 0 ? freezedSearchText.value : undefined

  const articlesResponse = await DefaultService.listArticlesArticlesGet(
    skip.value,
    limit.value,
    undefined,
    undefined,
    searchByTags.value ? searchInput : undefined,
    !searchByTags.value ? searchInput : undefined
  )
  articles.value = articlesResponse.articles
  total.value = articlesResponse.total
  maxPage.value = Math.ceil(total.value / limit.value)
}

const handleSearchbarSubmit = async () => {
  console.debug('提交搜索关键词', searchText.value)
  articles.value = []
  skip.value = 0
  freezedSearchText.value = searchText.value
  loadMoreArticles()
}

const handleSearchbarClear = () => {
  console.debug('重置搜索')
  searchText.value = ''
  freezedSearchText.value = ''
  loadMoreArticles()
}

const handlePageChange = async () => {
  if (!page.value) {
    page.value = 1
    return
  }
  console.debug('切换页面至 ', page.value)
  skip.value = (page.value - 1) * limit.value
  await loadMoreArticles()
  window.scrollTo(0, 0)
}

onBeforeMount(async () => {
  if (route.query.tag) {
    console.debug('组件挂载，带有标签', route.query.tag)
    searchByTags.value = true
    searchText.value = route.query.tag as string
    await handleSearchbarSubmit()
  } else {
    console.debug('组件挂载，无标签')
    await loadMoreArticles()
  }
})

onBeforeRouteUpdate(async (to, from) => {
  window.scrollTo(0, 0)
  articles.value = []
  skip.value = 0

  if (to.query.tag) {
    console.debug('组件更新，带有标签', to.query.tag)
    searchByTags.value = true
    searchText.value = to.query.tag as string
    freezedSearchText.value = searchText.value
    await handleSearchbarSubmit()
  } else {
    console.debug('组件更新，无标签')
    searchByTags.value = false
    searchText.value = ''
    freezedSearchText.value = ''
    await loadMoreArticles()
  }
})
</script>

<template>
  <div class="column q-py-lg">
    <!-- Header & Search -->
    <div class="search-section q-mb-xl">
      <div class="search-input-wrapper">
        <q-input
          v-model="searchText"
          @keyup.enter="handleSearchbarSubmit"
          placeholder="搜索文章..."
          class="search-input"
          outlined
          dense
          bg-color="white"
        >
          <template v-slot:prepend>
            <q-icon name="search" class="search-icon" />
          </template>
          <template v-slot:append>
            <q-icon
              v-if="searchText"
              name="close"
              @click="handleSearchbarClear"
              class="cursor-pointer clear-icon"
            />
            <q-btn
              @click="handleSearchbarSubmit"
              unelevated
              color="accent"
              size="sm"
              class="search-btn"
              icon="arrow_forward"
              round
            />
          </template>
        </q-input>
        <div class="search-options row items-center q-mt-sm">
          <q-checkbox
            v-model="searchByTags"
            label="按标签搜索"
            class="tag-checkbox"
            @update:model-value="handleSearchbarSubmit"
            dense
          />
          <div v-if="freezedSearchText.length > 0" class="search-info row items-center q-ml-md">
            <q-chip size="sm" color="accent" text-color="white" class="q-mr-sm">
              {{ freezedSearchText }}
            </q-chip>
            <span class="text-caption text-grey-6">找到 {{ total }} 篇文章</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Articles -->
    <div class="articles-list">
      <div
        v-for="article in articles"
        :key="article._id ?? ''"
        class="article-item"
      >
        <!-- With preview image -->
        <div v-if="article.preview_image_url" class="article-card article-card--featured">
          <div class="article-image-wrapper">
            <img
              :src="article.preview_image_url"
              :alt="article.title ?? ''"
              class="article-image"
            />
            <div class="article-image-overlay">
              <div class="article-meta-overlay">
                <span class="article-date">{{ moment(article?.created_at).format('YYYY年M月D日') }}</span>
                <div v-if="article?.tags" class="article-tags-overlay">
                  <router-link
                    v-for="tag in article?.tags"
                    :key="tag"
                    :to="{ name: 'home', query: { tag: tag } }"
                  >
                    <span class="tag-pill">{{ tag }}</span>
                  </router-link>
                </div>
              </div>
              <h2 class="article-title-overlay">
                <router-link :to="'/article/' + article._id">
                  {{ article.title }}
                </router-link>
              </h2>
            </div>
          </div>
          <div class="article-body">
            <div class="article-preview">
              <MdPreview :modelValue="article.content || ''" language="zh-CN" />
            </div>
            <div class="article-footer">
              <router-link
                :to="{ name: 'user', params: { id: article.author?._id } }"
                class="article-author"
              >
                <q-avatar size="28px" class="q-mr-sm">
                  <img :src="article.author?.avatar_url || '/favicon.ico'" />
                </q-avatar>
                <span>{{ article.author?.username }}</span>
              </router-link>
              <router-link :to="'/article/' + article._id" class="read-more">
                阅读全文 <span class="arrow">&rarr;</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Without preview image -->
        <div v-else class="article-card article-card--simple">
          <div class="article-simple-content">
            <div class="article-simple-header">
              <div class="article-simple-left">
                <h2 class="article-title">
                  <router-link :to="'/article/' + article._id">
                    {{ article.title }}
                  </router-link>
                </h2>
                <div class="article-simple-meta">
                  <span class="article-date">{{ moment(article?.created_at).format('YYYY年M月D日') }}</span>
                  <div v-if="article?.tags" class="article-tags">
                    <router-link
                      v-for="tag in article?.tags"
                      :key="tag"
                      :to="{ name: 'home', query: { tag: tag } }"
                    >
                      <span class="tag-pill">{{ tag }}</span>
                    </router-link>
                  </div>
                </div>
              </div>
              <router-link
                :to="{ name: 'user', params: { id: article.author?._id } }"
                class="article-author-simple"
              >
                <q-avatar size="40px">
                  <img :src="article.author?.avatar_url || '/favicon.ico'" />
                </q-avatar>
              </router-link>
            </div>
            <div class="article-preview">
              <MdPreview :modelValue="article.content || ''" language="zh-CN" />
            </div>
            <div class="article-footer">
              <router-link :to="'/article/' + article._id" class="read-more">
                阅读全文 <span class="arrow">&rarr;</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination-wrapper q-mt-xl">
      <q-pagination
        v-model="page"
        @update:model-value="handlePageChange"
        input
        :max="maxPage"
        class="pagination"
        color="accent"
        text-color="dark"
        active-design="unelevated"
        active-color="accent"
        active-text-color="white"
      />
    </div>
  </div>
</template>

<style scoped>
.search-section {
  display: flex;
  justify-content: center;
}

.search-input-wrapper {
  width: 100%;
  max-width: 560px;
}

.search-input :deep(.q-field__control) {
  border-radius: 14px !important;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  padding: 4px 8px 4px 16px;
  min-height: 52px;
  transition: all 0.2s ease;
}

.search-input :deep(.q-field__control:hover) {
  border-color: #cbd5e1;
}

.search-input :deep(.q-field--focused .q-field__control) {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.08);
}

.search-icon {
  color: #94a3b8;
  font-size: 1.25rem;
}

.clear-icon {
  color: #cbd5e1;
  font-size: 1.1rem;
  margin-right: 4px;
}

.clear-icon:hover {
  color: #94a3b8;
}

.search-btn {
  width: 36px;
  height: 36px;
  min-height: 36px;
}

.tag-checkbox :deep(.q-checkbox__label) {
  color: #64748b;
  font-size: 0.85rem;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.article-item {
  animation: fadeInUp 0.5s ease forwards;
}

.article-item:nth-child(1) { animation-delay: 0s; }
.article-item:nth-child(2) { animation-delay: 0.08s; }
.article-item:nth-child(3) { animation-delay: 0.16s; }
.article-item:nth-child(4) { animation-delay: 0.24s; }
.article-item:nth-child(5) { animation-delay: 0.32s; }

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

.article-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  overflow: hidden;
  transition: all 0.3s ease;
}

.article-card:hover {
  border-color: #e2e8f0;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06), 0 12px 48px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.article-card--featured .article-image-wrapper {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
}

.article-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.article-card--featured:hover .article-image {
  transform: scale(1.03);
}

.article-image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.85) 0%, rgba(15, 23, 42, 0.2) 50%, transparent 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 28px;
}

.article-meta-overlay {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.article-date {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.8rem;
  font-weight: 500;
}

.article-tags-overlay {
  display: flex;
  gap: 6px;
}

.tag-pill {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.tag-pill:hover {
  background: rgba(37, 99, 235, 0.8);
}

.article-title-overlay a {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.3;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: color 0.2s ease;
}

.article-title-overlay a:hover {
  color: #93c5fd;
}

.article-body {
  padding: 24px 28px 20px;
}

.article-preview {
  position: relative;
  max-height: 280px;
  overflow: hidden;
  color: #475569;
  line-height: 1.7;
}

.article-preview::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px;
  background: linear-gradient(to bottom, transparent, #ffffff);
  pointer-events: none;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.article-author {
  display: flex;
  align-items: center;
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.article-author:hover {
  color: #2563eb;
}

.read-more {
  color: #2563eb;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.read-more:hover {
  gap: 8px;
}

.arrow {
  transition: transform 0.2s ease;
}

.read-more:hover .arrow {
  transform: translateX(3px);
}

/* Simple card style */
.article-card--simple {
  padding: 28px;
}

.article-simple-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.article-simple-left {
  flex: 1;
}

.article-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0 0 10px 0;
}

.article-title a {
  color: #0f172a;
  transition: color 0.2s ease;
}

.article-title a:hover {
  color: #2563eb;
}

.article-simple-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.article-simple-meta .article-date {
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 500;
}

.article-tags {
  display: flex;
  gap: 6px;
}

.article-tags .tag-pill {
  background: #f1f5f9;
  color: #64748b;
}

.article-tags .tag-pill:hover {
  background: #2563eb;
  color: #ffffff;
}

.article-author-simple {
  margin-left: 16px;
  flex-shrink: 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
}

.pagination :deep(.q-btn) {
  font-weight: 500;
}

@media (max-width: 768px) {
  .article-card--featured .article-image-wrapper {
    height: 220px;
  }
  
  .article-title-overlay a {
    font-size: 1.3rem;
  }
  
  .article-image-overlay {
    padding: 20px;
  }
  
  .article-card--simple {
    padding: 20px;
  }
  
  .article-title {
    font-size: 1.15rem;
  }
  
  .article-body {
    padding: 20px;
  }
  
  .article-simple-header {
    flex-direction: column-reverse;
    align-items: flex-start;
  }
  
  .article-author-simple {
    margin-left: 0;
    margin-bottom: 12px;
  }
}
</style>
