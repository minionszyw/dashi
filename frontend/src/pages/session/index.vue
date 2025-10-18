<template>
  <view class="session-page">
    <view class="header">
      <text class="title">会话</text>
      <text v-if="!isEditMode" class="edit-btn" @click="toggleEditMode">编辑</text>
      <text v-else class="done-btn" @click="toggleEditMode">完成</text>
    </view>

    <scroll-view scroll-y class="session-list">
      <view v-if="chatStore.conversations.length === 0" class="empty">
        <image src="/static/empty-session.png" class="empty-icon" />
        <text class="empty-text">还没有会话记录</text>
        <button class="create-btn" @click="handleCreate">创建会话</button>
      </view>

      <view
        v-for="conversation in chatStore.conversations"
        :key="conversation.id"
        class="session-item"
        @click="handleSelect(conversation.id)"
      >
        <view v-if="isEditMode" class="checkbox">
          <checkbox
            :checked="selectedIds.includes(conversation.id)"
            @click.stop="toggleSelect(conversation.id)"
          />
        </view>

        <view class="session-content">
          <view class="session-header">
            <text class="session-title">{{ conversation.title }}</text>
            <text class="session-time">{{ formatTime(conversation.created_at) }}</text>
          </view>
          <text class="session-preview">{{ getPreview(conversation.id) }}</text>
        </view>

        <view v-if="!isEditMode" class="arrow">›</view>
      </view>
    </scroll-view>

    <!-- 编辑模式底部操作栏 -->
    <view v-if="isEditMode" class="edit-bar">
      <view class="select-all">
        <checkbox :checked="isAllSelected" @click="toggleSelectAll" />
        <text>全选</text>
      </view>
      <button class="delete-btn" :disabled="selectedIds.length === 0" @click="handleDelete">
        删除({{ selectedIds.length }})
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useChatStore } from '@/stores'
import { formatTime } from '@/utils/format'

const chatStore = useChatStore()

const isEditMode = ref(false)
const selectedIds = ref<string[]>([])

const isAllSelected = computed(() => {
  return selectedIds.value.length === chatStore.conversations.length && chatStore.conversations.length > 0
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
  if (isEditMode.value) {
    toggleSelect(id)
  } else {
    // 切换到对话页
    uni.switchTab({
      url: '/pages/chat/index'
    })
    // 切换会话
    chatStore.switchConversation(id)
  }
}

function handleCreate() {
  uni.switchTab({
    url: '/pages/chat/index'
  })
  chatStore.newConversation()
}

async function handleDelete() {
  if (selectedIds.value.length === 0) return

  uni.showModal({
    title: '确认删除',
    content: `确定要删除${selectedIds.value.length}个会话吗？`,
    success: async (res) => {
      if (res.confirm) {
        try {
          for (const id of selectedIds.value) {
            await chatStore.removeConversation(id)
          }
          selectedIds.value = []
          isEditMode.value = false
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          })
        } catch (error) {
          console.error('删除失败:', error)
          uni.showToast({
            title: '删除失败',
            icon: 'none'
          })
        }
      }
    }
  })
}

function getPreview(conversationId: string): string {
  const messages = chatStore.messages.filter(m => m.conversation_id === conversationId)
  if (messages.length === 0) return '开始对话...'
  const lastMessage = messages[messages.length - 1]
  return lastMessage.content.substring(0, 50) + (lastMessage.content.length > 50 ? '...' : '')
}
</script>

<style scoped lang="scss">
.session-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx;
  background: #fff;
  border-bottom: 1rpx solid #e5e5e5;

  .title {
    font-size: 36rpx;
    font-weight: bold;
  }

  .edit-btn,
  .done-btn {
    font-size: 28rpx;
    color: #07c160;
  }
}

.session-list {
  flex: 1;
  overflow-y: auto;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 200rpx 60rpx;

  .empty-icon {
    width: 200rpx;
    height: 200rpx;
    opacity: 0.5;
  }

  .empty-text {
    margin: 40rpx 0;
    font-size: 28rpx;
    color: #999;
  }

  .create-btn {
    width: 300rpx;
    height: 80rpx;
    background: #07c160;
    color: #fff;
    border-radius: 40rpx;
    font-size: 28rpx;

    &::after {
      border: none;
    }
  }
}

.session-item {
  display: flex;
  align-items: center;
  padding: 32rpx;
  background: #fff;
  border-bottom: 1rpx solid #e5e5e5;

  &:active {
    background: #f5f5f5;
  }
}

.checkbox {
  margin-right: 24rpx;
}

.session-content {
  flex: 1;
  min-width: 0;
}

.session-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.session-title {
  font-size: 32rpx;
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.session-time {
  font-size: 24rpx;
  color: #999;
  margin-left: 20rpx;
  flex-shrink: 0;
}

.session-preview {
  font-size: 26rpx;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.arrow {
  font-size: 48rpx;
  color: #ccc;
  margin-left: 20rpx;
}

.edit-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  background: #fff;
  border-top: 1rpx solid #e5e5e5;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 16rpx;
  font-size: 28rpx;
}

.delete-btn {
  background: #fa5151;
  color: #fff;
  border-radius: 40rpx;
  padding: 16rpx 48rpx;
  font-size: 28rpx;

  &::after {
    border: none;
  }

  &[disabled] {
    opacity: 0.5;
  }
}
</style>

