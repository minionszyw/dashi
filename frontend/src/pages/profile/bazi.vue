<template>
  <view class="bazi-page">
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-state">
      <text class="loading-icon">⏳</text>
      <text class="loading-text">加载中...</text>
    </view>
    
    <!-- 排盘内容 -->
    <view v-else-if="profile" class="content">
      <!-- 八字命盘 -->
      <view class="bazi-section">
        <view class="section-title">
          <text class="title-icon">☯</text>
          <text class="title-text">八字命盘</text>
        </view>
        <view class="bazi-display">
          <text class="bazi-text">{{ profile.bazi_result.bazi }}</text>
        </view>
      </view>

      <!-- 排盘详情 -->
      <view class="result-section" v-if="profile.bazi_result.formatted_output">
        <view class="section-title">
          <text class="title-icon">📜</text>
          <text class="title-text">排盘详情</text>
        </view>
        <view class="result-content">
          <text class="result-text">{{ profile.bazi_result.formatted_output }}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-btns">
        <button class="action-btn secondary" @click="handleEdit">
          <text>编辑信息</text>
        </button>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-state">
      <text class="empty-icon">📋</text>
      <text class="empty-text">还没有排盘档案</text>
      <text class="empty-desc">创建您的第一个八字排盘</text>
      <button class="empty-btn" @click="handleCreate">
        <text>创建排盘</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useBaziStore } from '@/stores'
import type { BaziProfile } from '@/types'

const baziStore = useBaziStore()

const loading = ref(true)
const profile = ref<BaziProfile | null>(null)

// 加载排盘数据
async function loadProfile() {
  loading.value = true
  try {
    await baziStore.loadProfiles()
    // 显示第一个（最新的）档案
    if (baziStore.profiles.length > 0) {
      profile.value = baziStore.profiles[0]
    } else {
      profile.value = null
    }
  } catch (error) {
    console.error('加载排盘失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfile()
})

// 页面显示时刷新数据
onShow(() => {
  loadProfile()
})

function formatBirthInfo(birthInfo: any): string {
  if (!birthInfo) return '未知'
  const { year, month, day, hour } = birthInfo
  return `${year}年${month}月${day}日 ${hour}时`
}

function handleEdit() {
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}

function handleCreate() {
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.bazi-page {
  min-height: 100vh;
  background: $bg-page;
}

// ============================================
// 加载状态
// ============================================

.loading-state {
  @include flex-center;
  flex-direction: column;
  min-height: 80vh;
  gap: $space-lg;
}

.loading-icon {
  font-size: 96rpx;
  animation: rotate 2s linear infinite;
}

.loading-text {
  font-size: $font-lg;
  color: $text-secondary;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// ============================================
// 内容区域
// ============================================

.content {
  padding: $space-base;
  padding-bottom: $space-xxxl;
}

// 八字命盘
.bazi-section {
  @include card-bordered;
  padding: $space-lg;
  margin-bottom: $space-base;
}

.section-title {
  @include flex-center-y;
  gap: $space-sm;
  font-size: $font-lg;
  font-weight: $weight-bold;
  color: $text-primary;
  margin-bottom: $space-lg;
  padding-bottom: $space-md;
  border-bottom: 2rpx solid $border-light;
}

.title-icon {
  font-size: 32rpx;
}

.title-text {
  font-size: $font-lg;
}

.bazi-display {
  padding: $space-xl 0;
  text-align: center;
  background: linear-gradient(135deg, rgba($accent, 0.05) 0%, rgba($primary, 0.05) 100%);
  border-radius: $radius-base;
}

.bazi-text {
  font-size: 48rpx;
  font-weight: $weight-bold;
  color: $accent;
  letter-spacing: 16rpx;
  line-height: 1.8;
}

// 排盘详情
.result-section {
  @include card-bordered;
  padding: $space-lg;
  margin-bottom: $space-base;
}

.result-content {
  padding: $space-md 0;
}

.result-text {
  font-size: $font-base;
  color: $text-secondary;
  line-height: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

// 操作按钮
.action-btns {
  padding: $space-lg 0;
}

.action-btn {
  @include btn-ghost;
  width: 100%;
  height: 88rpx;
  font-size: $font-base;
}

// ============================================
// 空状态
// ============================================

.empty-state {
  @include flex-center;
  flex-direction: column;
  min-height: 80vh;
  gap: $space-lg;
  padding: $space-xl;
}

.empty-icon {
  font-size: 120rpx;
  opacity: 0.3;
}

.empty-text {
  font-size: $font-xl;
  font-weight: $weight-medium;
  color: $text-primary;
}

.empty-desc {
  font-size: $font-base;
  color: $text-tertiary;
  margin-top: -$space-md;
}

.empty-btn {
  @include btn-primary;
  width: 320rpx;
  height: 88rpx;
  font-size: $font-base;
  margin-top: $space-lg;
}
</style>

