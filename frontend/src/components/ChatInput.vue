<template>
  <view class="chat-input">
    <view class="input-container">
      <view class="plus-btn" @click="handlePlus">
        <text class="icon">+</text>
      </view>
      <view class="input-wrapper">
        <textarea
          v-model="inputText"
          class="input"
          :placeholder="placeholder"
          :disabled="disabled"
          :auto-height="true"
          :maxlength="2000"
          @confirm="handleSend"
        />
      </view>
      <view
        :class="['send-btn', { active: canSend }]"
        @click="handleSend"
      >
        <text>发送</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  placeholder?: string
  disabled?: boolean
}

interface Emits {
  (e: 'send', text: string): void
  (e: 'plus'): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请输入消息...',
  disabled: false
})

const emit = defineEmits<Emits>()

const inputText = ref('')

const canSend = computed(() => inputText.value.trim().length > 0 && !props.disabled)

function handleSend() {
  if (!canSend.value) return
  
  const text = inputText.value.trim()
  emit('send', text)
  inputText.value = ''
}

function handlePlus() {
  emit('plus')
}
</script>

<style scoped lang="scss">
.chat-input {
  background: #f7f7f7;
  padding: 20rpx 32rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 20rpx;
}

.plus-btn {
  width: 80rpx;
  height: 80rpx;
  border-radius: 10rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  .icon {
    font-size: 48rpx;
    color: #666;
  }
}

.input-wrapper {
  flex: 1;
  background: #fff;
  border-radius: 10rpx;
  padding: 20rpx 24rpx;
  min-height: 80rpx;
}

.input {
  width: 100%;
  font-size: 30rpx;
  line-height: 1.5;
  min-height: 40rpx;
  max-height: 200rpx;
}

.send-btn {
  width: 120rpx;
  height: 80rpx;
  border-radius: 10rpx;
  background: #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #999;
  font-size: 28rpx;
  transition: all 0.3s;

  &.active {
    background: #07c160;
    color: #fff;
  }
}
</style>

