<template>
  <view :class="['message-bubble', message.role]">
    <!-- AI消息 -->
    <template v-if="message.role === 'assistant'">
      <view class="avatar emoji">🤖</view>
      <view class="bubble-content">
        <text class="content">{{ message.content }}</text>
        <text class="time">{{ formatTime(message.created_at) }}</text>
      </view>
    </template>

    <!-- 用户消息 -->
    <template v-else>
      <view class="bubble-content">
        <text class="content">{{ message.content }}</text>
        <text class="time">{{ formatTime(message.created_at) }}</text>
      </view>
      <view class="avatar emoji">🧑</view>
    </template>
  </view>
 </template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Message } from '@/types'
import { formatTime } from '@/utils/format'
import { useUserStore } from '@/stores'

interface Props {
  message: Message
}

const props = defineProps<Props>()

const userStore = useUserStore()

// 使用表情占位，避免本地静态资源路径在小程序下 500
const userAvatar = computed(() => userStore.user?.avatar_url || '')
</script>

<style scoped lang="scss">
@import '@/styles/mixins.scss';

.message-bubble {
  display: flex;
  align-items: flex-start;
  margin: 24rpx 32rpx;
  animation: fadeIn 0.3s ease;

  &.user {
    flex-direction: row-reverse;

    .bubble-content {
      background: #95ec69;
      margin-right: 20rpx;
    }
  }

  &.assistant {
    .bubble-content {
      background: #ffffff;
      margin-left: 20rpx;
    }
  }
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 10rpx;
  flex-shrink: 0;
}

.emoji {
  @include flex-center;
  background: #f0f2f5;
  font-size: 40rpx;
}

.bubble-content {
  max-width: 500rpx;
  padding: 20rpx 24rpx;
  border-radius: 10rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.content {
  font-size: 30rpx;
  line-height: 1.6;
  word-break: break-all;
  white-space: pre-wrap;
}

.time {
  font-size: 22rpx;
  color: #999;
  margin-top: 12rpx;
  align-self: flex-end;
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

