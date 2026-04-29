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
    searchByTags.value ? searchInput : undefined, // tag
    !searchByTags.value ? searchInput : undefined // searchQuery
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
  <div class="column q-pa-md">
    <!-- Header -->
    <div class="row justify-end">
      <div class="col-10">
        <!-- 搜索框 -->
        <q-input
          v-model="searchText"
          @keyup.enter="handleSearchbarSubmit"
          placeholder="搜索"
          class="col-9 bg-white self-end"
          outlined
          dense
          bg-color="white"
        >
          <template v-slot:append>
            <q-icon name="search" @click="handleSearchbarSubmit" class="cursor-pointer text-grey-6" />
            <q-icon name="close" @click="handleSearchbarClear" class="cursor-pointer text-grey-6" />
          </template>
          <!-- "按标签搜索"复选框 -->
          <q-checkbox
            v-model="searchByTags"
            label="按标签搜索"
            class="q-mr-sm text-dark"
            @update:model-value="handleSearchbarSubmit"
          />
        </q-input>
        <!-- 搜索信息 -->
        <div v-if="freezedSearchText.length > 0" class="row self-sta text-accent q-mr-md q-mb-lg">
          <div class="q-mr-md">搜索关键词：{{ freezedSearchText }}</div>
          <div>找到文章数：{{ total }}</div>
        </div>
      </div>
    </div>

    <!-- 文章列表 -->
    <q-list separator padding>
      <!-- 文章 -->
      <div v-for="article in articles" :key="article._id ?? ''" class="row q-mb-lg">
        <!-- 头像和作者名称 -->
        <div class="col-auto q-mx-md">
          <UserInfoCard :user="article.author" class="self-center" />
        </div>

        <!-- 文章主体 -->
        <div class="col column bg-white q-pa-md rounded-borders shadow-1">
          <!-- HEADER - NO PREVIEW -->
          <div v-if="!article.preview_image_url" class="row justify-between q-mb-md full-width">
            <!-- 文章标题 -->
            <div class="col text-h5 text-dark text-weight-bold">
              <router-link
                style="color: inherit; align-self: start"
                :to="'/article/' + article._id"
              >
                {{ article.title }}
              </router-link>
            </div>
            <!-- 日期和标签 -->
            <div class="col column items-end full-width">
              <q-item-label caption class="text-body text-grey-6 flex-shrink">
                {{ moment(article?.created_at).format('Do MMMM YYYY') }}
              </q-item-label>
              <div v-if="article?.tags">
                <router-link
                  v-for="tag in article?.tags"
                  :key="tag"
                  :to="{ name: 'home', query: { tag: tag } }"
                >
                  <q-chip :label="tag" size="sm" color="secondary" text-color="dark" class="q-mr-xs" />
                </router-link>
              </div>
            </div>
          </div>

          <!-- 如果有预览图 -->
          <div v-else class="q-mb-md rounded-borders" style="position: relative">
            <img
              v-if="article?.preview_image_url"
              :src="article.preview_image_url"
              :alt="article.title ?? ''"
              class="rounded-borders"
              style="width: 100%; height: 250px; object-fit: cover"
            />
            <!-- 叠加文字 -->
            <div class="overlay-text column justify-between q-mb-md">
              <!-- 日期和标签 -->
              <div class="col full-width full-height q-pt-md">
                <q-item-label caption class="text-body flex-shrink">
                  {{ moment(article?.created_at).format('Do MMMM YYYY') }}
                </q-item-label>
                <div v-if="article?.tags">
                  <router-link
                    v-for="tag in article?.tags"
                    :key="tag"
                    :to="{ name: 'home', query: { tag: tag } }"
                  >
                    <q-chip :label="tag" size="sm" color="secondary" text-color="dark" class="q-mr-xs" />
                  </router-link>
                </div>
              </div>
              <!-- 文章标题 -->
              <div class="col full-width full-height text-h3 text-white text-weight-bold">
                <router-link
                  style="color: inherit; align-self: start; text-decoration: none"
                  :to="'/article/' + article._id"
                >
                  {{ article.title }}
                </router-link>
              </div>
              <div class="col full-width full-height"></div>
            </div>
          </div>

          <!-- 文章内容 -->
          <div class="preview-clamp">
            <MdPreview
              :modelValue="article.content || ''"
              language="zh-CN"
            />
          </div>
          <!-- "阅读全文"按钮 -->
          <q-btn :to="'/article/' + article._id" flat no-caps class="float-right text-accent">
            <q-item-label caption>阅读全文 &rarr;</q-item-label>
          </q-btn>
        </div>
      </div>
    </q-list>

    <!-- 分页 -->
    <q-pagination
      v-model="page"
      @update:model-value="handlePageChange"
      input
      :max="maxPage"
      class="self-center"
      color="accent"
      text-color="dark"
    />
  </div>
</template>

<style scoped>
.a {
  text-decoration: none;
}

.search-input {
  width: 80%;
}

.overlay-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-align: center;
  z-index: 1;
  text-shadow: 2px 2px 2px #00000044;
}

.preview-clamp {
  position: relative;
  max-height: 400px;
  overflow: hidden;
}

/* 底部渐变遮罩，避免硬截断 */
.preview-clamp::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 40px;
  background: linear-gradient(to bottom, transparent, white);
  pointer-events: none;
}
</style>
