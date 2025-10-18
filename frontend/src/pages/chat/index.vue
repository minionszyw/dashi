<template>
  <view class="chat-page">
    <!-- 消息列表 -->
    <scroll-view
      scroll-y
      class="message-list"
      :scroll-into-view="scrollToView"
      :scroll-with-animation="true"
    >
      <view v-if="chatStore.messages.length === 0" class="empty">
        <image src="/static/empty-chat.png" class="empty-icon" />
        <text class="empty-text">开始您的命理咨询吧~</text>
      </view>

      <view v-for="message in chatStore.messages" :key="message.id" :id="`msg-${message.id}`">
        <MessageBubble :message="message" />
      </view>

      <!-- AI正在输入... -->
      <view v-if="isAITyping" class="typing-indicator">
        <view class="typing-dots">
          <view class="dot" />
          <view class="dot" />
          <view class="dot" />
        </view>
      </view>
    </scroll-view>

    <!-- 输入区域 -->
    <ChatInput
      :disabled="isAITyping"
      placeholder="请输入您的问题..."
      @send="handleSend"
      @plus="handlePlus"
    />

    <!-- 加号菜单 -->
    <uni-popup ref="menuPopup" type="bottom">
      <view class="menu-container">
        <view class="menu-item" @click="handleNewConversation">
          <text class="icon">💬</text>
          <text>新建会话</text>
        </view>
        <view class="menu-item" @click="handleSelectBazi">
          <text class="icon">📊</text>
          <text>选择八字档案</text>
        </view>
        <view class="menu-item" @click="handleCancel">
          <text class="icon">❌</text>
          <text>取消</text>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { useChatStore, useUserStore } from '@/stores'
import MessageBubble from '@/components/MessageBubble.vue'
import ChatInput from '@/components/ChatInput.vue'
import { storage } from '@/utils/storage'

const chatStore = useChatStore()
const userStore = useUserStore()

const scrollToView = ref('')
const isAITyping = ref(false)
const menuPopup = ref()

onMounted(async () => {
  // 检查登录状态
  if (!userStore.isLogin) {
    uni.reLaunch({
      url: '/pages/login/index'
    })
    return
  }

  // 加载会话列表
  await chatStore.loadConversations()

  // 加载最近会话或创建新会话
  if (chatStore.conversations.length > 0) {
    await chatStore.switchConversation(chatStore.conversations[0].id)
  } else {
    await chatStore.newConversation()
  }

  scrollToBottom()
})

async function handleSend(text: string) {
  if (!chatStore.currentConversation) {
    uni.showToast({
      title: '请先创建会话',
      icon: 'none'
    })
    return
  }

  // 添加用户消息
  chatStore.addUserMessage(text)
  scrollToBottom()

  // 开始AI响应
  isAITyping.value = true
  const aiMessage = chatStore.addAIMessage()

  try {
    // 调用流式API
    await streamChat(text, aiMessage.id)
  } catch (error: any) {
    console.error('发送消息失败:', error)
    uni.showToast({
      title: error.message || '发送失败',
      icon: 'none'
    })
  } finally {
    isAITyping.value = false
  }
}

async function streamChat(text: string, tempMessageId: string) {
  const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const token = storage.getToken()

  return new Promise((resolve, reject) => {
    const requestTask = uni.request({
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
      success: (res) => {
        if (res.statusCode === 200) {
          // 处理SSE流式响应
          const data = res.data as string
          const lines = data.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const jsonStr = line.substring(6)
                const chunk = JSON.parse(jsonStr)

                if (chunk.type === 'token') {
                  // 追加内容
                  chatStore.appendAIMessageContent(tempMessageId, chunk.content)
                  scrollToBottom()
                } else if (chunk.type === 'done') {
                  // 完成
                  chatStore.finalizeAIMessage(
                    tempMessageId,
                    chunk.message_id,
                    chunk.token_cost
                  )
                  userStore.deductTokenBalance(chunk.token_cost)
                  resolve(true)
                } else if (chunk.type === 'error') {
                  reject(new Error(chunk.message))
                }
              } catch (e) {
                console.error('解析SSE数据失败:', e)
              }
            }
          }
        } else {
          reject(new Error('请求失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

function handlePlus() {
  menuPopup.value.open()
}

async function handleNewConversation() {
  menuPopup.value.close()
  try {
    await chatStore.newConversation()
    uni.showToast({
      title: '已创建新会话',
      icon: 'success'
    })
  } catch (error) {
    console.error('创建会话失败:', error)
  }
}

function handleSelectBazi() {
  menuPopup.value.close()
  uni.navigateTo({
    url: '/pages/bazi/list'
  })
}

function handleCancel() {
  menuPopup.value.close()
}

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
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.message-list {
  flex: 1;
  overflow-y: auto;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 200rpx 60rpx;

  .empty-icon {
    width: 200rpx;
    height: 200rpx;
    opacity: 0.5;
  }

  .empty-text {
    margin-top: 40rpx;
    font-size: 28rpx;
    color: #999;
  }
}

.typing-indicator {
  padding: 24rpx 32rpx;
}

.typing-dots {
  display: flex;
  gap: 12rpx;
  align-items: center;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: #999;
  animation: bounce 1.4s infinite ease-in-out both;

  &:nth-child(1) {
    animation-delay: -0.32s;
  }

  &:nth-child(2) {
    animation-delay: -0.16s;
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.menu-container {
  background: #fff;
  border-radius: 20rpx 20rpx 0 0;
  padding: 40rpx 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 32rpx 60rpx;
  font-size: 32rpx;

  .icon {
    font-size: 48rpx;
    margin-right: 24rpx;
  }

  &:active {
    background: #f5f5f5;
  }
}
</style>

