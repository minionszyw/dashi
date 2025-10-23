<template>
  <view class="chat-page">
    <!-- 消息列表 -->
    <scroll-view
      scroll-y
      class="message-list"
      :scroll-into-view="scrollToView"
      :scroll-with-animation="true"
      :enhanced="true"
      :bounces="true"
    >
      <!-- 空状态 -->
      <view v-if="chatStore.messages.length === 0" class="empty-state">
        <view class="empty-card fade-in">
          <view class="empty-icon-wrapper">
            <image src="/static/empty-chat.svg" mode="aspectFit" class="empty-icon" />
          </view>
          <text class="empty-title">开始您的命理咨询</text>
          <text class="empty-desc">我是您的AI命理助手，为您提供专业的命理分析</text>
          
          <!-- 快速开始 -->
          <view class="quick-start">
            <view class="quick-title-wrapper">
              <view class="quick-line"></view>
              <text class="quick-title">常见咨询</text>
              <view class="quick-line"></view>
            </view>
            <view class="quick-buttons">
              <view 
                v-for="(q, i) in quickQuestions" 
                :key="i"
                class="quick-button"
                @click="handleQuickQuestion(q)"
              >
                <text class="quick-text">{{ q }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 消息列表 -->
      <view v-else class="messages">
        <view 
          v-for="message in chatStore.messages" 
          :key="message.id" 
          :id="`msg-${message.id}`"
          class="message-wrapper"
        >
          <MessageBubble :message="message" />
        </view>
      </view>
    </scroll-view>

    <!-- 输入区域 -->
    <view class="input-area safe-area-bottom">
      <view class="input-container">
        <view 
          class="tool-btn" 
          @click="handleMore"
        >
          <text class="tool-icon">＋</text>
        </view>
        <input
          v-model="inputText"
          class="input-field"
          type="text"
          :placeholder="isAITyping ? 'AI正在思考中...' : '说点什么...'"
          :disabled="isAITyping"
          :adjust-position="false"
          confirm-type="send"
          @confirm="handleSend"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
        />
        <view 
          class="send-btn"
          :class="{ active: canSend, disabled: !canSend }"
          @click="handleSend"
        >
          <text class="send-text">发送</text>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <uni-popup ref="menuPopup" type="bottom" background-color="transparent">
      <view class="menu-popup">
        <view class="menu-content">
          <view class="menu-title">更多功能</view>
          <view class="menu-grid">
            <view class="menu-item" @click="handleNewConversation">
              <view class="menu-icon-wrapper">
                <text class="menu-icon">💬</text>
              </view>
              <text class="menu-label">新建会话</text>
            </view>
            <view class="menu-item" @click="handleClearChat">
              <view class="menu-icon-wrapper">
                <text class="menu-icon">🗑️</text>
              </view>
              <text class="menu-label">清空对话</text>
            </view>
          </view>
          <view class="menu-cancel" @click="handleCloseMenu">
            <text>取消</text>
          </view>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useChatStore, useUserStore } from '@/stores'
import MessageBubble from '@/components/MessageBubble.vue'
import { storage } from '@/utils/storage'

const chatStore = useChatStore()
const userStore = useUserStore()

const inputText = ref('')
const scrollToView = ref('')
const isAITyping = ref(false)
const menuPopup = ref()
const isInputFocused = ref(false)

// 快速问题
const quickQuestions = [
  '我的事业运势如何？',
  '今年的财运怎么样？',
  '帮我分析一下感情运势',
  '我适合什么行业？'
]

// 是否可以发送
const canSend = computed(() => {
  return inputText.value.trim().length > 0 && !isAITyping.value
})

onMounted(async () => {
  // 检查登录状态
  if (!userStore.isLogin) {
    uni.reLaunch({
      url: '/pages/login/index'
    })
    return
  }

  // 加载会话（如果有当前会话）
  if (chatStore.currentConversation) {
    scrollToBottom()
  }
})

// 发送消息
async function handleSend() {
  const text = inputText.value.trim()
  if (!canSend.value || !text) return

  if (!chatStore.currentConversation) {
    uni.showToast({
      title: '请先创建会话',
      icon: 'none'
    })
    return
  }

  const conversationId = chatStore.currentConversation.id
  const isFirstMessage = chatStore.messages.length === 0

  // 清空输入框
  inputText.value = ''

  // 添加用户消息
  chatStore.addUserMessage(text)
  scrollToBottom()

  // 开始AI响应
  isAITyping.value = true
  const aiMessage = chatStore.addAIMessage()

  try {
    // 调用流式API
    await streamChat(text, aiMessage.id)
    
    // 更新会话预览缓存
    updateConversationPreview(conversationId, text, isFirstMessage)
  } catch (error: any) {
    console.error('发送消息失败:', error)
    uni.showToast({
      title: error.message || '发送失败',
      icon: 'none'
    })
    // 移除失败的消息
    chatStore.removeMessage(aiMessage.id)
  } finally {
    isAITyping.value = false
  }
}

// 更新会话预览缓存
function updateConversationPreview(conversationId: string, userMessage: string, isFirst: boolean) {
  const cached = storage.get<Record<string, { preview: string, firstQuestion: string }>>('conversation_previews') || {}
  
  if (!cached[conversationId]) {
    cached[conversationId] = {
      preview: '',
      firstQuestion: ''
    }
  }
  
  // 如果是第一条消息或之前没有记录firstQuestion，记录为标题
  if (isFirst || !cached[conversationId].firstQuestion) {
    const truncatedQuestion = userMessage.length > 20
      ? userMessage.substring(0, 20) + '...'
      : userMessage
    cached[conversationId].firstQuestion = truncatedQuestion
  }
  
  // 更新预览（最新的用户消息）
  const truncatedPreview = userMessage.length > 30
    ? userMessage.substring(0, 30) + '...'
    : userMessage
  cached[conversationId].preview = truncatedPreview
  
  // 保存到本地存储
  storage.set('conversation_previews', cached)
}

// 快速问题
function handleQuickQuestion(question: string) {
  inputText.value = question
  handleSend()
}

// 流式对话
async function streamChat(text: string, tempMessageId: string) {
  const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const token = storage.getToken()

  return new Promise((resolve, reject) => {
    let buffer = ''
    
    const requestTask = wx.request({
      url: `${BASE_URL}/api/v1/chat/message`,
      method: 'POST',
      data: {
        conversation_id: chatStore.currentConversation?.id,
        content: text
      },
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      enableChunked: true,
      success: (res: any) => {
        if (res.statusCode !== 200) {
          reject(new Error(res.data?.message || '请求失败'))
        }
      },
      fail: (err: any) => {
        console.error('请求失败:', err)
        reject(err)
      }
    })

    // 监听流式数据
    requestTask.onChunkReceived((res: any) => {
      try {
        const chunk = String.fromCharCode.apply(null, new Uint8Array(res.data) as any)
        buffer += chunk
        
        // 按行处理SSE数据
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.substring(6).trim()
              if (!jsonStr) continue
              
              const data = JSON.parse(jsonStr)

              if (data.type === 'token') {
                chatStore.appendAIMessageContent(tempMessageId, data.content)
                scrollToBottom()
              } else if (data.type === 'done') {
                chatStore.finalizeAIMessage(
                  tempMessageId,
                  data.message_id,
                  data.token_cost
                )
                userStore.deductTokenBalance(data.token_cost)
                resolve(true)
              } else if (data.type === 'error') {
                reject(new Error(data.message))
              }
            } catch (e) {
              console.error('解析SSE数据失败:', line, e)
            }
          }
        }
      } catch (e) {
        console.error('处理chunk失败:', e)
      }
    })
  })
}

// 输入框聚焦/失焦
function handleInputFocus() {
  isInputFocused.value = true
}

function handleInputBlur() {
  isInputFocused.value = false
}

// 更多功能
function handleMore() {
  menuPopup.value.open()
}

function handleCloseMenu() {
  menuPopup.value.close()
}

// 新建会话
async function handleNewConversation() {
  menuPopup.value.close()
  try {
    await chatStore.newConversation()
    uni.showToast({
      title: '已创建新会话',
      icon: 'success',
      duration: 1500
    })
    scrollToBottom()
  } catch (error) {
    console.error('创建会话失败:', error)
    uni.showToast({
      title: '创建失败',
      icon: 'none'
    })
  }
}

// 清空对话
async function handleClearChat() {
  menuPopup.value.close()
  uni.showModal({
    title: '确认清空',
    content: '确定要清空当前对话吗？此操作不可恢复',
    success: async (res) => {
      if (res.confirm) {
        try {
          const oldConversationId = chatStore.currentConversation?.id
          
          if (oldConversationId) {
            await chatStore.deleteConversation(oldConversationId)
          }
          
          await chatStore.newConversation()
          
          uni.showToast({
            title: '已清空',
            icon: 'success'
          })
          
          scrollToBottom()
        } catch (error) {
          console.error('清空对话失败:', error)
          uni.showToast({
            title: '清空失败',
            icon: 'none'
          })
        }
      }
    }
  })
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (chatStore.messages.length > 0) {
      const lastMsg = chatStore.messages[chatStore.messages.length - 1]
      scrollToView.value = `msg-${lastMsg.id}`
    }
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.chat-page {
  height: 100vh;
  @include flex-column;
  background: $bg-page;
}

// ============================================
// 消息列表
// ============================================

.message-list {
  flex: 1;
  overflow-y: auto;
}

.messages {
  padding: $space-base;
}

.message-wrapper {
  margin-bottom: $space-base;
  animation: fadeInUp $duration-base ease;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  padding: 120rpx $space-xl $space-xl;
}

.empty-card {
  text-align: center;
}

.empty-icon-wrapper {
  width: 200rpx;
  height: 200rpx;
  margin: 0 auto $space-xl;
}

.empty-icon {
  width: 100%;
  height: 100%;
}

.empty-title {
  display: block;
  font-size: $font-xl;
  font-weight: $weight-semibold;
  color: $text-primary;
  margin-bottom: $space-sm;
}

.empty-desc {
  display: block;
  font-size: $font-base;
  color: $text-secondary;
  line-height: 1.6;
}

// 快速开始
.quick-start {
  margin-top: $space-xxxl;
}

.quick-title-wrapper {
  @include flex-center-y;
  gap: $space-base;
  margin-bottom: $space-lg;
}

.quick-line {
  flex: 1;
  height: 1rpx;
  background: linear-gradient(to right, transparent, $border-color, transparent);
}

.quick-title {
  font-size: $font-sm;
  color: $text-tertiary;
  letter-spacing: 2rpx;
}

.quick-buttons {
  @include flex-column;
  gap: $space-md;
}

.quick-button {
  @include card-bordered;
  padding: $space-base $space-lg;
  text-align: left;
  transition: all $duration-base ease;
  
  &:active {
    transform: scale(0.98);
    background: $bg-hover;
    border-color: $accent;
  }
}

.quick-text {
  font-size: $font-base;
  color: $text-secondary;
}

// ============================================
// 输入区域
// ============================================

.input-area {
  background: $bg-card;
  border-top: 1rpx solid $border-color;
  @include safe-area-bottom;
}

.input-container {
  display: flex;
  align-items: flex-end;
  padding: $space-base;
  gap: $space-md;
  box-sizing: border-box;
}

.tool-btn {
  width: 64rpx;
  height: 72rpx;
  @include flex-center;
  flex-shrink: 0;
  background: $bg-page;
  border-radius: $radius-base;
  transition: background $duration-fast;
  
  &:active {
    background: $bg-hover;
  }
}

.tool-icon {
  font-size: 40rpx;
  color: $text-secondary;
  font-weight: 300;
}

.input-field {
  flex: 1;
  min-width: 0;
  background: $bg-page;
  border: 1rpx solid $border-color;
  border-radius: $radius-base;
  padding: $space-md $space-base;
  font-size: $font-base;
  line-height: 1.5;
  color: $text-primary;
  height: 72rpx;
  box-sizing: border-box;
}

.send-btn {
  width: 120rpx;
  height: 72rpx;
  border-radius: $radius-base;
  @include flex-center;
  flex-shrink: 0;
  transition: all $duration-base ease;
  
  &.disabled {
    background: $bg-hover;
    border: 1rpx solid $border-color;
    
    .send-text {
      color: $text-disabled;
    }
  }
  
  &.active {
    background: $primary;
    border: none;
    
    .send-text {
      color: $text-inverse;
    }
    
    &:active {
      opacity: 0.9;
      transform: scale(0.98);
    }
  }
}

.send-text {
  font-size: $font-base;
  font-weight: $weight-medium;
}

// ============================================
// 功能菜单
// ============================================

.menu-popup {
  padding: $space-base;
  animation: slideUp $duration-base ease;
}

.menu-content {
  background: $bg-card;
  border-radius: $radius-xl;
  overflow: hidden;
}

.menu-title {
  padding: $space-lg;
  text-align: center;
  font-size: $font-sm;
  color: $text-tertiary;
  border-bottom: 1rpx solid $border-color;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: $space-xl $space-base;
  gap: $space-lg;
}

.menu-item {
  @include flex-center;
  flex-direction: column;
  gap: $space-sm;
  
  &:active {
    opacity: 0.7;
  }
}

.menu-icon-wrapper {
  width: 96rpx;
  height: 96rpx;
  @include flex-center;
  background: $bg-page;
  border-radius: $radius-lg;
  border: 1rpx solid $border-light;
}

.menu-icon {
  font-size: 48rpx;
}

.menu-label {
  font-size: $font-xs;
  color: $text-secondary;
}

.menu-cancel {
  height: 96rpx;
  @include flex-center;
  font-size: $font-md;
  color: $text-secondary;
  border-top: 1rpx solid $border-color;
  
  &:active {
    background: $bg-hover;
  }
}

// ============================================
// 动画
// ============================================

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

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

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
