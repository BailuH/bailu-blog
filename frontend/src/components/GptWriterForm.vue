<script setup lang="ts">
import { ref } from 'vue'
import { DefaultService } from '@/client'
import router from '@/router'

const title = ref('ESP32 软件开发')
const tagsString = ref('编程, ESP32')
const keyPhrasesString = ref('开发环境, 数据交换')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  const gptGeneratorResponse = await DefaultService.generateArticleGptWriterPost({
    title: title.value,
    tags: [...tagsString.value.split(','), 'ChatGPT generated'],
    key_phrases: keyPhrasesString.value.split(',').map((phrase) => phrase.trim())
  }).finally(() => {
    loading.value = false
  })

  console.log(gptGeneratorResponse)

  const articleId = gptGeneratorResponse.article._id
  // 根据组件名称和文章 ID 进行跳转
  router.push({ name: 'edit-article', params: { id: articleId } })
}
</script>

<template>
  <q-card square class="shadow-1 bg-white" style="width: 400px; max-width: 90vw;">
    <q-card-section class="bg-white border-bottom">
      <h4 class="text-dark q-my-md text-weight-bold">GptWriter</h4>
    </q-card-section>

    <!-- GptWriter 模块说明 -->
    <q-card-section class="bg-white">
      <p class="text-grey-7">该模块根据输入的数据生成文章。</p>
      <p class="text-grey-7">
        生成成功后，您将被重定向到所创建文章的编辑页面。
      </p>
    </q-card-section>

    <q-form class="q-px-md q-pt-md">
      <q-input label="标题" v-model="title" clearable outlined dense class="q-mb-md" />
      <!-- 新标签输入框 -->
      <q-input label="新标签（用逗号分隔）" v-model="tagsString" clearable outlined dense class="q-mb-md" />
      <!-- 新关键词输入框 -->
      <q-input label="新关键词（用逗号分隔）" v-model="keyPhrasesString" clearable outlined dense class="q-mb-md" />
    </q-form>

    <!-- 在收到响应前显示加载状态 -->
    <q-card-actions class="q-px-lg">
      <q-btn
        unelevated
        size="md"
        color="accent"
        class="full-width text-white"
        @click="handleSubmit"
        :disable="loading"
        no-caps
      >
        <div v-if="!loading" class="row items-center no-wrap">
          <div>生成文章</div>
        </div>
        <q-spinner-oval v-if="loading" />
      </q-btn>
    </q-card-actions>
  </q-card>
</template>

<style scoped>
.border-bottom {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
