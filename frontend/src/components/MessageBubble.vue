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
        :src="userStore.user?.avatar_url || '/static/user-avatar.svg'" 
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

// 格式化消息时间
function formatMessageTime(timestamp: string): string {
  const now = new Date()
  const msgDate = new Date(timestamp)
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const msgDay = new Date(msgDate.getFullYear(), msgDate.getMonth(), msgDate.getDate())
  
  const diffDays = Math.floor((today.getTime() - msgDay.getTime()) / (24 * 60 * 60 * 1000))
  
  if (diffDays === 0) {
    return formatDateTime(timestamp, 'HH:mm')
  } else if (diffDays === 1) {
    return '昨天 ' + formatDateTime(timestamp, 'HH:mm')
  } else if (diffDays < 7) {
    const weekDays = ['日', '一', '二', '三', '四', '五', '六']
    return '星期' + weekDays[msgDate.getDay()] + ' ' + formatDateTime(timestamp, 'HH:mm')
  } else {
    return formatDateTime(timestamp, 'MM-DD HH:mm')
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/mixins.scss';
@import '@/styles/variables.scss';

.message-bubble {
  @include flex-center-y;
  align-items: flex-start;
  margin-bottom: $space-lg;
  animation: fadeIn 0.3s ease;

  // 用户消息（右侧）
  &.user {
    justify-content: flex-end;

    .bubble-wrapper {
      align-items: flex-end;
      margin-right: $space-md;
    }

    .bubble-content {
      background: $primary;
      border-radius: $radius-lg $radius-xs $radius-lg $radius-lg;
      
      .content {
        color: $text-inverse;
      }
    }

    .time {
      text-align: right;
    }
  }

  // AI消息（左侧）
  &.assistant {
    .bubble-wrapper {
      align-items: flex-start;
      margin-left: $space-md;
    }

    .bubble-content {
      background: $bg-card;
      border: 1rpx solid $border-light;
      border-radius: $radius-xs $radius-lg $radius-lg $radius-lg;
    }
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: $radius-base;
  flex-shrink: 0;
  background: $bg-hover;
}

.bubble-wrapper {
  @include flex-column;
  max-width: 70%;
  gap: $space-xs;
}

.bubble-content {
  padding: $space-base $space-lg;
  box-shadow: $shadow-sm;
}

.content {
  font-size: $font-base;
  line-height: 1.6;
  color: $text-primary;
  word-break: break-word;
  white-space: pre-wrap;
}

.time {
  font-size: $font-xs;
  color: $text-tertiary;
  padding: 0 $space-sm;
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
