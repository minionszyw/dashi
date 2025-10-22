<template>
  <view class="session-page">
    <!-- 自定义导航栏 -->
    <view class="navbar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="navbar-content" :style="{ height: navBarHeight + 'px' }">
        <!-- 左侧新建按钮 -->
        <view class="navbar-left" @click="handleCreate">
          <text class="create-icon">+</text>
        </view>
        <!-- 标题 -->
        <text class="navbar-title">会话</text>
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
  // 分离置顶和未置顶的会话
  const pinned = chatStore.conversations.filter(c => pinnedIds.value.includes(c.id))
  const unpinned = chatStore.conversations.filter(c => !pinnedIds.value.includes(c.id))
  
  // 按时间倒序排序（最新的在前）
  const sortByTime = (a: Conversation, b: Conversation) => {
    const timeA = new Date(a.updated_at || a.created_at).getTime()
    const timeB = new Date(b.updated_at || b.created_at).getTime()
    return timeB - timeA
  }
  
  // 分别对置顶和未置顶的会话排序
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
async function handlePin(id: string) {
  const wasPinned = isPinned(id)
  
  // 立即关闭左滑状态
  swipingId.value = null
  await nextTick()
  
  if (wasPinned) {
    // 取消置顶
    pinnedIds.value = pinnedIds.value.filter(pid => pid !== id)
  } else {
    // 置顶
    pinnedIds.value.unshift(id)
  }
  
  // 保存到本地存储
  storage.set('pinned_conversations', pinnedIds.value)
  
  uni.showToast({
    title: wasPinned ? '已取消置顶' : '已置顶',
    icon: 'success',
    duration: 1500
  })
}

// 删除会话
async function handleDelete(id: string) {
  // 立即关闭左滑状态
  swipingId.value = null
  await nextTick()
  
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个会话吗？',
    success: async (res) => {
      if (res.confirm) {
        await chatStore.deleteConversation(id)
        // 同时从置顶列表中移除
        pinnedIds.value = pinnedIds.value.filter(pid => pid !== id)
        storage.set('pinned_conversations', pinnedIds.value)
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
  // 1. 如果有自定义标题且不是"新会话"，使用自定义标题
  if (conversation.title && conversation.title !== '新会话') {
    return conversation.title
  }
  
  // 2. 尝试从缓存中获取第一个用户问题
  const cached = conversationPreviews.value[conversation.id]
  if (cached?.firstQuestion) {
    return cached.firstQuestion
  }
  
  // 3. 显示创建时间作为标题（更友好）
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
  
  // 4. 最后才显示"新会话"
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
  
  // 3. 默认显示更友好的提示文本
  return '开始你的AI命理咨询'
}

// 加载会话预览信息
async function loadConversationPreviews() {
  // 从本地缓存读取
  const cached = storage.get<Record<string, { preview: string, firstQuestion: string }>>('conversation_previews')
  if (cached) {
    conversationPreviews.value = cached
  }
  
  // 异步加载缺少预览的会话（后台加载，不阻塞UI）
  loadMissingPreviews()
}

// 异步加载缺少预览的会话
async function loadMissingPreviews() {
  // 找出所有缺少预览的会话
  const conversationsNeedingPreview = chatStore.conversations.filter(conv => {
    const cached = conversationPreviews.value[conv.id]
    return !cached || (!cached.preview && !cached.firstQuestion)
  })
  
  // 如果没有需要加载的，直接返回
  if (conversationsNeedingPreview.length === 0) {
    return
  }
  
  // 逐个加载（限制并发数为3）
  const limit = 3
  for (let i = 0; i < conversationsNeedingPreview.length; i += limit) {
    const batch = conversationsNeedingPreview.slice(i, i + limit)
    await Promise.all(batch.map(async (conv) => {
      try {
        // 获取会话历史（只获取最后2条消息）
        const result = await getChatHistory(conv.id, { skip: 0, limit: 2 })
        
        if (result.messages && result.messages.length > 0) {
          // 找到第一条用户消息和最后一条消息
          const firstUserMsg = result.messages.find(m => m.role === 'user')
          const lastMsg = result.messages[result.messages.length - 1]
          
          if (!conversationPreviews.value[conv.id]) {
            conversationPreviews.value[conv.id] = { preview: '', firstQuestion: '' }
          }
          
          // 更新标题（第一条用户消息）
          if (firstUserMsg) {
            conversationPreviews.value[conv.id].firstQuestion = firstUserMsg.content.length > 20
              ? firstUserMsg.content.substring(0, 20) + '...'
              : firstUserMsg.content
          }
          
          // 更新预览（最后一条消息）
          conversationPreviews.value[conv.id].preview = lastMsg.content.length > 30
            ? lastMsg.content.substring(0, 30) + '...'
            : lastMsg.content
          
          // 保存到缓存
          storage.set('conversation_previews', conversationPreviews.value)
        }
      } catch (error: any) {
        // 静默失败，不影响用户体验
      }
    }))
  }
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
  background: #f7f8fa;
}

// ============================================
// 自定义导航栏
// ============================================

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  border-bottom: 1rpx solid $border-color;
  z-index: 999;
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
  justify-content: center;
  min-width: 80rpx;
  transition: all $duration-fast $ease-apple;
  
  &:active {
    opacity: 0.6;
  }
}

.create-icon {
  font-size: 56rpx;
  font-weight: 300;
  color: $primary;
  line-height: 1;
  margin-top: -6rpx;
}

.navbar-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 34rpx;
  font-weight: $font-weight-medium;
  color: $text-primary;
  white-space: nowrap;
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
