<template>
  <view class="settings-page">
    <!-- AI对话设置 -->
    <view class="settings-section">
      <view class="section-title">AI对话设置</view>
      
      <view class="setting-item">
        <view class="item-header">
          <text class="item-label">上下文条数</text>
          <text class="item-value">{{ contextSize }} 条</text>
        </view>
        <view class="item-desc">设置AI记忆的对话轮数，越多消耗越大</view>
        <slider 
          class="slider"
          :value="contextSize" 
          :min="5" 
          :max="20" 
          :step="1"
          activeColor="#667eea"
          backgroundColor="#e5e5e5"
          block-size="24"
          @change="handleContextChange"
        />
        <view class="slider-labels">
          <text>5条</text>
          <text>20条</text>
        </view>
      </view>
      
      <view class="setting-item">
        <view class="item-header">
          <text class="item-label">对话模式</text>
          <text class="item-value mode">{{ modeText }}</text>
        </view>
        <view class="item-desc">不同模式影响AI回答的详细程度</view>
        <view class="mode-options">
          <view 
            v-for="mode in modes" 
            :key="mode.value"
            class="mode-option"
            :class="{ active: aiStyle === mode.value }"
            @click="handleModeChange(mode.value)"
          >
            <view class="mode-icon">{{ mode.icon }}</view>
            <text class="mode-name">{{ mode.label }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 保存按钮 -->
    <view class="save-section">
      <button class="save-button" @click="handleSave">
        <text>保存设置</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '@/stores'
import { storage } from '@/utils/storage'
import { updateConversation } from '@/api'

const chatStore = useChatStore()

const contextSize = ref(10)
const aiStyle = ref('professional')

const modes = [
  { value: 'simple', label: '简单', icon: '📝', desc: '简明扼要，快速回答' },
  { value: 'balanced', label: '默认', icon: '⚖️', desc: '平衡专业性与易懂性' },
  { value: 'professional', label: '专业', icon: '🎓', desc: '详细专业，术语丰富' }
]

const modeText = computed(() => {
  return modes.find(m => m.value === aiStyle.value)?.label || '默认'
})

onMounted(() => {
  // 从当前会话或存储加载设置
  if (chatStore.currentConversation) {
    contextSize.value = chatStore.currentConversation.context_size || 10
    aiStyle.value = chatStore.currentConversation.ai_style || 'professional'
  } else {
    // 从本地存储加载默认设置
    const savedSettings = storage.get<any>('ai_settings')
    if (savedSettings) {
      contextSize.value = savedSettings.contextSize || 10
      aiStyle.value = savedSettings.aiStyle || 'professional'
    }
  }
})

function handleContextChange(e: any) {
  contextSize.value = e.detail.value
}

function handleModeChange(mode: string) {
  aiStyle.value = mode
}

async function handleSave() {
  try {
    // 保存到本地存储作为默认设置
    storage.set('ai_settings', {
      contextSize: contextSize.value,
      aiStyle: aiStyle.value
    })
    
    // 如果有当前会话，更新会话设置
    if (chatStore.currentConversation) {
      const updated = await updateConversation(chatStore.currentConversation.id, {
        context_size: contextSize.value,
        ai_style: aiStyle.value
      })
      
      // 更新 store 中的会话数据
      chatStore.currentConversation = updated
      const index = chatStore.conversations.findIndex(c => c.id === updated.id)
      if (index !== -1) {
        chatStore.conversations[index] = updated
      }
    }
    
    uni.showToast({
      title: '保存成功',
      icon: 'success'
    })
    
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error: any) {
    uni.showToast({
      title: error.message || '保存失败',
      icon: 'none'
    })
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.settings-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: $spacing-xxxl;
}

.settings-section {
  margin-top: $spacing-base;
  background: $bg-card;
  padding: $spacing-base;
}

.section-title {
  padding: $spacing-sm 0;
  font-size: $font-size-sm;
  color: $text-tertiary;
  font-weight: $font-weight-medium;
}

.setting-item {
  padding: $spacing-lg 0;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
}

.item-header {
  @include flex-between;
  margin-bottom: $spacing-sm;
}

.item-label {
  font-size: $font-size-lg;
  color: $text-primary;
  font-weight: $font-weight-semibold;
}

.item-value {
  font-size: $font-size-base;
  color: $primary;
  font-weight: $font-weight-medium;
  
  &.mode {
    color: $primary;
  }
}

.item-desc {
  font-size: $font-size-sm;
  color: $text-tertiary;
  line-height: 1.6;
  margin-bottom: $spacing-base;
}

.slider {
  width: 100%;
  margin: $spacing-lg 0 $spacing-sm;
}

.slider-labels {
  @include flex-between;
  font-size: $font-size-xs;
  color: $text-tertiary;
}

.mode-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-base;
  margin-top: $spacing-base;
}

.mode-option {
  @include flex-center;
  flex-direction: column;
  padding: $spacing-lg;
  background: $bg-page;
  border-radius: $radius-lg;
  border: 3rpx solid transparent;
  transition: all $duration-fast $ease-apple;
  
  &.active {
    background: rgba($primary, 0.1);
    border-color: $primary;
  }
  
  &:active {
    transform: scale(0.95);
  }
}

.mode-icon {
  font-size: 48rpx;
  margin-bottom: $spacing-sm;
}

.mode-name {
  font-size: $font-size-base;
  color: $text-primary;
  font-weight: $font-weight-medium;
}

.save-section {
  padding: $spacing-xxl $spacing-base;
}

.save-button {
  @include btn-primary;
  height: 88rpx;
  font-size: $font-size-lg;
}
</style>

