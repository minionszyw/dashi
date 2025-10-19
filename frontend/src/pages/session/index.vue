<template>
  <view class="session-page">
    <!-- 页面标题栏 -->
    <view class="page-header">
      <text class="page-title">会话</text>
      <text 
        class="header-action" 
        @click="toggleEditMode"
      >
        {{ isEditMode ? '完成' : '管理' }}
      </text>
    </view>

    <!-- 会话列表 -->
    <scroll-view scroll-y class="session-list" :enhanced="true">
      <!-- 空状态 -->
      <view v-if="chatStore.conversations.length === 0" class="empty-state">
        <view class="empty-card fade-in">
          <view class="empty-icon">💬</view>
          <text class="empty-title">还没有会话记录</text>
          <text class="empty-desc">开始一段新的对话吧</text>
          <button class="create-button" @click="handleCreate">
            <text>创建会话</text>
          </button>
        </view>
      </view>

      <!-- 会话卡片 -->
      <view v-else class="sessions">
        <view
          v-for="(conversation, index) in chatStore.conversations"
          :key="conversation.id"
          class="session-card"
          :class="{ 'edit-mode': isEditMode }"
          @click="handleSelect(conversation.id)"
        >
          <!-- 选择框 -->
          <view v-if="isEditMode" class="checkbox-wrapper" @click.stop>
            <view 
              class="checkbox"
              :class="{ checked: selectedIds.includes(conversation.id) }"
              @click="toggleSelect(conversation.id)"
            >
              <text v-if="selectedIds.includes(conversation.id)" class="check-icon">✓</text>
            </view>
          </view>

          <!-- 会话内容 -->
          <view class="session-content">
            <view class="session-header">
              <text class="session-title">{{ conversation.title || '新会话' }}</text>
              <text class="session-time">{{ formatTime(conversation.updated_at) }}</text>
            </view>
            <text class="session-preview">{{ getLastMessage(conversation.id) }}</text>
            <view class="session-footer">
              <text class="message-count">{{ getMessageCount(conversation.id) }} 条消息</text>
            </view>
          </view>

          <!-- 箭头 -->
          <text v-if="!isEditMode" class="arrow">›</text>
        </view>
      </view>
    </scroll-view>

    <!-- 编辑模式底部栏 -->
    <view v-if="isEditMode" class="edit-toolbar safe-area-bottom">
      <view class="toolbar-left">
        <view class="select-all" @click="toggleSelectAll">
          <view class="checkbox" :class="{ checked: isAllSelected }">
            <text v-if="isAllSelected" class="check-icon">✓</text>
          </view>
          <text class="select-text">全选</text>
        </view>
      </view>
      <view class="toolbar-right">
        <button 
          class="delete-button"
          :class="{ disabled: selectedIds.length === 0 }"
          :disabled="selectedIds.length === 0"
          @click="handleDelete"
        >
          <text>删除{{ selectedIds.length > 0 ? `(${selectedIds.length})` : '' }}</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '@/stores'

const chatStore = useChatStore()

const isEditMode = ref(false)
const selectedIds = ref<string[]>([])

const isAllSelected = computed(() => {
  return selectedIds.value.length === chatStore.conversations.length && chatStore.conversations.length > 0
})

onMounted(async () => {
  await chatStore.loadConversations()
})

function toggleEditMode() {
  isEditMode.value = !isEditMode.value
  if (!isEditMode.value) {
    selectedIds.value = []
  }
}

function toggleSelect(id: string) {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) {
    selectedIds.value.splice(index, 1)
  } else {
    selectedIds.value.push(id)
  }
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value = []
  } else {
    selectedIds.value = chatStore.conversations.map(c => c.id)
  }
}

function handleSelect(id: string) {
  if (isEditMode.value) return
  
  chatStore.switchConversation(id)
  uni.switchTab({
    url: '/pages/chat/index'
  })
}

function handleCreate() {
  chatStore.newConversation()
  uni.switchTab({
    url: '/pages/chat/index'
  })
}

function handleDelete() {
  if (selectedIds.value.length === 0) return
  
  uni.showModal({
    title: '确认删除',
    content: `确定要删除${selectedIds.value.length}个会话吗？`,
    success: async (res) => {
      if (res.confirm) {
        for (const id of selectedIds.value) {
          await chatStore.deleteConversation(id)
        }
        selectedIds.value = []
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        })
      }
    }
  })
}

function getLastMessage(conversationId: string): string {
  const messages = chatStore.getConversationMessages(conversationId)
  if (messages.length === 0) return '暂无消息'
  const lastMsg = messages[messages.length - 1]
  return lastMsg.content.substring(0, 50) + (lastMsg.content.length > 50 ? '...' : '')
}

function getMessageCount(conversationId: string): number {
  return chatStore.getConversationMessages(conversationId).length
}

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return `${date.getMonth() + 1}月${date.getDate()}日`
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.session-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: $bg-page;
}

// ============================================
// 页面头部
// ============================================

.page-header {
  background: $bg-card;
  padding: $spacing-lg $spacing-base;
  @include flex-between;
  border-bottom: 1rpx solid $border-color;
}

.page-title {
  font-size: $font-size-xxl;
  font-weight: $font-weight-bold;
  color: $text-primary;
}

.header-action {
  font-size: $font-size-md;
  color: $primary;
  padding: $spacing-sm $spacing-base;
  
  &:active {
    opacity: 0.7;
  }
}

// ============================================
// 会话列表
// ============================================

.session-list {
  flex: 1;
  overflow-y: auto;
}

.sessions {
  padding: $spacing-base;
}

.session-card {
  @include card;
  @include flex-center-y;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;
  transition: all $duration-base $ease-apple;
  animation: fadeInUp $duration-base $ease-apple backwards;
  
  &:nth-child(n) {
    animation-delay: calc(0.05s * (n - 1));
  }
  
  &.edit-mode {
    padding-left: $spacing-base;
  }
  
  &:not(.edit-mode):active {
    transform: scale(0.98);
    background: $bg-hover;
  }
}

.checkbox-wrapper {
  margin-right: $spacing-base;
}

.checkbox {
  width: 44rpx;
  height: 44rpx;
  border: 3rpx solid $border-color;
  border-radius: $radius-round;
  @include flex-center;
  transition: all $duration-fast $ease-apple;
  
  &.checked {
    background: $primary;
    border-color: $primary;
  }
}

.check-icon {
  font-size: $font-size-md;
  font-weight: $font-weight-bold;
  color: #ffffff;
}

.session-content {
  flex: 1;
  min-width: 0;
}

.session-header {
  @include flex-between;
  margin-bottom: $spacing-sm;
}

.session-title {
  font-size: $font-size-md;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  @include ellipsis;
  flex: 1;
  margin-right: $spacing-base;
}

.session-time {
  font-size: $font-size-xs;
  color: $text-tertiary;
  flex-shrink: 0;
}

.session-preview {
  font-size: $font-size-sm;
  color: $text-secondary;
  @include ellipsis-multi(2);
  line-height: 1.5;
  margin-bottom: $spacing-sm;
}

.session-footer {
  @include flex-center-y;
}

.message-count {
  font-size: $font-size-xs;
  color: $text-tertiary;
}

.arrow {
  font-size: 48rpx;
  color: $text-disabled;
  margin-left: $spacing-base;
  font-weight: $font-weight-light;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  padding: 200rpx $spacing-xl;
}

.empty-card {
  text-align: center;
}

.empty-icon {
  font-size: 128rpx;
  margin-bottom: $spacing-xl;
  opacity: 0.5;
}

.empty-title {
  display: block;
  font-size: $font-size-lg;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.empty-desc {
  display: block;
  font-size: $font-size-base;
  color: $text-secondary;
  margin-bottom: $spacing-xxl;
}

.create-button {
  @include btn-primary;
  width: 400rpx;
  height: 80rpx;
  margin: 0 auto;
}

// ============================================
// 编辑工具栏
// ============================================

.edit-toolbar {
  background: $bg-card;
  border-top: 1rpx solid $border-color;
  padding: $spacing-base;
  @include flex-between;
  @include safe-area-bottom;
}

.toolbar-left {
  flex: 1;
}

.select-all {
  @include flex-center-y;
  gap: $spacing-md;
  
  &:active {
    opacity: 0.7;
  }
}

.select-text {
  font-size: $font-size-base;
  color: $text-primary;
}

.toolbar-right {
  margin-left: $spacing-base;
}

.delete-button {
  @include btn-secondary;
  height: 64rpx;
  padding: 0 $spacing-xl;
  color: $error;
  border-color: $error;
  
  &.disabled {
    opacity: 0.5;
  }
  
  &:not(.disabled):active {
    background: rgba($error, 0.1);
  }
}

// ============================================
// 动画
// ============================================

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
