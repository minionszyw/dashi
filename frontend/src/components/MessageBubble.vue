<template>
  <view :class="['message-bubble', message.role]">
    <!-- AI消息（左侧） -->
    <template v-if="message.role === 'assistant'">
      <image class="avatar" src="/static/ai-avatar.svg" mode="aspectFill" />
      <view class="bubble-wrapper">
        <view class="bubble-content">
          <text class="content">{{ message.content }}</text>
        </view>
        <text class="time">{{ formatMessageTime(message.created_at) }}</text>
      </view>
    </template>

    <!-- 用户消息（右侧） -->
    <template v-else>
      <view class="bubble-wrapper">
        <view class="bubble-content">
          <text class="content">{{ message.content }}</text>
        </view>
        <text class="time">{{ formatMessageTime(message.created_at) }}</text>
      </view>
      <image 
        class="avatar" 
        :src="userStore.user?.avatar_url || '/static/default-avatar.svg'" 
        mode="aspectFill" 
      />
    </template>
  </view>
 </template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Message } from '@/types'
import { formatDateTime } from '@/utils/format'
import { useUserStore } from '@/stores'

interface Props {
  message: Message
}

const props = defineProps<Props>()

const userStore = useUserStore()

// 格式化消息时间（微信样式：仅显示时分）
function formatMessageTime(timestamp: string): string {
  const now = new Date()
  const msgDate = new Date(timestamp)
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const msgDay = new Date(msgDate.getFullYear(), msgDate.getMonth(), msgDate.getDate())
  
  const diffDays = Math.floor((today.getTime() - msgDay.getTime()) / (24 * 60 * 60 * 1000))
  
  if (diffDays === 0) {
    // 今天：只显示时间
    return formatDateTime(timestamp, 'HH:mm')
  } else if (diffDays === 1) {
    // 昨天
    return '昨天 ' + formatDateTime(timestamp, 'HH:mm')
  } else if (diffDays < 7) {
    // 一周内：显示星期
    const weekDays = ['日', '一', '二', '三', '四', '五', '六']
    return '星期' + weekDays[msgDate.getDay()] + ' ' + formatDateTime(timestamp, 'HH:mm')
  } else {
    // 更早：显示日期
    return formatDateTime(timestamp, 'MM-DD HH:mm')
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/mixins.scss';
@import '@/styles/variables.scss';

.message-bubble {
  display: flex;
  align-items: flex-start;
  margin-bottom: $spacing-lg;
  animation: fadeIn 0.3s ease;

  // 用户消息（右侧）
  &.user {
    justify-content: flex-end;

    .bubble-wrapper {
      align-items: flex-end;
      margin-right: $spacing-md;
    }

    .bubble-content {
      background: #95ec69;
      border-radius: 10rpx 2rpx 10rpx 10rpx;
    }

    .time {
      text-align: right;
    }
  }

  // AI消息（左侧）
  &.assistant {
    .bubble-wrapper {
      align-items: flex-start;
      margin-left: $spacing-md;
    }

    .bubble-content {
      background: #ffffff;
      border-radius: 2rpx 10rpx 10rpx 10rpx;
    }
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 10rpx;
  flex-shrink: 0;
  background: #f0f2f5;
}

.bubble-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 70%; // 使用相对宽度，更好适配不同屏幕尺寸
  gap: $spacing-xs;
}

.bubble-content {
  padding: 20rpx 24rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.content {
  font-size: 30rpx;
  line-height: 1.6;
  color: $text-primary;
  word-break: break-word;
  white-space: pre-wrap;
}

.time {
  font-size: 20rpx;
  color: $text-tertiary;
  padding: 0 $spacing-sm;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

