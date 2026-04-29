<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse } from '@/client'
import ArticleList from '@/components/ArticleList.vue'
import { onBeforeMount, ref } from 'vue'
import moment from 'moment'

const featuredArticles = ref<ArticleDocumentResponse[]>([])
const slide = ref('1') // 轮播图当前页绑定

onBeforeMount(async () => {
  try {
    const res = await DefaultService.listArticlesArticlesGet(0, 3)
    featuredArticles.value = res.articles.slice(0, 3)
  } catch {
    // ignore
  }
})
</script>

<template>
  <q-page class="home-page">
    <!-- 首图板块 -->
    <section class="hero-section">
      <div class="hero-left">
        <h1 class="hero-title">
          探索<br />
          <span class="hero-title-accent">思想的深度</span>
        </h1>
        <p class="hero-desc">
          记录技术成长的每一步，分享对世界的思考与观察。
          这里汇聚开发者、创作者与思考者的声音。
        </p>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="hero-stat-num">+</span>
            <span class="hero-stat-label">原创文章</span>
          </div>
          <div class="hero-stat-divider"></div>
          <div class="hero-stat">
            <span class="hero-stat-num">+</span>
            <span class="hero-stat-label">活跃作者</span>
          </div>
          <div class="hero-stat-divider"></div>
          <div class="hero-stat">
            <span class="hero-stat-num">+</span>
            <span class="hero-stat-label">技术讨论</span>
          </div>
        </div>
      </div>
      <!-- 轮播图 -->
      <div class="hero-visual">
        <q-carousel
          v-model="slide"
          animated
          infinite
          autoplay
          arrows
          navigation
          transition-prev="slide-right"
          transition-next="slide-left"
          control-color="white"
          control-text-color="grey-8"
          class="hero-carousel shadow-2 rounded-boarders"
        >
          <q-carousel-slide name="1" class="q-pa-none">
            <img src="../../images/pexels-alphaen-15601235.jpg" alt="图片无法显示" class="carousel-img" draggable="false">
          </q-carousel-slide>
          <q-carousel-slide name="2" class="q-pa-none">
            <img src="../../images/pexels-jean-daniel-4006158.jpg" alt="图片无法显示" class="carousel-img" draggable="false">
          </q-carousel-slide>
          <q-carousel-slide name="3" class="q-pa-none">
            <img src="../../images/pexels-eberhardgross-443446.jpg" alt="图片无法显示" class="carousel-img" draggable="false">
          </q-carousel-slide>
        </q-carousel>
      </div>
    </section>

    <!-- 精选文章板块 -->
    <section v-if="featuredArticles.length > 0" class="featured-section">
      <div class="section-header">
        <h2 class="section-title">精选文章</h2>
        <router-link to="/" class="section-link">
          查看全部 <span class="arrow">&rarr;</span>
        </router-link>
      </div>
      <div class="featured-grid">
        <router-link
          v-for="(article, index) in featuredArticles"
          :key="article._id ?? index"
          :to="'/article/' + article._id"
          class="featured-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="featured-image-wrapper">
            <img
              v-if="article.preview_image_url"
              :src="article.preview_image_url"
              class="featured-image"
            />
            <div v-else class="featured-image-placeholder">
              <q-icon name="article" size="2rem" color="blue-3" />
              <span>暂未设置文章封面噢</span>
            </div>
          </div>
          <div class="featured-body">
            <h3 class="featured-title">{{ article.title }}</h3>
            <div class="featured-meta">
              <span class="featured-author">{{ article.author?.username }}</span>
              <span class="featured-date">{{ moment(article.created_at).format('M月D日') }}</span>
            </div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Main Content -->
    <section class="main-content">
      <ArticleList />
    </section>
  </q-page>
</template>

<style scoped>
.home-page {
  padding: 32px 0 48px;
}

/* ===== Hero Section ===== */
.hero-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: center;
  margin-bottom: 28px;
  padding: 48px 200px 48px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #DFB871 50%, #F7B324 100%);
  border-radius: 28px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -80px;
  right: -80px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

.hero-left {
  position: relative;
  z-index: 1;
}

.hero-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.15;
  margin: 0 0 16px 0;
  letter-spacing: -0.03em;
}

.hero-title-accent {
  background: linear-gradient(135deg, #F8DF72 0%, #EDA01F 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  color: #64748b;
  font-size: 1.05rem;
  line-height: 1.7;
  margin: 0 0 28px 0;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hero-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hero-stat-num {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
}

.hero-stat-label {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 500;
}

.hero-stat-divider {
  width: 1px;
  height: 36px;
  background: #e2e8f0;
}

/* Hero Visual / Carousel */
.hero-visual {
  position: relative;
  z-index: 1;
  max-width: 420px;
}

.hero-carousel {
  border-radius: 20px;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.08);
  /* 保持 3:2 比例 */
  aspect-ratio: 3 / 2;
}

/* 让图片填满 slide */
.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 自定义导航点颜色，匹配你的主题 */
.hero-carousel :deep(.q-carousel__navigation-inner .q-btn) {
  color: #ffffff !important;
}

.hero-carousel :deep(.q-carousel__navigation-inner .q-btn--active) {
  color: #2563eb !important;
}

/* ===== Featured Section ===== */
.featured-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.section-link {
  color: #2563eb;
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.2s ease;
}

.section-link:hover {
  gap: 8px;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.featured-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  overflow: hidden;
  transition: all 0.3s ease;
  text-decoration: none;
  animation: fadeInUp 0.5s ease both;
}

.featured-card:hover {
  border-color: #e2e8f0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  transform: translateY(-4px);
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

.featured-image-wrapper {
  width: 100%;
  height: 160px;
  overflow: hidden;
  background: #f8fafc;
}

.featured-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.featured-card:hover .featured-image {
  transform: scale(1.05);
}

.featured-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #94a3b8;
  font-size: 0.8rem;
}

.featured-body {
  padding: 16px 18px 18px;
}

.featured-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.4;
  margin: 0 0 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.78rem;
}

.featured-author {
  color: #64748b;
  font-weight: 500;
}

.featured-date {
  color: #94a3b8;
}

/* ===== Main Content ===== */
.main-content {
  /* ArticleList handles its own padding */
}

@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    padding: 32px 24px;
    gap: 28px;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-desc {
    font-size: 0.95rem;
  }

  .featured-grid {
    grid-template-columns: 1fr;
  }

  .hero-stats {
    gap: 16px;
  }

  .hero-stat-num {
    font-size: 1.3rem;
  }
}
</style>
