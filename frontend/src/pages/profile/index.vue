<template>
  <view class="profile-page">
    <!-- 用户信息卡片 -->
    <view class="user-section">
      <view class="user-card">
        <view class="user-header">
          <image 
            :src="userStore.user?.avatar_url || '/static/user-avatar.svg'" 
            class="avatar"
            mode="aspectFill"
          />
          <view class="user-info">
            <text class="nickname">{{ userStore.user?.nickname || '未设置昵称' }}</text>
            <text class="user-id">ID: {{ formatUserId(userStore.user?.openid) }}</text>
          </view>
          <view class="edit-btn" @click="handleEditProfile">
            <text class="edit-text">编辑</text>
          </view>
        </view>
        
        <!-- 余额 -->
        <view class="balance-card">
          <view class="balance-header">
            <view class="balance-label">
              <text class="balance-icon">💰</text>
              <text class="balance-text">账户余额</text>
            </view>
            <view class="recharge-btn" @click="handleRecharge">
              <text>充值</text>
            </view>
          </view>
          <view class="balance-amount">
            <text class="currency">¥</text>
            <text class="amount">{{ (userStore.user?.token_balance || 0) / 100 }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 功能列表 -->
    <view class="menu-section">
      <view class="menu-group">
        <view class="menu-item" @click="handleBazi">
          <view class="menu-left">
            <text class="menu-icon">☯</text>
            <text class="menu-title">八字排盘</text>
          </view>
          <view class="menu-right">
            <text class="menu-desc" v-if="baziCount > 0">已设置</text>
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="divider"></view>
        
        <view class="menu-item" @click="handleSettings">
          <view class="menu-left">
            <text class="menu-icon">⚙</text>
            <text class="menu-title">系统设置</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
        
        <view class="divider"></view>
        
        <view class="menu-item" @click="handleAbout">
          <view class="menu-left">
            <text class="menu-icon">ℹ</text>
            <text class="menu-title">关于我们</text>
          </view>
          <view class="menu-right">
            <text class="menu-arrow">›</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部退出登录 -->
    <view class="logout-section">
      <button class="logout-btn" @click="handleLogout">
        <text>退出登录</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores'

const userStore = useUserStore()
const baziCount = ref(0)

onMounted(async () => {
  // 加载八字数量
  // TODO: 从API获取
})

function formatUserId(openid: string | undefined): string {
  if (!openid) return '--------'
  
  // 使用hash算法生成8位数字ID（与edit页面保持一致）
  let hash = 0
  for (let i = 0; i < openid.length; i++) {
    hash = ((hash << 5) - hash) + openid.charCodeAt(i)
    hash = hash & hash
  }
  
  const num = Math.abs(hash) % 90000000 + 10000000
  return String(num)
}

function handleEditProfile() {
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}

function handleRecharge() {
  uni.navigateTo({
    url: '/pages/profile/recharge'
  })
}

function handleBazi() {
  uni.navigateTo({
    url: '/pages/profile/bazi'
  })
}

function handleSettings() {
  uni.navigateTo({
    url: '/pages/profile/settings'
  })
}

function handleConsumption() {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

function handleFeedback() {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

function handleAbout() {
  uni.showToast({
    title: '大师命理 v1.0.0',
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
  padding-bottom: $space-xxxl;
}

// ============================================
// 用户信息卡片
// ============================================

.user-section {
  padding: $space-lg $space-base $space-xl;
}

.user-card {
  @include card;
  padding: $space-lg;
}

.user-header {
  @include flex-center-y;
  margin-bottom: $space-xl;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: $radius-lg;
  background: $bg-hover;
  border: 2rpx solid $border-color;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  margin-left: $space-lg;
  min-width: 0;
}

.nickname {
  display: block;
  font-size: $font-lg;
  font-weight: $weight-semibold;
  color: $text-primary;
  margin-bottom: $space-xs;
  @include text-ellipsis;
}

.user-id {
  font-size: $font-sm;
  color: $text-tertiary;
}

.edit-btn {
  @include btn-ghost;
  height: 60rpx;
  padding: 0 $space-lg;
  border-radius: $radius-base;
  
  &:active {
    background: $bg-hover;
  }
}

.edit-text {
  font-size: $font-sm;
  color: $text-secondary;
}

// 余额卡片
.balance-card {
  background: linear-gradient(135deg, $primary 0%, $primary-light 100%);
  border-radius: $radius-lg;
  padding: $space-lg;
}

.balance-header {
  @include flex-between;
  margin-bottom: $space-base;
}

.balance-label {
  @include flex-center-y;
  gap: $space-sm;
}

.balance-icon {
  font-size: 32rpx;
}

.balance-text {
  font-size: $font-sm;
  color: rgba(255, 255, 255, 0.9);
  font-weight: $weight-medium;
}

.recharge-btn {
  background: rgba(255, 255, 255, 0.2);
  padding: $space-xs $space-base;
  border-radius: $radius-base;
  font-size: $font-xs;
  color: $text-inverse;
  font-weight: $weight-medium;
  
  &:active {
    opacity: 0.8;
  }
}

.balance-amount {
  @include flex-center-y;
}

.currency {
  font-size: $font-lg;
  color: rgba(255, 255, 255, 0.8);
  margin-right: $space-xs;
}

.amount {
  font-size: $font-xxxl;
  font-weight: $weight-bold;
  color: $text-inverse;
}

// ============================================
// 功能列表
// ============================================

.menu-section {
  padding: 0 $space-base;
  margin-bottom: $space-xl;
}

.menu-group {
  @include card;
  padding: 0;
  overflow: hidden;
}

.menu-item {
  @include flex-between;
  padding: $space-lg $space-base;
  transition: background $duration-fast;
  
  &:active {
    background: $bg-hover;
  }
}

.menu-left {
  @include flex-center-y;
  gap: $space-base;
  flex: 1;
  min-width: 0;
}

.menu-icon {
  font-size: 36rpx;
  width: 36rpx;
  text-align: center;
}

.menu-title {
  font-size: $font-base;
  color: $text-primary;
}

.menu-right {
  @include flex-center-y;
  gap: $space-sm;
}

.menu-desc {
  font-size: $font-sm;
  color: $accent;
}

.menu-arrow {
  font-size: 40rpx;
  color: $text-disabled;
  font-weight: 300;
}

.divider {
  height: 1rpx;
  background: $border-light;
  margin: 0 $space-base;
}

// ============================================
// 退出登录
// ============================================

.logout-section {
  padding: 0 $space-base;
}

.logout-btn {
  @include btn-ghost;
  width: 100%;
  height: 88rpx;
  font-size: $font-base;
  color: $error;
  
  &:active {
    background: rgba($error, 0.05);
  }
}
</style>
