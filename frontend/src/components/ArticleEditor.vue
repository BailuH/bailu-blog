<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse } from '@/client'
import router from '@/router'
import { Notify } from 'quasar'
import { ref } from 'vue'

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
  props.articleToEdit?.title ? props.articleToEdit.title : '文章标题'
)
const conentRef = ref<string>(
  props.articleToEdit?.content ? props.articleToEdit.content : '文章正文'
)
const tagsRef = ref<string[]>(
  props.articleToEdit?.tags ? props.articleToEdit.tags : ['标签1', '标签2']
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
  if (newTag.value) {
    tagsRef.value.push(newTag.value)
    newTag.value = ''
  }
}
</script>

<template>
  <div class="column q-pa-md">
    <q-card square class="shadow-24" style="min-heightht: 550px">
      <!-- HTML 编辑器 -->
      <q-input
        v-model="titleRef"
        label="标题"
        :input-style="{ fontSize: '20px' }"
        class="q-ma-md"
      />
      <q-editor v-model="conentRef" min-height="5rem" />

      <!-- 预览图链接 -->
      <div class="row justify-between items-center">
        <q-input v-model="previewImageURLRef" label="预览图链接" class="col-grow q-pa-md" />
        <!-- 图片高度受相邻组件限制 -->
          <img :src="previewImageURLRef" class="rounded-borders" style="max-height: 50px" />
        <q-btn
          label="从默认图库选择预览图"
          @click="previewImageDialog = true"
          flat
          size="sm"
          class="col-4"
        />
      </div>

      <!-- 标签 -->
      <div class="row justify-between items-center">
        <div>
          <q-chip
            v-for="tag in tagsRef"
            :label="tag"
            :key="tag"
            removable
            @remove="tagsRef.splice(tagsRef.indexOf(tag), 1)"
            size="sm"
            dark
            color="primary"
          />
        </div>
        <!-- 添加标签 -->
        <div class="row">
          <q-input v-model="newTag" class="col q-pl-lg" dense />
          <q-btn label="添加标签" @click="handleAddTag" flat size="sm"> </q-btn>
        </div>
      </div>

      <!-- 按钮 -->
      <q-card-actions class="row justify-between">
        <q-btn label="保存文章" class="q-ma-md self-stretch" @click="handleArticleSave" />
        <!-- 红色的删除按钮，触发删除对话框 -->
        <q-btn
          v-if="editMode"
          label="删除文章"
          class="q-ma-md self-stretch text-white bg-negative"
          @click="articleDeleteDialog = true"
        />
      </q-card-actions>
    </q-card>

    <!-- 文章删除确认对话框（提示：您确定要删除这篇文章吗？此操作不可撤销） -->
    <q-dialog v-model="articleDeleteDialog">
      <q-card class="bg-secondary items-center" style="width: 100%">
        <q-card-section>
          <div class="text-body2 text-center q-mt-sm">
            您确定要删除这篇文章吗？<br />
            此操作<b class="text-info">不可撤销</b>。
          </div>
        </q-card-section>
        <q-card-actions class="justify-around">
          <q-btn @click="articleDeleteDialog = false" color="primary">取消删除</q-btn>
          <q-btn @click="handleArticleDelete" color="secondary">删除</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!-- 从默认图库选择预览图对话框 -->
    <q-dialog v-model="previewImageDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <div class="text-center text-h6 text-white q-mb-md">为文章选择预览图</div>
          <q-btn
            v-for="imageUrl in getDefaultPreviewImages()"
            :key="imageUrl"
            @click="previewImageURLRef = imageUrl"
            v-close-popup
            flat
          >
            <img :src="imageUrl" style="width: 100px" />
          </q-btn>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
