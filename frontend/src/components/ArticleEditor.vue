<script setup lang="ts">
import { DefaultService, type ArticleDocumentResponse } from '@/client'
import router from '@/router'
import { Notify } from 'quasar'
import { ref } from 'vue'
import { MdEditor } from 'md-editor-v3'

export interface Props {
  articleToEdit?: ArticleDocumentResponse // 代表需要被编辑的文章，把父组件的文章数据回显到当前组件
  createMode?: boolean
  editMode?: boolean
}

// `defineProps<>()`是Vue3的编程宏（TS泛型格式），最终转换为**当前**组件的Props声明配置
// 这里是要给文章编辑状态的Props设置默认值
// 这里有两种写法，在3.5+的版本可以使用**响应式结构**
// 由于这里用的是TS，因此还要注意如何正确地给Props确定类型，参见：https://cn.vuejs.org/guide/typescript/composition-api.html#typing-component-props
const props = withDefaults(defineProps<Props>(), {
  createMode: () => false,
  editMode: () => false
})

// const { createMode = false, editMode = false } = defineProps<Props>()


const titleRef = ref<string>(
  props.articleToEdit?.title ? props.articleToEdit.title : ''
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
    <q-card square class="shadow-1 bg-white" style="min-height: 550px">
      <!-- HTML 编辑器 -->
      <q-input
        v-model="titleRef"
        label="标题"
        :input-style="{ fontSize: '20px' }"
        class="q-ma-md"
        outlined
        dense
      />
      <MdEditor 
        v-model="conentRef"
        language="zh-CN"
        placeholder=""
        style="height: 500px"
      />
      <!-- 预览图链接 -->
      <div class="row justify-between items-center q-pa-md">
        <q-input
          v-model="previewImageURLRef"
          label="预览图链接"
          class="col-grow q-pr-md"
          outlined
          dense
        />
        <!-- 图片高度受相邻组件限制 -->
        <img
          v-if="previewImageURLRef"
          :src="previewImageURLRef"
          class="rounded-borders"
          style="max-height: 50px"
        />
        <q-btn
          label="从默认图库选择预览图"
          @click="previewImageDialog = true"
          flat
          no-caps
          size="sm"
          class="col-4 text-accent"
        />
      </div>

      <!-- 标签 -->
      <div class="row justify-between items-center q-px-md q-pb-md">
        <div>
          <q-chip
            v-for="tag in tagsRef"
            :label="tag"
            :key="tag"
            removable
            @remove="tagsRef.splice(tagsRef.indexOf(tag), 1)"
            size="sm"
            color="secondary"
            text-color="dark"
          />
        </div>
        <!-- 添加标签 -->
        <div class="row">
          <q-input v-model="newTag" class="col q-pl-lg" dense outlined />
          <q-btn label="添加标签" @click="handleAddTag" flat no-caps size="sm" class="text-accent">
          </q-btn>
        </div>
      </div>

      <!-- 按钮 -->
      <q-card-actions class="row justify-between border-top q-pa-md">
        <q-btn
          label="保存文章"
          no-caps
          class="q-ma-md self-stretch text-white bg-accent"
          @click="handleArticleSave"
          unelevated
        />
        <!-- 红色的删除按钮，触发删除对话框 -->
        <q-btn
          v-if="editMode"
          label="删除文章"
          no-caps
          class="q-ma-md self-stretch text-white bg-negative"
          @click="articleDeleteDialog = true"
          unelevated
        />
      </q-card-actions>
    </q-card>

    <!-- 文章删除确认对话框（提示：您确定要删除这篇文章吗？此操作不可撤销） -->
    <q-dialog v-model="articleDeleteDialog">
      <q-card class="bg-white items-center" style="width: 100%">
        <q-card-section>
          <div class="text-body2 text-center q-mt-sm text-dark">
            您确定要删除这篇文章吗？<br />
            此操作<b class="text-negative">不可撤销</b>。
          </div>
        </q-card-section>
        <q-card-actions class="justify-around">
          <q-btn @click="articleDeleteDialog = false" color="grey-6" no-caps flat>取消删除</q-btn>
          <q-btn @click="handleArticleDelete" color="negative" no-caps unelevated>删除</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!-- 从默认图库选择预览图对话框 -->
    <q-dialog v-model="previewImageDialog">
      <q-card class="bg-white" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <div class="text-center text-h6 text-dark q-mb-md">为文章选择预览图</div>
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

<style scoped>
.border-top {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
