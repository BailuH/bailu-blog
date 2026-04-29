<script setup lang="ts">
import { DefaultService, type CommentDocumentResponse } from '@/client'
import UserInfoCard from '@/components/UserInfoCard.vue'
import moment from 'moment'
import { ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

const props = defineProps<{
  articleId: string
}>()

const comments = ref<CommentDocumentResponse[]>([])
const deletedCommentIds = ref<string[]>([])
const skip = ref<number>(0)
const limit = ref<number>(10)
const newCommentText = ref<string>('')
const newReplyText = ref<string>('')
const commentEditorIsActive = ref<boolean>(false)
const activeReplyEditorCommentId = ref<string | null>(null)

const currentUser = useUserStore().user

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

const loadMore = async (_index: number, done: CallableFunction) => {
  const commentsLoaded = await loadMoreComments()
  done(commentsLoaded > 0 ? false : true)
}

const reloadComments = async () => {
  const commentsResponse = await DefaultService.listCommentsCommentsGet(
    props.articleId,
    0,
    skip.value + limit.value
  )
  comments.value = commentsResponse.comments
}

const handleReplyButtonClick = (commentId: string) => {
  activeReplyEditorCommentId.value = commentId
  newReplyText.value = ''
}

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

const handleDeleteCommentButtonClick = async (commentId: string) => {
  await DefaultService.deleteCommentCommentsCommentIdDelete(commentId)
  Notify.create('评论已删除')
  deletedCommentIds.value.push(commentId)
}

const checkUserCanModifyComment = (authorId: string) => {
  return currentUser?.role == 'Admin' || currentUser?._id == authorId
}

const isCommentDisabled = (commentId: string) => {
  return deletedCommentIds.value.includes(commentId)
}

// 初始加载由 q-infinite-scroll 自动触发，避免与 onBeforeMount 重复加载
</script>

<template>
  <div class="comments-section">
    <div class="comments-header">
      <h3 class="comments-title">
        <q-icon name="chat_bubble" class="q-mr-sm" size="1.1rem" />
        评论
        <span v-if="comments.length > 0" class="comments-count">{{ comments.length }}</span>
      </h3>
    </div>

    <!-- New comment input -->
    <div class="comment-input-area">
      <q-avatar size="38px" class="comment-avatar q-mr-md">
        <img :src="currentUser?.avatar_url || '/favicon.ico'" />
      </q-avatar>
      <div class="comment-input-wrapper">
        <q-input
          v-model="newCommentText"
          @focus="commentEditorIsActive = true"
          placeholder="写下你的想法..."
          class="comment-input"
          outlined
          dense
          autogrow
          type="textarea"
          :input-style="{ minHeight: commentEditorIsActive ? '80px' : '44px', maxHeight: '200px' }"
        />
        <div v-if="commentEditorIsActive" class="comment-input-actions">
          <q-btn
            @click="commentEditorIsActive = false; newCommentText = ''"
            flat
            no-caps
            label="取消"
            class="cancel-btn"
            size="sm"
          />
          <q-btn
            @click="handleCommentSubmit"
            no-caps
            unelevated
            color="accent"
            label="发送评论"
            class="submit-btn"
            size="sm"
            :disable="!newCommentText.trim()"
          />
        </div>
      </div>
    </div>

    <!-- Comments list -->
    <q-infinite-scroll @load="loadMore" :offset="10" class="comments-list">
      <div
        v-for="comment in comments"
        :key="comment._id!"
        :class="{ 'disabled-item': isCommentDisabled(comment._id!) }"
        class="comment-item"
      >
        <!-- Comment body -->
        <div class="comment-main">
          <router-link
            :to="{ name: 'user', params: { id: comment.author._id } }"
            class="comment-author-avatar"
          >
            <q-avatar size="40px">
              <img :src="comment.author.avatar_url || '/favicon.ico'" />
            </q-avatar>
          </router-link>
          <div class="comment-content">
            <div class="comment-header-row">
              <div class="comment-author-info">
                <router-link
                  :to="{ name: 'user', params: { id: (comment.author as any)._id } }"},{
                  class="comment-author-name"
                >
                  {{ 'username' in comment.author ? comment.author.username : '' }}
                </router-link>
                <span v-if="comment.author.role == 'Admin'" class="author-badge admin">管理员</span>
                <span v-if="comment.author._id == currentUser?._id" class="author-badge you">我</span>
              </div>
              <span class="comment-time">
                {{ comment.updated_at ? '(已编辑) ' : '' }}
                {{ moment(comment.created_at).format('MM-DD HH:mm') }}
              </span>
            </div>
            <p class="comment-text">{{ comment.content }}</p>
            <div class="comment-actions">
              <button
                @click="handleReplyButtonClick(comment._id!)"
                class="action-btn"
              >
                <q-icon name="reply" size="0.85rem" class="q-mr-xs" />
                回复
              </button>
              <button
                v-if="checkUserCanModifyComment(comment.author._id!)"
                @click="comment._id && handleDeleteCommentButtonClick(comment._id)"
                class="action-btn action-btn--danger"
              >
                <q-icon name="delete_outline" size="0.85rem" class="q-mr-xs" />
                删除
              </button>
            </div>
          </div>
        </div>

        <!-- Reply editor -->
        <div
          v-if="activeReplyEditorCommentId === comment._id"
          class="reply-editor"
        >
          <q-avatar size="32px" class="q-mr-md">
            <img :src="currentUser?.avatar_url || '/favicon.ico'" />
          </q-avatar>
          <div class="reply-input-wrapper">
            <q-input
              v-model="newReplyText"
              placeholder="回复..."
              class="reply-input"
              outlined
              dense
              autogrow
              type="textarea"
              :input-style="{ minHeight: '60px', maxHeight: '150px' }"
            />
            <div class="reply-input-actions">
              <q-btn
                @click="activeReplyEditorCommentId = null"
                flat
                no-caps
                label="取消"
                class="cancel-btn"
                size="sm"
              />
              <q-btn
                @click="handleReplySubmit(comment._id!)"
                no-caps
                unelevated
                color="accent"
                label="发送"
                class="submit-btn"
                size="sm"
                :disable="!newReplyText.trim()"
              />
            </div>
          </div>
        </div>

        <!-- Replies -->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
          <div
            v-for="reply in comment.replies"
            :key="reply._id!"
            :class="{ 'disabled-item': isCommentDisabled(reply._id!) }"
            class="reply-item"
          >
            <q-avatar size="32px" class="q-mr-md">
              <img :src="(reply.author as any).avatar_url || '/favicon.ico'" />
            </q-avatar>
            <div class="reply-content">
              <div class="reply-header-row">
                <div class="reply-author-info">
                  <router-link
                    :to="{ name: 'user', params: { id: (reply.author as any)._id } }"
                    class="reply-author-name"
                  >
                    {{ 'username' in reply.author ? (reply.author as any).username : '' }}
                  </router-link>
                  <span v-if="(reply.author as any).role == 'Admin'" class="author-badge admin">管理员</span>
                </div>
                <span class="reply-time">
                  {{ reply.updated_at ? '(已编辑) ' : '' }}
                  {{ moment(reply.created_at).format('MM-DD HH:mm') }}
                </span>
              </div>
              <p class="reply-text">{{ reply.content }}</p>
              <div class="reply-actions">
                <button
                  v-if="checkUserCanModifyComment((reply.author as any).id)"
                  @click="handleDeleteCommentButtonClick(reply._id!)"
                  class="action-btn action-btn--danger"
                >
                  <q-icon name="delete_outline" size="0.85rem" class="q-mr-xs" />
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-infinite-scroll>
  </div>
</template>

<style scoped>
.comments-section {
  margin-top: 32px;
  animation: fadeInUp 0.5s ease 0.1s both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.comments-header {
  margin-bottom: 24px;
}

.comments-title {
  font-family: 'Plus Jakarta Sans', 'PingFang SC', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  display: flex;
  align-items: center;
  margin: 0;
}

.comments-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  border-radius: 12px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: 8px;
}

/* Comment input area */
.comment-input-area {
  display: flex;
  align-items: flex-start;
  margin-bottom: 32px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-input-wrapper {
  flex: 1;
}

.comment-input :deep(.q-field__control) {
  border-radius: 12px !important;
  background: #ffffff;
}

.comment-input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 10px;
}

.cancel-btn {
  color: #64748b;
  font-weight: 500;
  border-radius: 8px;
}

.submit-btn {
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

/* Comments list */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.comment-item {
  padding: 20px 0;
  border-bottom: 1px solid #f1f5f9;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-main {
  display: flex;
  align-items: flex-start;
}

.comment-author-avatar {
  flex-shrink: 0;
  margin-right: 14px;
  transition: transform 0.2s ease;
}

.comment-author-avatar:hover {
  transform: scale(1.05);
}

.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  flex-wrap: wrap;
  gap: 4px;
}

.comment-author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-author-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.comment-author-name:hover {
  color: #2563eb;
}

.author-badge {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
}

.author-badge.admin {
  background: #fef2f2;
  color: #ef4444;
}

.author-badge.you {
  background: #eff6ff;
  color: #2563eb;
}

.comment-time {
  font-size: 0.78rem;
  color: #94a3b8;
}

.comment-text {
  color: #475569;
  line-height: 1.7;
  margin: 0 0 10px 0;
  font-size: 0.92rem;
  word-wrap: break-word;
}

.comment-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.action-btn--danger:hover {
  background: #fef2f2;
  color: #ef4444;
}

/* Reply editor */
.reply-editor {
  display: flex;
  align-items: flex-start;
  margin-top: 14px;
  margin-left: 54px;
  padding: 14px;
  background: #f8fafc;
  border-radius: 12px;
}

.reply-input-wrapper {
  flex: 1;
}

.reply-input :deep(.q-field__control) {
  border-radius: 10px !important;
  background: #ffffff;
}

.reply-input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

/* Replies list */
.replies-list {
  margin-top: 14px;
  margin-left: 54px;
}

.reply-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 14px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 8px;
}

.reply-content {
  flex: 1;
  min-width: 0;
}

.reply-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  flex-wrap: wrap;
  gap: 4px;
}

.reply-author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.reply-author-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 0.88rem;
  transition: color 0.2s ease;
}

.reply-author-name:hover {
  color: #2563eb;
}

.reply-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.reply-text {
  color: #475569;
  line-height: 1.6;
  margin: 0 0 6px 0;
  font-size: 0.88rem;
  word-wrap: break-word;
}

.reply-actions {
  display: flex;
  gap: 8px;
}

.disabled-item {
  pointer-events: none;
  opacity: 0.4;
}

@media (max-width: 768px) {
  .comment-input-area {
    padding: 14px;
  }
  
  .reply-editor,
  .replies-list {
    margin-left: 0;
  }
  
  .reply-item {
    padding: 10px;
  }
  
  .comment-header-row,
  .reply-header-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
