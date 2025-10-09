<template>
  <view class="sessions-container">
    <view v-if="sessions.length === 0" class="empty">
      <text class="empty-icon">📝</text>
      <text class="empty-text">暂无对话记录</text>
    </view>
    
    <view v-else class="sessions-list">
      <view 
        v-for="session in sessions" 
        :key="session.id" 
        class="session-item"
        @tap="viewSession(session.id)"
      >
        <view class="session-icon">💬</view>
        <view class="session-info">
          <view class="session-title">{{ session.title || '未命名对话' }}</view>
          <view class="session-time">{{ formatTime(session.updated_at) }}</view>
        </view>
        <view class="session-actions">
          <text class="action-btn" @tap.stop="deleteSessionConfirm(session.id)">删除</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSessions, deleteSession } from '@/api/chat'
import type { ChatSession } from '@/api/chat'

const sessions = ref<ChatSession[]>([])

onMounted(() => {
  loadSessions()
})

const loadSessions = async () => {
  try {
    const { data } = await getSessions()
    sessions.value = data
  } catch (error) {
    console.error('获取会话列表失败:', error)
  }
}

const viewSession = (sessionId: number) => {
  uni.navigateTo({
    url: `/pages/chat/chat?sessionId=${sessionId}`
  })
}

const deleteSessionConfirm = (sessionId: number) => {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个对话吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deleteSession(sessionId)
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          })
          loadSessions()
        } catch (error) {
          console.error('删除会话失败:', error)
        }
      }
    }
  })
}

const formatTime = (time: string) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  } else if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  } else {
    return date.toLocaleDateString()
  }
}
</script>

<style scoped>
.sessions-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 200rpx 0;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 40rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.sessions-list {
  padding: 20rpx;
}

.session-item {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
}

.session-icon {
  font-size: 48rpx;
  margin-right: 24rpx;
}

.session-info {
  flex: 1;
}

.session-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.session-time {
  font-size: 24rpx;
  color: #999;
}

.session-actions {
  margin-left: 20rpx;
}

.action-btn {
  color: #ff4d4f;
  font-size: 28rpx;
}
</style>

