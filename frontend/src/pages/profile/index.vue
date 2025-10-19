<template>
  <view class="profile-page">
    <!-- 用户信息卡片 -->
    <view class="user-section">
      <view class="user-card">
        <view class="user-header">
          <image 
            :src="userStore.user?.avatar_url || '/static/default-avatar.svg'" 
            class="avatar"
            mode="aspectFill"
          />
          <view class="user-info">
            <text class="nickname">{{ userStore.user?.nickname || '未设置昵称' }}</text>
            <text class="user-id">ID: {{ formatUserId(userStore.user?.id) }}</text>
          </view>
        </view>
        
        <!-- Token余额 -->
        <view class="token-card">
          <view class="token-header">
            <view class="token-label">
              <text class="token-icon">💎</text>
              <text class="token-text">我的Token</text>
            </view>
            <view class="recharge-btn" @click="handleRecharge">
              <text>充值</text>
            </view>
          </view>
          <text class="token-balance">{{ userStore.user?.token_balance || 0 }}</text>
        </view>
      </view>
    </view>

    <!-- 功能列表 -->
    <view class="menu-section">
      <!-- 八字管理 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleNavigate('/pages/bazi/calculate')">
          <view class="menu-left">
            <view class="menu-icon-wrapper primary">
              <text class="menu-icon">📊</text>
            </view>
            <text class="menu-title">八字排盘</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="menu-item" @click="handleNavigate('/pages/bazi/list')">
          <view class="menu-left">
            <view class="menu-icon-wrapper info">
              <text class="menu-icon">📁</text>
            </view>
            <text class="menu-title">八字档案</text>
          </view>
          <view class="menu-right">
            <text class="menu-badge" v-if="baziCount > 0">{{ baziCount }}</text>
            <text class="menu-arrow">›</text>
          </view>
        </view>
      </view>

      <!-- 订单记录 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleNavigate('/pages/recharge/index')">
          <view class="menu-left">
            <view class="menu-icon-wrapper success">
              <text class="menu-icon">💰</text>
            </view>
            <text class="menu-title">充值记录</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="menu-item" @click="handleNavigate('/pages/order/list')">
          <view class="menu-left">
            <view class="menu-icon-wrapper warning">
              <text class="menu-icon">📦</text>
            </view>
            <text class="menu-title">消费记录</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
      </view>

      <!-- 设置 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleFeedback">
          <view class="menu-left">
            <view class="menu-icon-wrapper">
              <text class="menu-icon">💬</text>
            </view>
            <text class="menu-title">意见反馈</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="menu-item" @click="handleAbout">
          <view class="menu-left">
            <view class="menu-icon-wrapper">
              <text class="menu-icon">ℹ️</text>
            </view>
            <text class="menu-title">关于我们</text>
          </view>
          <view class="menu-right">
            <text class="menu-desc">v1.0.0</text>
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="menu-item" @click="handleSettings">
          <view class="menu-left">
            <view class="menu-icon-wrapper">
              <text class="menu-icon">⚙️</text>
            </view>
            <text class="menu-title">设置</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section safe-area-bottom">
      <button class="logout-button" @click="handleLogout">
        <text>退出登录</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useUserStore, useBaziStore } from '@/stores'

const userStore = useUserStore()
const baziStore = useBaziStore()

const baziCount = computed(() => baziStore.profiles.length)

onMounted(async () => {
  // 加载八字档案数量
  await baziStore.loadProfiles()
})

function formatUserId(id?: string): string {
  if (!id) return '---'
  return id.substring(0, 8)
}

function handleNavigate(url: string) {
  uni.navigateTo({ url })
}

function handleRecharge() {
  uni.navigateTo({
    url: '/pages/recharge/index'
  })
}

function handleFeedback() {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

function handleAbout() {
  uni.showModal({
    title: '关于我们',
    content: '大师AI命理 v1.0.0\n\n专业的命理分析智能助手',
    showCancel: false
  })
}

function handleSettings() {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

function handleLogout() {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.reLaunch({
          url: '/pages/login/index'
        })
      }
    }
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.profile-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: $spacing-xl;
}

// ============================================
// 用户信息区
// ============================================

.user-section {
  padding: $spacing-xl $spacing-base $spacing-base;
}

.user-card {
  @include card;
  padding: $spacing-xl;
  background: $primary-gradient;
  position: relative;
  overflow: visible;
}

.user-header {
  @include flex-center-y;
  gap: $spacing-lg;
  margin-bottom: $spacing-xl;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: $radius-round;
  border: 6rpx solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
}

.user-info {
  flex: 1;
}

.nickname {
  display: block;
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: #ffffff;
  margin-bottom: $spacing-sm;
}

.user-id {
  display: block;
  font-size: $font-size-sm;
  color: rgba(255, 255, 255, 0.8);
}

// Token卡片
.token-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20rpx);
  border-radius: $radius-lg;
  padding: $spacing-lg;
}

.token-header {
  @include flex-between;
  margin-bottom: $spacing-base;
}

.token-label {
  @include flex-center-y;
  gap: $spacing-sm;
}

.token-icon {
  font-size: $font-size-lg;
}

.token-text {
  font-size: $font-size-base;
  color: rgba(255, 255, 255, 0.9);
  font-weight: $font-weight-medium;
}

.recharge-btn {
  background: rgba(255, 255, 255, 0.3);
  border-radius: $radius-round;
  padding: 8rpx $spacing-base;
  font-size: $font-size-sm;
  color: #ffffff;
  font-weight: $font-weight-medium;
  transition: all $duration-fast $ease-apple;
  
  &:active {
    transform: scale(0.95);
    background: rgba(255, 255, 255, 0.4);
  }
}

.token-balance {
  font-size: 80rpx;
  font-weight: $font-weight-bold;
  color: #ffffff;
  line-height: 1;
  @include gradient-text(linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.8) 100%));
}

// ============================================
// 菜单列表
// ============================================

.menu-section {
  padding: 0 $spacing-base;
}

.menu-group {
  @include card;
  margin-bottom: $spacing-base;
  overflow: hidden;
}

.menu-item {
  @include flex-between;
  padding: $spacing-lg;
  transition: all $duration-fast $ease-apple;
  
  &:not(:last-child) {
    border-bottom: 1rpx solid $border-color;
  }
  
  &:active {
    background: $bg-hover;
  }
}

.menu-left {
  @include flex-center-y;
  gap: $spacing-lg;
  flex: 1;
  min-width: 0;
}

.menu-icon-wrapper {
  width: 72rpx;
  height: 72rpx;
  @include flex-center;
  background: $bg-page;
  border-radius: $radius-lg;
  flex-shrink: 0;
  
  &.primary {
    background: linear-gradient(135deg, rgba($primary, 0.1) 0%, rgba($primary, 0.2) 100%);
  }
  
  &.info {
    background: linear-gradient(135deg, rgba($info, 0.1) 0%, rgba($info, 0.2) 100%);
  }
  
  &.success {
    background: linear-gradient(135deg, rgba($success, 0.1) 0%, rgba($success, 0.2) 100%);
  }
  
  &.warning {
    background: linear-gradient(135deg, rgba($warning, 0.1) 0%, rgba($warning, 0.2) 100%);
  }
}

.menu-icon {
  font-size: 40rpx;
}

.menu-title {
  font-size: $font-size-md;
  color: $text-primary;
  font-weight: $font-weight-medium;
}

.menu-right {
  @include flex-center-y;
  gap: $spacing-sm;
  flex-shrink: 0;
}

.menu-badge {
  @include badge;
  transform: scale(0.8);
}

.menu-desc {
  font-size: $font-size-sm;
  color: $text-tertiary;
}

.menu-arrow {
  font-size: 48rpx;
  color: $text-disabled;
  font-weight: $font-weight-light;
}

// ============================================
// 退出登录
// ============================================

.logout-section {
  padding: $spacing-xxl $spacing-base;
  @include safe-area-bottom;
}

.logout-button {
  @include btn-secondary;
  height: 88rpx;
  color: $error;
  border-color: $error;
  
  &:active {
    background: rgba($error, 0.05);
  }
}
</style>

