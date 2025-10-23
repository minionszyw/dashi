<template>
  <view class="session-page">
    <!-- 自定义导航栏 -->
    <view class="navbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="navbar-content" :style="{ height: navBarHeight + 'px' }">
        <!-- 左侧新建按钮 -->
        <view class="navbar-left" @click="handleCreate">
          <text class="create-icon">＋</text>
        </view>
        <!-- 标题 -->
        <text class="navbar-title">会话列表</text>
        <!-- 右侧预留胶囊空间 -->
        <view class="navbar-right" :style="{ width: menuButtonWidth + 'px' }"></view>
      </view>
    </view>

    <!-- 会话列表 -->
    <scroll-view 
      scroll-y 
      class="session-list" 
      :style="{ paddingTop: (statusBarHeight + navBarHeight) + 'px' }"
      :enhanced="true"
      @tap="handleScrollViewClick"
    >
      <!-- 空状态 -->
      <view v-if="chatStore.conversations.length === 0" class="empty-state">
        <view class="empty-icon">💬</view>
        <text class="empty-title">还没有会话记录</text>
        <text class="empty-desc">点击左上角 ＋ 开始新对话</text>
      </view>

      <!-- 会话列表（左滑操作，置顶会话优先） -->
      <view v-else class="sessions">
        <view
          v-for="conversation in sortedConversations"
          :key="conversation.id"
          class="session-item-wrapper"
          :class="{ 'is-pinned': isPinned(conversation.id) }"
        >
          <!-- 会话项（可左滑） -->
          <view
            class="session-item"
            :style="getItemStyle(conversation.id)"
            @touchstart="handleTouchStart($event, conversation.id)"
            @touchmove="handleTouchMove($event, conversation.id)"
            @touchend="handleTouchEnd($event, conversation.id)"
            @click="handleSelect(conversation.id)"
          >
            <!-- 置顶标识 -->
            <view v-if="isPinned(conversation.id)" class="pin-badge">📌</view>
            
            <!-- 头像 -->
            <image class="session-avatar" src="/static/ai-avatar.svg" mode="aspectFill" />
            
            <!-- 会话内容 -->
            <view class="session-content">
              <view class="session-header">
                <text class="session-title">{{ getConversationTitle(conversation) }}</text>
                <text class="session-time">{{ formatTime(conversation.updated_at || conversation.created_at) }}</text>
              </view>
              <text class="session-preview">{{ getConversationPreview(conversation.id) }}</text>
            </view>
            <text class="arrow">›</text>
          </view>

          <!-- 左滑操作按钮 -->
          <view class="swipe-actions">
            <view 
              class="action-btn action-pin" 
              @tap.stop="handlePin(conversation.id)"
            >
              <text class="action-text">{{ isPinned(conversation.id) ? '取消' : '置顶' }}</text>
            </view>
            <view class="action-btn action-delete" @tap.stop="handleDelete(conversation.id)">
              <text class="action-text">删除</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useChatStore } from '@/stores'
import { storage } from '@/utils/storage'
import { getChatHistory } from '@/api'
import type { Conversation } from '@/types'

const chatStore = useChatStore()

// 导航栏相关
const statusBarHeight = ref(0)
const navBarHeight = ref(44)
const menuButtonWidth = ref(87)

// 置顶相关
const pinnedIds = ref<string[]>([])

// 左滑相关
const swipingId = ref<string | null>(null)
const touchStartX = ref(0)
const touchStartY = ref(0)
const currentX = ref(0)
const isSwiping = ref(false)
const activeId = ref<string>('')

// 会话消息缓存（用于显示预览）
const conversationPreviews = ref<Record<string, { preview: string, firstQuestion: string }>>({})

// 排序后的会话列表（置顶优先，然后按时间倒序）
const sortedConversations = computed(() => {
  const pinned = chatStore.conversations.filter(c => pinnedIds.value.includes(c.id))
  const unpinned = chatStore.conversations.filter(c => !pinnedIds.value.includes(c.id))
  
  const sortByTime = (a: Conversation, b: Conversation) => {
    const timeA = new Date(a.updated_at || a.created_at).getTime()
    const timeB = new Date(b.updated_at || b.created_at).getTime()
    return timeB - timeA
  }
  
  pinned.sort(sortByTime)
  unpinned.sort(sortByTime)
  
  return [...pinned, ...unpinned]
})

onMounted(async () => {
  // 获取系统信息和胶囊按钮位置
  // #ifdef MP-WEIXIN
  try {
    const systemInfo = uni.getSystemInfoSync()
    const menuButtonInfo = uni.getMenuButtonBoundingClientRect()
    
    statusBarHeight.value = systemInfo.statusBarHeight || 0
    navBarHeight.value = menuButtonInfo.height + (menuButtonInfo.top - statusBarHeight.value) * 2
    menuButtonWidth.value = systemInfo.windowWidth - menuButtonInfo.left
  } catch (e) {
    // 静默失败
  }
  // #endif
  
  // #ifndef MP-WEIXIN
  const systemInfo = uni.getSystemInfoSync()
  statusBarHeight.value = systemInfo.statusBarHeight || 20
  // #endif
  
  // 加载置顶列表
  const savedPinnedIds = storage.get<string[]>('pinned_conversations')
  if (savedPinnedIds) {
    pinnedIds.value = savedPinnedIds
  }

  // 加载会话列表
  await chatStore.loadConversations()
  
  // 加载会话预览信息
  loadConversationPreviews()
})

// 页面显示时刷新预览数据
onShow(() => {
  loadConversationPreviews()
  
  if (chatStore.currentConversation && chatStore.messages.length > 0) {
    const conversationId = chatStore.currentConversation.id
    const lastMsg = chatStore.messages[chatStore.messages.length - 1]
    const firstMsg = chatStore.messages.find(m => m.role === 'user')
    
    if (!conversationPreviews.value[conversationId]) {
      conversationPreviews.value[conversationId] = { preview: '', firstQuestion: '' }
    }
    
    conversationPreviews.value[conversationId].preview = lastMsg.content.length > 30 
      ? lastMsg.content.substring(0, 30) + '...' 
      : lastMsg.content
    
    if (firstMsg && !conversationPreviews.value[conversationId].firstQuestion) {
      conversationPreviews.value[conversationId].firstQuestion = firstMsg.content.length > 20 
        ? firstMsg.content.substring(0, 20) + '...' 
        : firstMsg.content
    }
    
    storage.set('conversation_previews', conversationPreviews.value)
  }
})

function getItemStyle(id: string) {
  if (swipingId.value === id) {
    return {
      transform: 'translateX(-280rpx)',
      transition: 'transform 0.3s ease'
    }
  }
  return {
    transform: 'translateX(0)',
    transition: 'transform 0.3s ease'
  }
}

function handleTouchStart(e: any, id: string) {
  touchStartX.value = e.touches[0].pageX
  touchStartY.value = e.touches[0].pageY
  activeId.value = id
  isSwiping.value = false
  
  if (swipingId.value && swipingId.value !== id) {
    swipingId.value = null
  }
}

function handleTouchMove(e: any, id: string) {
  if (activeId.value !== id) return
  
  const deltaX = e.touches[0].pageX - touchStartX.value
  const deltaY = e.touches[0].pageY - touchStartY.value
  
  if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
    isSwiping.value = true
    e.stopPropagation()
  }
  
  if (isSwiping.value && deltaX < -30) {
    swipingId.value = id
  } else if (deltaX > 30) {
    swipingId.value = null
  }
}

function handleTouchEnd(e: any, id: string) {
  activeId.value = ''
  isSwiping.value = false
}

function handleScrollViewClick(e: any) {
  if (swipingId.value) {
    swipingId.value = null
  }
}

function handleSelect(id: string) {
  if (swipingId.value === id) {
    swipingId.value = null
    return
  }
  
  if (swipingId.value && swipingId.value !== id) {
    swipingId.value = null
    return
  }
  
  chatStore.switchConversation(id)
  uni.navigateTo({
    url: '/pages/chat/index'
  })
}

async function handleCreate() {
  uni.navigateTo({
    url: '/pages/chat/index'
  })
  
  try {
    await chatStore.newConversation()
  } catch (error) {
    console.error('创建会话失败:', error)
    uni.showToast({
      title: '创建失败',
      icon: 'none'
    })
  }
}

function isPinned(conversationId: string): boolean {
  return pinnedIds.value.includes(conversationId)
}

async function handlePin(id: string) {
  const wasPinned = isPinned(id)
  
  // 先执行置顶操作
  if (wasPinned) {
    pinnedIds.value = pinnedIds.value.filter(pid => pid !== id)
  } else {
    pinnedIds.value.unshift(id)
  }
  
  storage.set('pinned_conversations', pinnedIds.value)
  
  // 操作完成后关闭滑动
  await nextTick()
  swipingId.value = null
  
  uni.showToast({
    title: wasPinned ? '已取消置顶' : '已置顶',
    icon: 'success',
    duration: 1500
  })
}

async function handleDelete(id: string) {
  const targetId = id
  
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个会话吗？',
    success: async (res) => {
      if (res.confirm) {
        // 确认删除时才关闭滑动
        await nextTick()
        swipingId.value = null
        
        // 执行删除
        await chatStore.deleteConversation(targetId)
        pinnedIds.value = pinnedIds.value.filter(pid => pid !== targetId)
        storage.set('pinned_conversations', pinnedIds.value)
        
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        })
      } else {
        // 取消删除时也关闭滑动
        await nextTick()
        swipingId.value = null
      }
    }
  })
}

function getConversationTitle(conversation: Conversation): string {
  if (conversation.title && conversation.title !== '新会话') {
    return conversation.title
  }
  
  const cached = conversationPreviews.value[conversation.id]
  if (cached?.firstQuestion) {
    return cached.firstQuestion
  }
  
  const createDate = new Date(conversation.created_at)
  if (!isNaN(createDate.getTime())) {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const msgDay = new Date(createDate.getFullYear(), createDate.getMonth(), createDate.getDate())
    
    if (msgDay.getTime() === today.getTime()) {
      return '今天的对话'
    } else if (msgDay.getTime() === today.getTime() - 24 * 60 * 60 * 1000) {
      return '昨天的对话'
    } else {
      return `${createDate.getMonth() + 1}月${createDate.getDate()}日的对话`
    }
  }
  
  return '新会话'
}

function getConversationPreview(conversationId: string): string {
  const cached = conversationPreviews.value[conversationId]
  if (cached?.preview) {
    return cached.preview
  }
  
  if (chatStore.currentConversation?.id === conversationId) {
    const messages = chatStore.messages
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1]
      const preview = lastMsg.content.length > 30 
        ? lastMsg.content.substring(0, 30) + '...' 
        : lastMsg.content
      if (!conversationPreviews.value[conversationId]) {
        conversationPreviews.value[conversationId] = { preview: '', firstQuestion: '' }
      }
      conversationPreviews.value[conversationId].preview = preview
      storage.set('conversation_previews', conversationPreviews.value)
      return preview
    }
  }
  
  return '开始你的AI命理咨询'
}

async function loadConversationPreviews() {
  const cached = storage.get<Record<string, { preview: string, firstQuestion: string }>>('conversation_previews')
  if (cached) {
    conversationPreviews.value = cached
  }
  
  loadMissingPreviews()
}

async function loadMissingPreviews() {
  const conversationsNeedingPreview = chatStore.conversations.filter(conv => {
    const cached = conversationPreviews.value[conv.id]
    return !cached || (!cached.preview && !cached.firstQuestion)
  })
  
  if (conversationsNeedingPreview.length === 0) {
    return
  }
  
  const limit = 3
  for (let i = 0; i < conversationsNeedingPreview.length; i += limit) {
    const batch = conversationsNeedingPreview.slice(i, i + limit)
    await Promise.all(batch.map(async (conv) => {
      try {
        const result = await getChatHistory(conv.id, { skip: 0, limit: 2 })
        
        if (result.messages && result.messages.length > 0) {
          const firstUserMsg = result.messages.find(m => m.role === 'user')
          const lastMsg = result.messages[result.messages.length - 1]
          
          if (!conversationPreviews.value[conv.id]) {
            conversationPreviews.value[conv.id] = { preview: '', firstQuestion: '' }
          }
          
          if (firstUserMsg) {
            conversationPreviews.value[conv.id].firstQuestion = firstUserMsg.content.length > 20
              ? firstUserMsg.content.substring(0, 20) + '...'
              : firstUserMsg.content
          }
          
          conversationPreviews.value[conv.id].preview = lastMsg.content.length > 30
            ? lastMsg.content.substring(0, 30) + '...'
            : lastMsg.content
          
          storage.set('conversation_previews', conversationPreviews.value)
        }
      } catch (error: any) {
        // 静默失败
      }
    }))
  }
}

function formatTime(dateStr: string): string {
  if (!dateStr) return ''
  
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return ''
    
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    
    const minute = 60 * 1000
    const hour = 60 * minute
    const day = 24 * hour
    
    if (diff < 0) return ''
    if (diff < minute) return '刚刚'
    if (diff < hour) return `${Math.floor(diff / minute)}分钟前`
    
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    
    if (messageDate.getTime() === today.getTime()) {
      const hours = date.getHours()
      const minutes = date.getMinutes()
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
    }
    
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    if (messageDate.getTime() === yesterday.getTime()) {
      return '昨天'
    }
    
    if (diff < 7 * day) {
      const weekdays = ['日', '一', '二', '三', '四', '五', '六']
      return `星期${weekdays[date.getDay()]}`
    }
    
    if (date.getFullYear() === now.getFullYear()) {
      return `${date.getMonth() + 1}月${date.getDate()}日`
    }
    
    return `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
  } catch (e) {
    console.error('时间格式化失败:', dateStr, e)
    return ''
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.session-page {
  height: 100vh;
  @include flex-column;
  background: $bg-page;
}

// ============================================
// 自定义导航栏
// ============================================

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: $bg-card;
  border-bottom: 1rpx solid $border-color;
  z-index: 999;
}

.navbar-content {
  @include flex-between;
  padding: 0 $space-base;
  position: relative;
}

.navbar-left {
  @include flex-center;
  min-width: 80rpx;
  transition: opacity $duration-fast;
  
  &:active {
    opacity: 0.6;
  }
}

.create-icon {
  font-size: 64rpx;
  font-weight: 300;
  color: $accent;
  line-height: 1;
}

.navbar-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: $font-md;
  font-weight: $weight-medium;
  color: $text-primary;
}

.navbar-right {
  flex-shrink: 0;
}

// ============================================
// 会话列表
// ============================================

.session-list {
  flex: 1;
  overflow-y: auto;
}

.sessions {
  background: $bg-card;
}

.session-item-wrapper {
  position: relative;
  overflow: hidden;
  
  &.is-pinned {
    background: linear-gradient(90deg, rgba(201, 168, 124, 0.05) 0%, $bg-card 20%);
  }
}

.session-item {
  @include flex-center-y;
  padding: $space-lg $space-base;
  background: $bg-card;
  border-bottom: 1rpx solid $border-light;
  position: relative;
  z-index: 2;
  
  &:active {
    background: $bg-hover;
  }
}

.pin-badge {
  font-size: 24rpx;
  margin-right: $space-sm;
  flex-shrink: 0;
}

.session-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: $radius-lg;
  background: $bg-page;
  margin-right: $space-md;
  flex-shrink: 0;
  border: 1rpx solid $border-color;
}

.session-content {
  flex: 1;
  min-width: 0;
}

.session-header {
  @include flex-between;
  margin-bottom: $space-sm;
}

.session-title {
  font-size: $font-md;
  font-weight: $weight-medium;
  color: $text-primary;
  @include text-ellipsis;
  flex: 1;
  margin-right: $space-base;
}

.session-time {
  font-size: $font-xs;
  color: $text-tertiary;
  flex-shrink: 0;
}

.session-preview {
  font-size: $font-sm;
  color: $text-secondary;
  @include text-ellipsis;
  line-height: 1.4;
}

.arrow {
  font-size: 44rpx;
  color: $text-disabled;
  margin-left: $space-base;
  font-weight: 300;
}

// ============================================
// 左滑操作按钮
// ============================================

.swipe-actions {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 280rpx;
  display: flex;
  align-items: stretch;
  z-index: 1;
}

.action-btn {
  width: 140rpx;
  @include flex-center;
  color: $text-inverse;
  font-size: $font-sm;
  font-weight: $weight-medium;
  
  &:active {
    opacity: 0.8;
  }
}

.action-pin {
  background: $accent;
  
  .action-text {
    color: $text-primary;
  }
}

.action-delete {
  background: $primary-dark;
}

.action-text {
  color: $text-inverse;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  @include flex-center;
  flex-direction: column;
  padding: 200rpx $space-xl;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: $space-xl;
  opacity: 0.3;
}

.empty-title {
  font-size: $font-lg;
  font-weight: $weight-medium;
  color: $text-primary;
  margin-bottom: $space-sm;
}

.empty-desc {
  font-size: $font-base;
  color: $text-secondary;
}
</style>
