<template>
  <view class="bazi-result-page">
    <view v-if="loading" class="loading">
      <text>加载中...</text>
    </view>
    
    <view v-else-if="profile" class="result-container">
      <!-- 八字命盘 -->
      <view class="bazi-card">
        <view class="card-title">八字命盘</view>
        <view class="bazi-content">
          <text class="bazi-text">{{ profile.bazi_result.bazi }}</text>
        </view>
      </view>

      <!-- 详细解析 -->
      <view class="info-card" v-if="profile.bazi_result.formatted_output">
        <view class="card-title">详细解析</view>
        <view class="info-content">
          <text class="content-text formatted">{{ profile.bazi_result.formatted_output }}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-buttons">
        <button class="btn-edit" @click="handleEdit">
          <text>编辑</text>
        </button>
        <button class="btn-back" @click="handleBack">
          <text>返回</text>
        </button>
      </view>
    </view>

    <view v-else class="error">
      <text>加载失败</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useBaziStore } from '@/stores'
import type { BaziProfile } from '@/types'

const baziStore = useBaziStore()

const loading = ref(true)
const profile = ref<BaziProfile | null>(null)
const profileId = ref('')

onLoad((options) => {
  if (options.id) {
    profileId.value = options.id
  }
})

onMounted(async () => {
  if (profileId.value) {
    try {
      profile.value = await baziStore.loadProfile(profileId.value)
    } catch (error) {
      console.error('加载八字档案失败:', error)
      uni.showToast({
        title: '加载失败',
        icon: 'none'
      })
    } finally {
      loading.value = false
    }
  } else {
    loading.value = false
  }
})

function handleEdit() {
  // 跳转到编辑页面
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}

function handleBack() {
  uni.navigateBack()
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.bazi-result-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: $spacing-xxl;
}

.loading, .error {
  @include flex-center;
  min-height: 80vh;
  font-size: $font-size-lg;
  color: $text-secondary;
}

.result-container {
  padding: $spacing-base;
}

.info-card, .bazi-card {
  @include card;
  margin-bottom: $spacing-base;
  padding: $spacing-lg;
}

.card-title {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-sm;
  border-bottom: 2rpx solid $border-color;
}

.info-row {
  @include flex-between;
  padding: $spacing-md 0;
  
  &:not(:last-child) {
    border-bottom: 1rpx solid $bg-page;
  }
}

.label {
  font-size: $font-size-md;
  color: $text-tertiary;
  font-weight: $font-weight-medium;
}

.value {
  font-size: $font-size-md;
  color: $text-primary;
}

.bazi-content {
  padding: $spacing-lg 0;
  text-align: center;
}

.bazi-text {
  font-size: $font-size-xxl;
  font-weight: $font-weight-bold;
  color: $primary;
  letter-spacing: 8rpx;
  line-height: 1.8;
}

.info-content {
  padding: $spacing-md 0;
}

.content-text {
  font-size: $font-size-md;
  color: $text-secondary;
  line-height: 1.8;
  
  &.formatted {
    white-space: pre-wrap;
    font-family: monospace;
  }
}

.action-buttons {
  @include flex-center;
  gap: $spacing-lg;
  margin-top: $spacing-xl;
  padding: 0 $spacing-base;
}

.btn-edit {
  @include btn-secondary;
  flex: 1;
  height: 88rpx;
  font-size: $font-size-lg;
}

.btn-back {
  @include btn-primary;
  flex: 1;
  height: 88rpx;
  font-size: $font-size-lg;
}
</style>
