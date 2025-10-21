<template>
  <view class="chat-page">
    <!-- 自定义导航栏（对齐胶囊按钮） -->
    <view class="navbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="navbar-content" :style="{ height: navBarHeight + 'px' }">
        <view class="navbar-left" @click="goBack">
          <text class="back-icon">‹</text>
        </view>
        <text class="navbar-title">{{ chatStore.currentConversation?.title || '新会话' }}</text>
        <view class="navbar-right" :style="{ width: menuButtonWidth + 'px' }">
          <view class="icon-button" @click="handleMore">
            <text class="icon">⋮</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 消息列表 -->
    <scroll-view
      scroll-y
      class="message-list"
      :style="{ paddingTop: (statusBarHeight + navBarHeight) + 'px' }"
      :scroll-into-view="scrollToView"
      :scroll-with-animation="true"
      :enhanced="true"
      :bounces="true"
    >
      <!-- 空状态 -->
      <view v-if="chatStore.messages.length === 0" class="empty-state">
        <view class="empty-card fade-in">
          <view class="empty-icon">
            <image src="/static/empty-chat.svg" mode="aspectFit" />
          </view>
          <text class="empty-title">开始您的命理咨询</text>
          <text class="empty-desc">我是您的AI命理助手，可以为您解答命理问题</text>
          
          <!-- 快速开始 -->
          <view class="quick-start">
            <text class="quick-title">常见问题</text>
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
        <view class="tool-btn" @click="handleMore" v-if="!canSend">
          <text class="tool-icon">➕</text>
        </view>
        <input
          v-model="inputText"
          class="input-field"
          type="text"
          :placeholder="isAITyping ? 'AI正在思考中...' : ''"
          placeholder="说点什么..."
          :disabled="isAITyping"
          confirm-type="send"
          @confirm="handleSend"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
        />
        <view 
          class="send-btn"
          :class="{ active: canSend }"
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
// 导航栏相关
const statusBarHeight = ref(0) // 状态栏高度
const navBarHeight = ref(44) // 导航栏内容高度
const menuButtonWidth = ref(87) // 胶囊按钮区域宽度

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

  // 获取系统信息和胶囊按钮位置（微信小程序）
  // #ifdef MP-WEIXIN
  try {
    const systemInfo = uni.getSystemInfoSync()
    const menuButtonInfo = uni.getMenuButtonBoundingClientRect()
    
    // 状态栏高度
    statusBarHeight.value = systemInfo.statusBarHeight || 0
    
    // 导航栏内容高度（胶囊按钮高度 + 上下间距）
    navBarHeight.value = menuButtonInfo.height + (menuButtonInfo.top - statusBarHeight.value) * 2
    
    // 胶囊按钮区域宽度（屏幕宽度 - 胶囊左边距）
    menuButtonWidth.value = systemInfo.windowWidth - menuButtonInfo.left
  } catch (e) {
    console.error('获取胶囊位置失败:', e)
  }
  // #endif
  
  // #ifndef MP-WEIXIN
  // 非微信小程序环境使用默认值
  const systemInfo = uni.getSystemInfoSync()
  statusBarHeight.value = systemInfo.statusBarHeight || 20
  // #endif

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
    console.log('✅ 更新会话标题:', conversationId, truncatedQuestion)
  }
  
  // 更新预览（最新的用户消息）
  const truncatedPreview = userMessage.length > 30 
    ? userMessage.substring(0, 30) + '...' 
    : userMessage
  cached[conversationId].preview = truncatedPreview
  console.log('✅ 更新会话预览:', conversationId, truncatedPreview)
  
  // 保存到本地存储
  storage.set('conversation_previews', cached)
}

// 快速问题
function handleQuickQuestion(question: string) {
  inputText.value = question
  handleSend()
}

// 流式对话（使用微信原生API支持流式响应）
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
        buffer = lines.pop() || '' // 保留不完整的行

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.substring(6).trim()
              if (!jsonStr) continue
              
              const data = JSON.parse(jsonStr)

              if (data.type === 'token') {
                // 追加内容
                chatStore.appendAIMessageContent(tempMessageId, data.content)
                scrollToBottom()
              } else if (data.type === 'done') {
                // 完成
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
          
          // 删除当前会话
          if (oldConversationId) {
            await chatStore.deleteConversation(oldConversationId)
          }
          
          // 创建新会话
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

// 返回上一页
function goBack() {
  uni.navigateBack({
    delta: 1
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
  display: flex;
  flex-direction: column;
  background: #ededed;
}

// ============================================
// 导航栏（微信风格，对齐胶囊按钮）
// ============================================

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  border-bottom: 1rpx solid $border-color;
  z-index: 100;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $spacing-base;
  position: relative;
}

.navbar-left {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 80rpx;
  flex-shrink: 0;
  z-index: 1;
  
  &:active {
    opacity: 0.7;
  }
}

.back-icon {
  font-size: 48rpx;
  color: $text-primary;
  font-weight: 300;
  line-height: 1;
  margin-top: -4rpx;
}

.navbar-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 32rpx;
  font-weight: $font-weight-medium;
  color: $text-primary;
  white-space: nowrap;
  max-width: 400rpx;
  @include ellipsis;
}

.navbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.icon-button {
  width: 60rpx;
  height: 60rpx;
  @include flex-center;
  border-radius: $radius-base;
  transition: all $duration-fast $ease-apple;
  
  &:active {
    background: rgba(0, 0, 0, 0.05);
  }
}

.icon {
  font-size: 36rpx;
  color: $text-primary;
  font-weight: $font-weight-bold;
}

// ============================================
// 消息列表
// ============================================

.message-list {
  flex: 1;
  overflow-y: auto;
}

.messages {
  padding: $spacing-base;
}

.message-wrapper {
  margin-bottom: $spacing-base;
  animation: fadeInUp $duration-base $ease-apple;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  padding: 120rpx $spacing-xl $spacing-xl;
}

.empty-card {
  text-align: center;
}

.empty-icon {
  width: 200rpx;
  height: 200rpx;
  margin: 0 auto $spacing-xl;
  opacity: 0.6;
}

.empty-title {
  display: block;
  font-size: $font-size-xl;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.empty-desc {
  display: block;
  font-size: $font-size-base;
  color: $text-secondary;
  line-height: 1.6;
}

// 快速开始
.quick-start {
  margin-top: $spacing-xxxl;
}

.quick-title {
  display: block;
  font-size: $font-size-sm;
  color: $text-tertiary;
  margin-bottom: $spacing-base;
  text-align: left;
}

.quick-buttons {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.quick-button {
  @include card;
  padding: $spacing-base $spacing-lg;
  text-align: left;
  transition: all $duration-base $ease-apple;
  
  &:active {
    transform: scale(0.98);
    background: $bg-hover;
  }
}

.quick-text {
  font-size: $font-size-base;
  color: $text-primary;
}

// ============================================
// 输入区域（微信风格）
// ============================================

.input-area {
  background: #f7f7f7;
  border-top: 1rpx solid #d9d9d9;
  @include safe-area-bottom;
}

.input-container {
  padding: 16rpx;
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.tool-btn {
  width: 56rpx;
  height: 56rpx;
  @include flex-center;
  flex-shrink: 0;
  transition: all $duration-fast $ease-apple;
  
  &:active {
    opacity: 0.6;
  }
}

.tool-icon {
  font-size: 44rpx;
  color: $text-secondary;
}

.input-field {
  flex: 1;
  min-width: 0;
  background: #ffffff;
  border-radius: 8rpx;
  padding: 14rpx $spacing-base;
  font-size: 30rpx;
  line-height: 1.4;
  color: $text-primary;
  height: 72rpx;
  
  &::placeholder {
    color: #999999;
  }
}

.send-btn {
  background: #d9d9d9;
  border-radius: 8rpx;
  padding: 0 32rpx;
  height: 72rpx;
  @include flex-center;
  flex-shrink: 0;
  transition: all $duration-fast $ease-apple;
  
  &.active {
    background: $primary;
    
    &:active {
      opacity: 0.8;
    }
  }
}

.send-text {
  font-size: 28rpx;
  color: #ffffff;
  font-weight: $font-weight-medium;
  white-space: nowrap;
}

// ============================================
// 功能菜单
// ============================================

.menu-popup {
  padding: $spacing-base;
  animation: slideUp $duration-base $ease-apple;
}

.menu-content {
  background: $bg-card;
  border-radius: $radius-xl;
  overflow: hidden;
}

.menu-title {
  padding: $spacing-lg;
  text-align: center;
  font-size: $font-size-sm;
  color: $text-tertiary;
  border-bottom: 1rpx solid $border-color;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: $spacing-xl $spacing-base;
  gap: $spacing-lg;
}

.menu-item {
  @include flex-center;
  flex-direction: column;
  gap: $spacing-sm;
  
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
}

.menu-icon {
  font-size: 48rpx;
}

.menu-label {
  font-size: $font-size-xs;
  color: $text-secondary;
}

.menu-cancel {
  height: 96rpx;
  @include flex-center;
  font-size: $font-size-md;
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
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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
