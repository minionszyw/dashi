<template>
  <view class="session-page">
    <!-- 顶部导航（对齐胶囊按钮） -->
    <view class="navbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="navbar-content" :style="{ height: navBarHeight + 'px' }">
        <!-- 左侧创建按钮 -->
        <view class="navbar-left" @click="handleCreate">
          <text class="plus-icon">+</text>
        </view>
        <!-- 中间标题 -->
        <text class="page-title">会话</text>
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
        <view class="empty-card">
          <view class="empty-icon">💬</view>
          <text class="empty-title">还没有会话记录</text>
          <text class="empty-desc">点击左上角 + 开始新对话</text>
        </view>
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
              @click.stop="handlePin(conversation.id)"
            >
              <text class="action-text">{{ isPinned(conversation.id) ? '取消' : '置顶' }}</text>
            </view>
            <view class="action-btn action-delete" @click.stop="handleDelete(conversation.id)">
              <text class="action-text">删除</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useChatStore } from '@/stores'
import { storage } from '@/utils/storage'
import type { Conversation } from '@/types'

const chatStore = useChatStore()

// 导航栏相关
const statusBarHeight = ref(0) // 状态栏高度
const navBarHeight = ref(44) // 导航栏内容高度
const menuButtonWidth = ref(87) // 胶囊按钮区域宽度

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

// 排序后的会话列表（置顶优先）
const sortedConversations = computed(() => {
  const pinned = chatStore.conversations.filter(c => pinnedIds.value.includes(c.id))
  const unpinned = chatStore.conversations.filter(c => !pinnedIds.value.includes(c.id))
  return [...pinned, ...unpinned]
})

onMounted(async () => {
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
  // 重新加载会话预览信息（从本地缓存）
  loadConversationPreviews()
  
  // 如果当前会话有消息，更新其预览
  if (chatStore.currentConversation && chatStore.messages.length > 0) {
    const conversationId = chatStore.currentConversation.id
    const lastMsg = chatStore.messages[chatStore.messages.length - 1]
    const firstMsg = chatStore.messages.find(m => m.role === 'user')
    
    if (!conversationPreviews.value[conversationId]) {
      conversationPreviews.value[conversationId] = { preview: '', firstQuestion: '' }
    }
    
    // 更新预览
    conversationPreviews.value[conversationId].preview = lastMsg.content.length > 30 
      ? lastMsg.content.substring(0, 30) + '...' 
      : lastMsg.content
    
    // 更新标题（如果有第一条用户消息）
    if (firstMsg && !conversationPreviews.value[conversationId].firstQuestion) {
      conversationPreviews.value[conversationId].firstQuestion = firstMsg.content.length > 20 
        ? firstMsg.content.substring(0, 20) + '...' 
        : firstMsg.content
    }
    
    storage.set('conversation_previews', conversationPreviews.value)
  }
})

// 获取item样式（两个按钮，总宽280rpx）
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

// 触摸开始
function handleTouchStart(e: any, id: string) {
  touchStartX.value = e.touches[0].pageX
  touchStartY.value = e.touches[0].pageY
  activeId.value = id
  isSwiping.value = false
  
  // 关闭其他项
  if (swipingId.value && swipingId.value !== id) {
    swipingId.value = null
  }
}

// 触摸移动
function handleTouchMove(e: any, id: string) {
  if (activeId.value !== id) return
  
  const deltaX = e.touches[0].pageX - touchStartX.value
  const deltaY = e.touches[0].pageY - touchStartY.value
  
  // 判断是否为横向滑动
  if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
    isSwiping.value = true
    e.stopPropagation() // 阻止事件冒泡，避免触发点击
  }
  
  if (isSwiping.value && deltaX < -30) {
    // 左滑超过30px，显示操作按钮
    swipingId.value = id
  } else if (deltaX > 30) {
    // 右滑关闭
    swipingId.value = null
  }
}

// 触摸结束
function handleTouchEnd(e: any, id: string) {
  // 如果不是滑动操作，且没有打开的左滑项，则允许点击
  if (!isSwiping.value && !swipingId.value) {
    // 正常点击，不做处理
  }
  activeId.value = ''
  isSwiping.value = false
}

// 点击scroll-view空白区域
function handleScrollViewClick(e: any) {
  // 如果有左滑项，关闭它
  if (swipingId.value) {
    swipingId.value = null
  }
}

// 点击会话
function handleSelect(id: string) {
  // 如果点击的是已打开左滑的项，关闭左滑
  if (swipingId.value === id) {
    swipingId.value = null
    return
  }
  
  // 如果有其他项正在左滑，先关闭
  if (swipingId.value && swipingId.value !== id) {
    swipingId.value = null
    return
  }
  
  chatStore.switchConversation(id)
  uni.navigateTo({
    url: '/pages/chat/index'
  })
}

// 新建会话（优化：先跳转，后台异步创建）
async function handleCreate() {
  // 先跳转，提升用户体验
  uni.navigateTo({
    url: '/pages/chat/index'
  })
  
  // 后台创建会话
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

// 判断是否置顶
function isPinned(conversationId: string): boolean {
  return pinnedIds.value.includes(conversationId)
}

// 置顶/取消置顶
function handlePin(id: string) {
  const wasPinned = isPinned(id)
  
  if (wasPinned) {
    // 取消置顶
    pinnedIds.value = pinnedIds.value.filter(pid => pid !== id)
  } else {
    // 置顶
    pinnedIds.value.unshift(id)
  }
  // 保存到本地存储
  storage.set('pinned_conversations', pinnedIds.value)
  swipingId.value = null
  
  uni.showToast({
    title: wasPinned ? '已取消置顶' : '已置顶',
    icon: 'success',
    duration: 1500
  })
}

// 删除会话
function handleDelete(id: string) {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个会话吗？',
    success: async (res) => {
      if (res.confirm) {
        await chatStore.deleteConversation(id)
        // 同时从置顶列表中移除
        pinnedIds.value = pinnedIds.value.filter(pid => pid !== id)
        storage.set('pinned_conversations', pinnedIds.value)
        swipingId.value = null
        uni.showToast({
          title: '删除成功',
          icon: 'success'
        })
      }
    }
  })
}

// 获取会话标题（智能显示）
function getConversationTitle(conversation: Conversation): string {
  // 如果有自定义标题且不是"新会话"，使用自定义标题
  if (conversation.title && conversation.title !== '新会话') {
    return conversation.title
  }
  
  // 否则显示第一个用户问题（如果有缓存）
  const cached = conversationPreviews.value[conversation.id]
  if (cached && cached.firstQuestion) {
    return cached.firstQuestion
  }
  
  // 最后才显示"新会话"
  return '新会话'
}

// 获取会话预览文本
function getConversationPreview(conversationId: string): string {
  // 1. 首先从缓存中获取
  const cached = conversationPreviews.value[conversationId]
  if (cached?.preview) {
    return cached.preview
  }
  
  // 2. 如果是当前会话，从messages中获取最新消息
  if (chatStore.currentConversation?.id === conversationId) {
    const messages = chatStore.messages
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1]
      const preview = lastMsg.content.length > 30 
        ? lastMsg.content.substring(0, 30) + '...' 
        : lastMsg.content
      // 同时更新缓存
      if (!conversationPreviews.value[conversationId]) {
        conversationPreviews.value[conversationId] = { preview: '', firstQuestion: '' }
      }
      conversationPreviews.value[conversationId].preview = preview
      storage.set('conversation_previews', conversationPreviews.value)
      return preview
    }
  }
  
  // 3. 默认显示提示文本
  return '点击开始对话'
}

// 加载会话预览信息
async function loadConversationPreviews() {
  // 从本地缓存读取
  const cached = storage.get<Record<string, { preview: string, firstQuestion: string }>>('conversation_previews')
  if (cached) {
    conversationPreviews.value = cached
  }
  
  // TODO: 可以后续从后端API批量获取最新消息
}

// 格式化时间
function formatTime(dateStr: string): string {
  if (!dateStr) return ''
  
  try {
    const date = new Date(dateStr)
    // 检查日期是否有效
    if (isNaN(date.getTime())) return ''
    
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    
    const minute = 60 * 1000
    const hour = 60 * minute
    const day = 24 * hour
    
    if (diff < 0) return '' // 未来时间，返回空
    if (diff < minute) return '刚刚'
    if (diff < hour) return `${Math.floor(diff / minute)}分钟前`
    
    // 今天
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    
    if (messageDate.getTime() === today.getTime()) {
      const hours = date.getHours()
      const minutes = date.getMinutes()
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
    }
    
    // 昨天
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    if (messageDate.getTime() === yesterday.getTime()) {
      return '昨天'
    }
    
    // 一周内
    if (diff < 7 * day) {
      const weekdays = ['日', '一', '二', '三', '四', '五', '六']
      return `星期${weekdays[date.getDay()]}`
    }
    
    // 今年
    if (date.getFullYear() === now.getFullYear()) {
      return `${date.getMonth() + 1}月${date.getDate()}日`
    }
    
    // 更早
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
  display: flex;
  flex-direction: column;
  background: #ededed;
}

// ============================================
// 顶部导航（微信风格，对齐胶囊按钮）
// ============================================

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #ededed;
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
  transition: all $duration-fast $ease-apple;
  
  &:active {
    opacity: 0.6;
  }
}

.page-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 34rpx;
  font-weight: $font-weight-medium;
  color: $text-primary;
  white-space: nowrap;
}

.navbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
}

.plus-icon {
  font-size: 56rpx;
  font-weight: 300;
  color: $text-primary;
  line-height: 1;
  margin-top: -8rpx;
}

// ============================================
// 会话列表
// ============================================

.session-list {
  flex: 1;
  overflow-y: auto;
  background: #ffffff;
}

.sessions {
  // 无padding，贴边显示
}

.session-item-wrapper {
  position: relative;
  overflow: hidden;
  
  &.is-pinned {
    background: linear-gradient(90deg, rgba(255, 249, 230, 0.5) 0%, rgba(255, 255, 255, 1) 10%);
  }
}

.session-item {
  @include flex-center-y;
  padding: $spacing-lg $spacing-base;
  background: #ffffff;
  border-bottom: 1rpx solid $border-color;
  position: relative;
  z-index: 2;
  
  &:active {
    background: $bg-hover;
  }
}

.pin-badge {
  font-size: 24rpx;
  margin-right: $spacing-sm;
  flex-shrink: 0;
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
  font-size: 32rpx;
  font-weight: $font-weight-medium;
  color: $text-primary;
  @include ellipsis;
  flex: 1;
  margin-right: $spacing-base;
}

.session-time {
  font-size: 24rpx;
  color: $text-tertiary;
  flex-shrink: 0;
}

.session-preview {
  font-size: 28rpx;
  color: $text-secondary;
  @include ellipsis;
  line-height: 1.4;
}

.arrow {
  font-size: 44rpx;
  color: $text-disabled;
  margin-left: $spacing-base;
  font-weight: 300;
}

// ============================================
// 左滑操作按钮（置顶 + 删除）
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
  color: #ffffff;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  
  &:active {
    opacity: 0.8;
  }
}

.action-pin {
  background: $warning;
}

.action-delete {
  background: $error;
}

.action-text {
  color: #ffffff;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  padding: 200rpx $spacing-xl;
  background: #ffffff;
}

.empty-card {
  text-align: center;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: $spacing-xl;
  opacity: 0.5;
}

.empty-title {
  display: block;
  font-size: $font-size-lg;
  font-weight: $font-weight-medium;
  color: $text-primary;
  margin-bottom: $spacing-sm;
}

.empty-desc {
  display: block;
  font-size: $font-size-base;
  color: $text-secondary;
}
</style>
