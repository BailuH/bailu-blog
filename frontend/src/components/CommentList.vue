<script setup lang="ts">
import { DefaultService, type CommentDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import moment from 'moment'
import { onBeforeMount, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

// 定义 props
const props = defineProps<{
  articleId: string
}>()

// 组件状态
const comments = ref<CommentDocumentResponse[]>([])
const deletedCommentIds = ref<string[]>([])
const skip = ref<number>(0)
const limit = ref<number>(2)
const newCommentText = ref<string>('')
const newReplyText = ref<string>('')
const commentEditorIsActive = ref<boolean>(false)
const activeReplyEditorCommentId = ref<string | null>(null)

// 从存储中获取当前用户
const currentUser = useUserStore().user

// 加载更多评论的函数
const loadMoreComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    skip.value,
    limit.value
  )
  comments.value.push(...commentsResponse.comments)
  skip.value += limit.value
  return commentsResponse.comments.length
}

// 在评论列表滚动时加载评论的函数
const loadMore = async (_index: number, done: CallableFunction) => {
  const commentsLoaded = await loadMoreComments()
  done(commentsLoaded > 0 ? false : true)
}

// 重新加载评论列表的函数
const reloadComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    0,
    skip.value + limit.value
  )
  comments.value = commentsResponse.comments
}

// 处理“回复”按钮点击的函数
const handleReplyButtonClick = (commentId: string) => {
  activeReplyEditorCommentId.value = commentId
  newReplyText.value = ''
}

// 发送新评论的函数
const handleCommentSubmit = async () => {
  if (newCommentText.value.length > 0) {
    const commentResponse = await DefaultService.createCommentCommentsPost({
      article_id: props.articleId,
      content: newCommentText.value
    })
    newCommentText.value = ''
    commentEditorIsActive.value = false
    reloadComments()
  }
}

// 发送新回复的函数
const handleReplySubmit = async (commentId: string) => {
  if (newReplyText.value.length > 0) {
    const replyResponse = await DefaultService.createReplyCommentsReplyPost({
      parent_comment_id: commentId,
      content: newReplyText.value
    })
    newReplyText.value = ''
    activeReplyEditorCommentId.value = null
    reloadComments()
  }
}

// 处理评论删除按钮点击的函数
const handleDeleteCommentButtonClick = async (commentId: string) => {
  await DefaultService.deleteCommentCommentsCommentIdDelete(commentId)
  Notify.create('评论已删除')
  deletedCommentIds.value.push(commentId)
}

// 检查用户是否可以修改评论的函数
const checkUserCanModifyComment = (authorId: string) => {
  return currentUser?.role == 'Admin' || currentUser?._id == authorId
}

// 检查评论是否已被删除的函数
const isCommentDisabled = (commentId: string) => {
  return deletedCommentIds.value.includes(commentId)
}

onBeforeMount(() => {
  loadMoreComments()
})
</script>

<template>
  <!-- 文章评论和添加新评论表单 -->
  <q-list class="column bg-secondary">
    <!-- 无限滚动加载更多评论 -->
    <q-infinite-scroll @load="loadMore" :offset="10">
      <div class="text-h5 text-white q-ml-md q-mt-md">评论</div>

      <!-- 添加新评论表单 -->
      <div class="row q-mx-md q-mb-md q-pa-sm shadow-2 text-white">
        <q-input
          v-model="newCommentText"
          @focus="commentEditorIsActive = true"
          label="添加新评论..."
          label-color="white"
          class="col-grow q-pa-sm"
        />
        <q-btn
          v-if="commentEditorIsActive"
          @click="handleCommentSubmit"
          label="发送"
          class="col-shrink self-center"
        />
      </div>

      <!-- 评论展示 -->
      <q-item
        v-for="comment in comments"
        :key="comment._id!"
        :class="{ 'disabled-item': isCommentDisabled(comment._id!) }"
        class="column"
      >
        <div class="row shadow-5 q-pa-xs">
          <UserInfoCard :user="comment.author" small class="self-start q-mr-md" />
          <div class="col items-start">
            <!-- 评论作者信息及创建时间 -->
            <div class="row justify-between items-center">
              <div class="col-grow row q-gutter-xs text-subtitle1">
                <router-link
                  :to="{ name: 'user', params: { id: comment.author._id } }"
                  class="text-white"
                >
                  @{{ 'username' in comment.author ? comment.author.username : '' }}
                </router-link>
                <div v-if="comment.author._id == currentUser?._id" class="text-white">(您)</div>
                <div v-if="comment.author.role == 'Admin'" class="text-negative">管理员</div>
              </div>
              <div class="col text-right">
                {{ comment.updated_at ? '(已编辑)' : '' }}
                {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
              </div>
            </div>

            <!-- 评论内容 -->
            <q-item-section class="text-white">
              {{ comment.content }}
            </q-item-section>

            <!-- 回复和删除评论按钮 -->
            <div class="row justify-between">
              <q-btn
                @click="handleReplyButtonClick(comment._id!)"
                label="回复"
                color="secondary"
                no-caps
                flat
                padding="none"
                text-color="white"
                align="left"
              />
              <q-btn
                v-if="checkUserCanModifyComment(comment.author._id!)"
                @click="comment._id && handleDeleteCommentButtonClick(comment._id)"
                label="删除"
                icon-right="clear"
                no-caps
                flat
                padding="none"
              />
            </div>
          </div>
        </div>

        <!-- 回复展示 -->
        <q-list class="q-ml-xl">
          <!-- 添加回复表单 -->
          <div
            v-if="activeReplyEditorCommentId === comment._id"
            class="row shadow-2 q-my-xs q-pa-sm text-white"
          >
            <q-input
              v-model="newReplyText"
              label="添加回复..."
              label-color="white"
              class="col-grow q-px-sm"
            />
            <q-btn
              @click="handleReplySubmit(comment._id!)"
              label="发送"
              class="col-shrink self-center"
            />
          </div>

          <!-- 评论回复展示 -->
          <q-item
            v-for="reply in comment.replies"
            :key="reply._id!"
            :class="{ 'disabled-item': isCommentDisabled(reply._id!) }"
            class="row shadow-2 q-my-xs q-pa-sm"
          >
            <UserInfoCard :user="reply.author" small class="self-start q-mr-md" />
            <div class="col items-start">
              <!-- 回复作者信息及创建时间 -->
              <div class="row justify-between">
                <div class="col-grow row q-gutter-xs text-subtitle1">
                  <router-link
                    :to="{ name: 'user', params: { id: comment.author._id } }"
                    class="text-white"
                  >
                    @{{ 'username' in comment.author ? comment.author.username : '' }}
                  </router-link>
                  <div v-if="comment.author._id == currentUser?._id" class="text-white">(您)</div>
                  <div v-if="comment.author.role == 'Admin'" class="text-negative">管理员</div>
                </div>
                <div class="col-stretch text-right">
                  {{ comment.updated_at ? '(已编辑)' : '' }}
                  {{ moment(comment.created_at).format('hh:mm DD-MM-YYYY') }}
                </div>
              </div>

              <!-- 回复内容 -->
              <div class="text-white">
                {{ reply.content }}
              </div>

              <!-- 删除回复按钮 -->
              <div class="row justify-end">
                <q-btn
                  v-if="checkUserCanModifyComment(reply.author.id)"
                  @click="handleDeleteCommentButtonClick(reply._id!)"
                  label="删除"
                  icon-right="clear"
                  no-caps
                  flat
                  padding="none"
                />
              </div>
            </div>
          </q-item>
        </q-list>
      </q-item>
    </q-infinite-scroll>
  </q-list>
</template>

<style>
.disabled-item {
  pointer-events: none; /* 禁用 q-item 及其子元素的交互 */
  opacity: 0.5; /* 可用于降低禁用元素的透明度 */
}
</style>
