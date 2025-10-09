<template>
  <view class="chat-container">
    <!-- 自定义导航栏 -->
    <view class="custom-navbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="navbar-content">
        <text class="navbar-title">{{ sessionTitle }}</text>
        <view class="navbar-right">
          <text class="balance">余额: {{ balance }}</text>
        </view>
      </view>
    </view>
    
    <!-- 消息列表 -->
    <scroll-view 
      class="message-list" 
      scroll-y 
      :scroll-top="scrollTop"
      :style="{ height: `calc(100vh - ${statusBarHeight + 44}px - 120rpx)` }"
    >
      <view v-if="messages.length === 0" class="empty-tips">
        <text class="empty-icon">💬</text>
        <text class="empty-text">开始您的命理咨询之旅</text>
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
      
      <!-- 加载中 -->
      <view v-if="isLoading" class="message-item">
        <view class="message-ai">
          <view class="ai-avatar">🔮</view>
          <view class="message-content ai-content">
            <text class="typing">正在思考中...</text>
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
import { ref, onMounted, computed } from 'vue'
import { createSession, sendMessage, getSession } from '@/api/chat'
import { getBalance } from '@/api/billing'
import type { ChatMessage } from '@/api/chat'
import type { UserInfo } from '@/api/auth'

const statusBarHeight = ref(0)
const sessionId = ref(0)
const sessionTitle = ref('新对话')
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const isLoading = ref(false)
const scrollTop = ref(0)
const balance = ref(0)
const userInfo = ref<UserInfo | null>(null)

onMounted(async () => {
  // 获取状态栏高度
  const systemInfo = uni.getSystemInfoSync()
  statusBarHeight.value = systemInfo.statusBarHeight || 0
  
  // 检查登录状态
  const token = uni.getStorageSync('token')
  if (!token) {
    uni.reLaunch({
      url: '/pages/login/login'
    })
    return
  }
  
  // 获取用户信息
  userInfo.value = uni.getStorageSync('userInfo')
  
  // 创建新会话
  await initSession()
  
  // 获取余额
  await loadBalance()
})

const initSession = async () => {
  try {
    const { data } = await createSession('新对话')
    sessionId.value = data.id
    sessionTitle.value = data.title || '新对话'
  } catch (error) {
    console.error('创建会话失败:', error)
  }
}

const loadBalance = async () => {
  try {
    const { data } = await getBalance()
    balance.value = data.balance
  } catch (error) {
    console.error('获取余额失败:', error)
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
    
    // 更新余额
    await loadBalance()
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

.custom-navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.navbar-content {
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32rpx;
}

.navbar-title {
  font-size: 36rpx;
  font-weight: bold;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.balance {
  font-size: 24rpx;
  background: rgba(255, 255, 255, 0.2);
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
}

.message-list {
  flex: 1;
  padding: 20rpx;
}

.empty-tips {
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

.typing {
  color: #999;
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
