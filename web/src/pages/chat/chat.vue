<template>
  <view class="chat-container">
    <!-- 消息列表 -->
    <scroll-view 
      class="message-list" 
      scroll-y 
      :scroll-top="scrollTop"
    >
      <view v-if="messages.length === 0" class="empty-tips">
        <text class="empty-text">暂无消息</text>
      </view>
      
      <view v-for="msg in messages" :key="msg.id" class="message-item">
        <view v-if="msg.role === 'user'" class="message-user">
          <view class="message-content user-content">
            {{ msg.content }}
          </view>
          <image class="message-avatar" :src="userInfo?.avatar_url || '/static/avatar.png'" mode="aspectFill"></image>
        </view>
        
        <view v-else class="message-ai">
          <view class="ai-avatar">🔮</view>
          <view class="message-content ai-content">
            {{ msg.content }}
          </view>
        </view>
      </view>
    </scroll-view>
    
    <!-- 输入框 -->
    <view class="input-box">
      <input 
        v-model="inputText" 
        class="input-field" 
        placeholder="请输入您的问题..."
        confirm-type="send"
        @confirm="handleSend"
      />
      <button class="send-btn" @tap="handleSend" :disabled="!inputText.trim() || isLoading">
        发送
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSession, sendMessage } from '@/api/chat'
import type { ChatMessage } from '@/api/chat'
import type { UserInfo } from '@/api/auth'

const sessionId = ref(0)
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const isLoading = ref(false)
const scrollTop = ref(0)
const userInfo = ref<UserInfo | null>(null)

onMounted(async () => {
  // 获取用户信息
  userInfo.value = uni.getStorageSync('userInfo')
  
  // 获取会话ID
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  sessionId.value = Number(currentPage.options.sessionId)
  
  if (sessionId.value) {
    await loadSession()
  }
})

const loadSession = async () => {
  try {
    const { data } = await getSession(sessionId.value)
    messages.value = data.messages
    scrollToBottom()
  } catch (error) {
    console.error('获取会话失败:', error)
  }
}

const handleSend = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  const content = inputText.value.trim()
  inputText.value = ''
  
  // 添加用户消息
  const userMsg: ChatMessage = {
    id: Date.now(),
    session_id: sessionId.value,
    role: 'user',
    content,
    tokens_used: 0,
    created_at: new Date().toISOString()
  }
  messages.value.push(userMsg)
  scrollToBottom()
  
  // 发送消息
  isLoading.value = true
  try {
    const { data } = await sendMessage(sessionId.value, content)
    messages.value.push(data)
    scrollToBottom()
  } catch (error: any) {
    console.error('发送消息失败:', error)
    if (error.message === '余额不足') {
      uni.showModal({
        title: '余额不足',
        content: '您的余额不足，是否前往充值？',
        success: (res) => {
          if (res.confirm) {
            uni.switchTab({
              url: '/pages/profile/profile'
            })
          }
        }
      })
    }
  } finally {
    isLoading.value = false
  }
}

const scrollToBottom = () => {
  setTimeout(() => {
    scrollTop.value = 99999
  }, 100)
}
</script>

<style scoped>
.chat-container {
  height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.message-list {
  flex: 1;
  padding: 20rpx;
}

.empty-tips {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 200rpx 0;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.message-item {
  margin-bottom: 40rpx;
}

.message-user {
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}

.message-ai {
  display: flex;
  align-items: flex-start;
}

.message-avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  margin-left: 20rpx;
}

.ai-avatar {
  width: 72rpx;
  height: 72rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  margin-right: 20rpx;
}

.message-content {
  max-width: 500rpx;
  padding: 24rpx;
  border-radius: 16rpx;
  font-size: 28rpx;
  line-height: 1.6;
}

.user-content {
  background: #6366F1;
  color: #ffffff;
}

.ai-content {
  background: #ffffff;
  color: #333;
}

.input-box {
  background: #ffffff;
  padding: 20rpx;
  display: flex;
  align-items: center;
  border-top: 1rpx solid #eee;
}

.input-field {
  flex: 1;
  height: 72rpx;
  background: #f5f5f5;
  border-radius: 36rpx;
  padding: 0 32rpx;
  font-size: 28rpx;
}

.send-btn {
  margin-left: 20rpx;
  background: #6366F1;
  color: #ffffff;
  border-radius: 36rpx;
  height: 72rpx;
  line-height: 72rpx;
  padding: 0 40rpx;
  font-size: 28rpx;
}

.send-btn[disabled] {
  background: #ccc;
}
</style>

