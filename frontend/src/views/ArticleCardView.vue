<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse, type UserDocument } from '@/client'
import ArticleCard from '@/components/ArticleCard.vue'
import CommentList from '@/components/CommentList.vue'
import { onBeforeMount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import moment from 'moment'

const article = ref<ArticleDocumentResponse>()
const relatedArticles = ref<ArticleDocumentResponse[]>([])
const authorArticles = ref<ArticleDocumentResponse[]>([])

const route = useRoute()

const loadArticle = async () => {
  const articleResponse = await DefaultService.readArticleArticlesArticleIdGet(
    route.params.id.toString()
  )
  article.value = articleResponse.article

  // Load related content
  if (article.value) {
    try {
      // Load author's other articles (all articles then filter by author)
      const authorRes = await DefaultService.listArticlesArticlesGet(0, 50)
      authorArticles.value = authorRes.articles
        .filter((a: ArticleDocumentResponse) =>
          a.author?._id === article.value?.author?._id && a._id !== article.value?._id
        )
        .slice(0, 3)
    } catch {
      // ignore
    }

    try {
      // Load related by first tag
      const firstTag = article.value.tags?.[0]
      if (firstTag) {
        const relatedRes = await DefaultService.listArticlesArticlesGet(
          0, 4, undefined, undefined, firstTag
        )
        relatedArticles.value = relatedRes.articles
          .filter((a: ArticleDocumentResponse) => a._id !== article.value?._id)
          .slice(0, 3)
      }
    } catch {
      // ignore
    }
  }
}

watch(() => route.params.id, async () => {
  await loadArticle()
  window.scrollTo(0, 0)
}, { immediate: true })
</script>

<template>
  <q-page v-if="article" class="article-page">
    <div class="article-layout">
      <!-- Main Content -->
      <div class="article-main">
        <ArticleCard :article="article" />
        <CommentList :articleId="article._id!" />
      </div>

      <!-- Sidebar -->
      <aside class="article-sidebar">
        <!-- Author Card -->
        <div class="sidebar-card">
          <div class="sidebar-card-header">
            <q-icon name="person" size="1rem" class="q-mr-sm" />
            关于作者
          </div>
          <div class="sidebar-author">
            <router-link
              :to="{ name: 'user', params: { id: article.author?._id } }"
              class="sidebar-author-link"
            >
              <q-avatar size="56px" class="sidebar-author-avatar">
                <img :src="article.author?.avatar_url || '/favicon.ico'" />
              </q-avatar>
              <div class="sidebar-author-info">
                <div class="sidebar-author-name">{{ article.author?.username }}</div>
                <div class="sidebar-author-role" v-if="article.author?.role">
                  {{ article.author.role }}
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Article Tags -->
        <div v-if="article.tags && article.tags.length > 0" class="sidebar-card">
          <div class="sidebar-card-header">
            <q-icon name="label" size="1rem" class="q-mr-sm" />
            文章标签
          </div>
          <div class="sidebar-tags">
            <router-link
              v-for="tag in article.tags"
              :key="tag"
              :to="{ name: 'home', query: { tag } }"
              class="sidebar-tag"
            >
              {{ tag }}
            </router-link>
          </div>
        </div>

        <!-- [预留] 广告/推荐位 -->
        <div class="sidebar-card sidebar-card--placeholder">
          <div class="sidebar-card-header">
            <q-icon name="campaign" size="1rem" class="q-mr-sm" />
            推荐位
          </div>
          <div class="placeholder-box">
            <q-icon name="image" size="2rem" color="blue-3" />
            <span class="placeholder-text">[预留] 侧边广告/推广位</span>
            <span class="placeholder-hint">建议尺寸 280×200</span>
          </div>
        </div>

        <!-- Author's Other Articles -->
        <div v-if="authorArticles.length > 0" class="sidebar-card">
          <div class="sidebar-card-header">
            <q-icon name="library_books" size="1rem" class="q-mr-sm" />
            作者其他文章
          </div>
          <div class="sidebar-articles">
            <router-link
              v-for="(a, idx) in authorArticles"
              :key="a._id || idx"
              :to="'/article/' + a._id"
              class="sidebar-article"
            >
              <div class="sidebar-article-image-wrapper">
                <img
                  v-if="a.preview_image_url"
                  :src="a.preview_image_url"
                  class="sidebar-article-image"
                />
                <div v-else class="sidebar-article-image-placeholder">
                  <q-icon name="article" size="1rem" color="blue-3" />
                </div>
              </div>
              <div class="sidebar-article-body">
                <div class="sidebar-article-title">{{ a.title }}</div>
                <div class="sidebar-article-date">
                  {{ moment(a.created_at).format('YYYY.MM.DD') }}
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Related Articles -->
        <div v-if="relatedArticles.length > 0" class="sidebar-card">
          <div class="sidebar-card-header">
            <q-icon name="auto_stories" size="1rem" class="q-mr-sm" />
            相关推荐
          </div>
          <div class="sidebar-articles">
            <router-link
              v-for="(a, idx) in relatedArticles"
              :key="a._id || idx"
              :to="'/article/' + a._id"
              class="sidebar-article"
            >
              <div class="sidebar-article-image-wrapper">
                <img
                  v-if="a.preview_image_url"
                  :src="a.preview_image_url"
                  class="sidebar-article-image"
                />
                <div v-else class="sidebar-article-image-placeholder">
                  <q-icon name="article" size="1rem" color="blue-3" />
                </div>
              </div>
              <div class="sidebar-article-body">
                <div class="sidebar-article-title">{{ a.title }}</div>
                <div class="sidebar-article-date">
                  {{ moment(a.created_at).format('YYYY.MM.DD') }}
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- [预留] 二维码/公众号位 -->
        <div class="sidebar-card sidebar-card--placeholder">
          <div class="sidebar-card-header">
            <q-icon name="qr_code" size="1rem" class="q-mr-sm" />
            关注我
          </div>
          <div class="placeholder-box">
            <q-icon name="qr_code_scanner" size="2.5rem" color="blue-3" />
            <span class="placeholder-text">[预留] 二维码/公众号</span>
            <span class="placeholder-hint">建议尺寸 200×200</span>
          </div>
        </div>
      </aside>
    </div>
  </q-page>
</template>

<style scoped>
.article-page {
  padding: 24px 0 48px;
}

.article-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 32px;
  align-items: start;
}

.article-main {
  min-width: 0;
}

/* ===== Sidebar ===== */
.article-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 80px;
}

.sidebar-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  padding: 20px;
  transition: all 0.25s ease;
}

.sidebar-card:hover {
  border-color: #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.sidebar-card-header {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
}

/* Author */
.sidebar-author-link {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
}

.sidebar-author-avatar {
  border: 3px solid #f1f5f9;
  transition: all 0.25s ease;
}

.sidebar-author-link:hover .sidebar-author-avatar {
  border-color: #bfdbfe;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.12);
}

.sidebar-author-name {
  font-weight: 700;
  color: #0f172a;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.sidebar-author-link:hover .sidebar-author-name {
  color: #2563eb;
}

.sidebar-author-role {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 2px;
  text-transform: uppercase;
}

/* Tags */
.sidebar-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.sidebar-tag {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 10px;
  background: #f8fafc;
  color: #475569;
  font-size: 0.82rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.sidebar-tag:hover {
  background: #2563eb;
  color: #ffffff;
}

/* Articles list in sidebar */
.sidebar-articles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-article {
  display: flex;
  gap: 12px;
  text-decoration: none;
  padding: 8px;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.sidebar-article:hover {
  background: #f8fafc;
}

.sidebar-article-image-wrapper {
  width: 64px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f1f5f9;
}

.sidebar-article-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.sidebar-article:hover .sidebar-article-image {
  transform: scale(1.05);
}

.sidebar-article-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-article-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.sidebar-article-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 4px;
  transition: color 0.2s ease;
}

.sidebar-article:hover .sidebar-article-title {
  color: #2563eb;
}

.sidebar-article-date {
  font-size: 0.72rem;
  color: #94a3b8;
}

/* Placeholder */
.sidebar-card--placeholder {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.placeholder-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 24px;
  border-radius: 12px;
  border: 2px dashed #e2e8f0;
}

.placeholder-text {
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
}

.placeholder-hint {
  font-size: 0.72rem;
  color: #94a3b8;
}

@media (max-width: 900px) {
  .article-layout {
    grid-template-columns: 1fr;
  }

  .article-sidebar {
    position: static;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

@media (max-width: 600px) {
  .article-sidebar {
    grid-template-columns: 1fr;
  }
}
</style>
