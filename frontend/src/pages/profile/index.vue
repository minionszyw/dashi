<template>
  <view class="profile-page">
    <!-- 个人信息区 -->
    <view class="user-info">
      <view class="user-header">
        <image :src="userStore.user?.avatar_url || '/static/default-avatar.png'" class="avatar" />
        <view class="user-details">
          <text class="nickname">{{ userStore.user?.nickname || '未设置昵称' }}</text>
          <text v-if="userStore.user?.birth_info" class="birth">
            {{ formatBirthInfo(userStore.user.birth_info) }}
          </text>
        </view>
        <text class="edit-btn" @click="handleEditProfile">编辑</text>
      </view>

      <view class="token-info">
        <view class="token-item">
          <text class="label">Token余额</text>
          <text class="value">{{ formatTokenBalance(userStore.user?.token_balance || 0) }}</text>
        </view>
        <button class="recharge-btn" @click="handleRecharge">充值</button>
      </view>
    </view>

    <!-- 菜单区 -->
    <view class="menu-section">
      <!-- 八字排盘 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleBaziCalculate">
          <view class="menu-left">
            <text class="icon">🔮</text>
            <text class="title">八字排盘</text>
          </view>
          <text class="arrow">›</text>
        </view>
        <view class="menu-item" @click="handleBaziProfiles">
          <view class="menu-left">
            <text class="icon">📋</text>
            <text class="title">八字档案管理</text>
          </view>
          <text class="arrow">›</text>
        </view>
      </view>

      <!-- 系统设置 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleSettings">
          <view class="menu-left">
            <text class="icon">⚙️</text>
            <text class="title">系统设置</text>
          </view>
          <text class="arrow">›</text>
        </view>
      </view>

      <!-- 关于 -->
      <view class="menu-group">
        <view class="menu-item" @click="handleAbout">
          <view class="menu-left">
            <text class="icon">ℹ️</text>
            <text class="title">关于我们</text>
          </view>
          <text class="arrow">›</text>
        </view>
      </view>

      <!-- 退出登录 -->
      <view class="menu-group">
        <view class="menu-item logout" @click="handleLogout">
          <view class="menu-left">
            <text class="icon">🚪</text>
            <text class="title">退出登录</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores'
import { formatTokenBalance } from '@/utils/format'

const userStore = useUserStore()

onMounted(async () => {
  // 刷新用户信息
  try {
    await userStore.refreshUser()
  } catch (error) {
    console.error('刷新用户信息失败:', error)
  }
})

function formatBirthInfo(birthInfo: any): string {
  if (!birthInfo) return ''
  return `${birthInfo.year}-${birthInfo.month}-${birthInfo.day}`
}

function handleEditProfile() {
  uni.navigateTo({
    url: '/pages/profile/edit'
  })
}

function handleRecharge() {
  uni.navigateTo({
    url: '/pages/recharge/index'
  })
}

function handleBaziCalculate() {
  uni.navigateTo({
    url: '/pages/bazi/calculate'
  })
}

function handleBaziProfiles() {
  uni.navigateTo({
    url: '/pages/bazi/list'
  })
}

function handleSettings() {
  uni.navigateTo({
    url: '/pages/settings/index'
  })
}

function handleAbout() {
  uni.navigateTo({
    url: '/pages/about/index'
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
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.user-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60rpx 40rpx 40rpx;
  color: #fff;
}

.user-header {
  display: flex;
  align-items: center;
  margin-bottom: 40rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  background: rgba(255, 255, 255, 0.2);
}

.user-details {
  flex: 1;
  margin-left: 24rpx;
}

.nickname {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 8rpx;
}

.birth {
  display: block;
  font-size: 24rpx;
  opacity: 0.8;
}

.edit-btn {
  padding: 12rpx 32rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 40rpx;
  font-size: 26rpx;
}

.token-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16rpx;
  backdrop-filter: blur(10rpx);
}

.token-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 24rpx;
  opacity: 0.8;
  margin-bottom: 8rpx;
}

.value {
  font-size: 48rpx;
  font-weight: bold;
}

.recharge-btn {
  padding: 12rpx 48rpx;
  background: #fff;
  color: #667eea;
  border-radius: 40rpx;
  font-size: 28rpx;
  font-weight: bold;

  &::after {
    border: none;
  }
}

.menu-section {
  padding: 24rpx 0;
}

.menu-group {
  margin-bottom: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx 40rpx;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: #f5f5f5;
  }

  &.logout {
    justify-content: center;

    .title {
      color: #fa5151;
    }
  }
}

.menu-left {
  display: flex;
  align-items: center;
}

.icon {
  font-size: 44rpx;
  margin-right: 24rpx;
}

.title {
  font-size: 30rpx;
}

.arrow {
  font-size: 48rpx;
  color: #ccc;
}
</style>

