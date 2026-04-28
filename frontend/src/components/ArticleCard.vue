<script setup lang="ts">
import { type ArticleDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { useUserStore } from '@/stores/UserStore'
import moment from 'moment'
import { computed, onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{
  article: ArticleDocumentResponse | undefined
}>()

const route = useRoute()

const formattedDate = ref<string>(moment(props.article?.created_at).format('Do MMMM YYYY'))
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
  <div class="column q-pa-md">
    <!-- 文章区块 -->
    <div class="column bg-white q-pa-md rounded-borders shadow-1">
      <!-- 带预览图背景的标题栏 -->
      <div
        class="article-header q-pa-sm q-mb-md rounded-borders"
        :style="{ backgroundImage: 'url(' + article?.preview_image_url + ')' }"
      >
        <div class="row justify-between items-center q-mb-md">
          <!-- 头像和作者名称 -->
          <router-link
            :to="{ name: 'user', params: { id: article?.author?._id } }"
            class="row items-end text-h5 text-uppercase text-weight-bold text-white"
          >
            <UserInfoCard :user="article?.author" small class="q-mr-md" />
            {{ article?.author?.username }}
          </router-link>
          <!-- 日期和标签 -->
          <div class="col column items-end full-width">
            <div caption class="date-shadow text-body flex-shrink">
              {{ formattedDate }}
            </div>
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
        <!-- 文章标题 -->
        <div class="title-style q-mb-lg text-h4 text-white text-weight-bold text-center">
          {{ article?.title }}
        </div>
      </div>

      <!-- 文章正文 -->
      <div
        class="text-body1 text-grey-7"
        v-html="article.content!.replace(/\n/g, '<br>')"
      />

      <!-- "编辑文章"按钮 -->
      <q-btn
        v-if="isAllowedToEdit"
        label="编辑"
        :to="editLink"
        flat
        no-caps
        class="self-end text-body q-ma-md text-accent"
      />
    </div>
  </div>
</template>

<style scoped>
.article-header {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.title-style {
  text-shadow: 2px 2px 2px #00000044;
}

.date-shadow {
  text-shadow: 2px 2px 4px #ffffff;
}
</style>
