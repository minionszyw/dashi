<template>
  <view class="login-page">
    <!-- 装饰性渐变背景 -->
    <view class="bg-gradient"></view>
    
    <!-- 主要内容区 -->
    <view class="content">
      <!-- Logo 和品牌区 -->
      <view class="brand-section fade-in">
        <view class="logo-wrapper">
          <image src="/static/logo.png" mode="aspectFit" class="logo" />
        </view>
        <text class="app-name">大师AI命理</text>
        <text class="app-slogan">专业命理分析 · 智能对话助手</text>
      </view>
      
      <!-- 特性展示 -->
      <view class="features fade-in-up">
        <view class="feature-item">
          <view class="feature-icon">✨</view>
          <text class="feature-text">AI智能分析</text>
        </view>
        <view class="feature-item">
          <view class="feature-icon">🎯</view>
          <text class="feature-text">专业八字排盘</text>
        </view>
        <view class="feature-item">
          <view class="feature-icon">💬</view>
          <text class="feature-text">实时对话咨询</text>
        </view>
      </view>
    </view>
    
    <!-- 底部登录区 -->
    <view class="footer safe-area-bottom">
      <button 
        class="login-button"
        open-type="getUserInfo"
        @getuserinfo="handleGetUserInfo"
        :loading="loading"
        hover-class="login-button-active"
      >
        <view class="button-content">
          <image src="/static/wechat-icon.svg" class="wechat-icon" v-if="!loading" />
          <text class="button-text">{{ loading ? '登录中...' : '微信一键登录' }}</text>
        </view>
      </button>
      
      <!-- 协议提示 -->
      <view class="agreement">
        <text class="agreement-text">登录即表示同意</text>
        <text class="agreement-link" @click="handlePrivacy">《隐私政策》</text>
        <text class="agreement-text">和</text>
        <text class="agreement-link" @click="handleTerms">《用户协议》</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { wxLogin } from '@/api'
import { useUserStore } from '@/stores'

const userStore = useUserStore()
const loading = ref(false)

async function handleGetUserInfo(e: any) {
  if (!e.detail.userInfo) {
    uni.showToast({
      title: '需要授权才能登录',
      icon: 'none'
    })
    return
  }

  try {
    loading.value = true

    // 获取微信登录code
    uni.login({
      provider: 'weixin',
      success: async (loginRes: any) => {
        try {
          if (!loginRes.code) {
            throw new Error('获取登录凭证失败')
          }

          // 调用后端登录接口
          const result = await wxLogin(loginRes.code)

          // 保存登录状态
          userStore.login(result.token, result.user)

          // 显示欢迎提示
          if (result.is_new_user) {
            uni.showModal({
              title: '欢迎使用',
              content: `恭喜您获得 ${result.user.token_balance} 个免费 Token！`,
              showCancel: false,
              confirmText: '开始体验',
              success: () => {
                navigateToHome()
              }
            })
          } else {
            uni.showToast({
              title: '登录成功',
              icon: 'success'
            })
            setTimeout(navigateToHome, 500)
          }
        } catch (error: any) {
          console.error('登录失败:', error)
          uni.showToast({
            title: error.message || '登录失败，请重试',
            icon: 'none',
            duration: 2000
          })
        } finally {
          loading.value = false
        }
      },
      fail: (err: any) => {
        console.error('微信登录失败:', err)
        uni.showToast({
          title: '微信登录失败，请重试',
          icon: 'none'
        })
        loading.value = false
      }
    })
  } catch (error: any) {
    console.error('登录异常:', error)
    uni.showToast({
      title: '登录异常，请重试',
      icon: 'none'
    })
    loading.value = false
  }
}

function navigateToHome() {
  uni.reLaunch({
    url: '/pages/chat/index'
  })
}

function handlePrivacy() {
  // TODO: 打开隐私政策页面
  uni.showToast({
    title: '隐私政策',
    icon: 'none'
  })
}

function handleTerms() {
  // TODO: 打开用户协议页面
  uni.showToast({
    title: '用户协议',
    icon: 'none'
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.login-page {
  position: relative;
  min-height: 100vh;
  background: $bg-page;
  overflow: hidden;
}

// ============================================
// 渐变背景
// ============================================

.bg-gradient {
  position: fixed;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: $primary-gradient;
  opacity: 0.08;
  transform: rotate(-12deg);
  z-index: 0;
}

// ============================================
// 主要内容
// ============================================

.content {
  position: relative;
  z-index: 1;
  min-height: 60vh;
  padding: 120rpx $spacing-xl $spacing-xl;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

// ============================================
// 品牌区
// ============================================

.brand-section {
  text-align: center;
  margin-bottom: $spacing-xxxl;
}

.logo-wrapper {
  width: 160rpx;
  height: 160rpx;
  margin: 0 auto $spacing-xl;
  background: $bg-card;
  border-radius: $radius-xl;
  @include flex-center;
  box-shadow: $shadow-lg;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    inset: -4rpx;
    background: $primary-gradient;
    border-radius: $radius-xl;
    opacity: 0.2;
    z-index: -1;
  }
}

.logo {
  width: 120rpx;
  height: 120rpx;
}

.app-name {
  display: block;
  font-size: $font-size-xxxl;
  font-weight: $font-weight-bold;
  @include gradient-text;
  margin-bottom: $spacing-sm;
  letter-spacing: 2rpx;
}

.app-slogan {
  display: block;
  font-size: $font-size-base;
  color: $text-secondary;
  font-weight: $font-weight-medium;
}

// ============================================
// 特性展示
// ============================================

.features {
  display: flex;
  gap: $spacing-lg;
  padding: 0 $spacing-base;
  animation-delay: 0.1s;
}

.feature-item {
  flex: 1;
  @include card;
  padding: $spacing-lg $spacing-base;
  text-align: center;
  transition: all $duration-base $ease-apple;
  
  &:active {
    transform: translateY(-4rpx);
    box-shadow: $shadow-md;
  }
}

.feature-icon {
  font-size: 48rpx;
  margin-bottom: $spacing-sm;
}

.feature-text {
  display: block;
  font-size: $font-size-sm;
  color: $text-secondary;
  font-weight: $font-weight-medium;
}

// ============================================
// 底部登录区
// ============================================

.footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  padding: $spacing-xl $spacing-xl $spacing-base;
  background: linear-gradient(to top, $bg-page 80%, transparent);
  z-index: 10;
}

.login-button {
  width: 100%;
  height: 96rpx;
  background: $wechat-green;
  border-radius: $radius-round;
  box-shadow: $shadow-md;
  transition: all $duration-base $ease-apple;
  
  &::after {
    border: none;
  }
  
  &:active:not([loading]) {
    transform: scale(0.98);
    box-shadow: $shadow-sm;
  }
}

.login-button-active {
  opacity: 0.9;
}

.button-content {
  @include flex-center;
  height: 100%;
}

.wechat-icon {
  width: 40rpx;
  height: 40rpx;
  margin-right: $spacing-sm;
}

.button-text {
  font-size: $font-size-md;
  font-weight: $font-weight-semibold;
  color: #ffffff;
}

// ============================================
// 协议提示
// ============================================

.agreement {
  margin-top: $spacing-lg;
  text-align: center;
  line-height: 1.8;
}

.agreement-text {
  font-size: $font-size-xs;
  color: $text-tertiary;
}

.agreement-link {
  font-size: $font-size-xs;
  color: $primary;
  margin: 0 4rpx;
  
  &:active {
    opacity: 0.7;
  }
}

// ============================================
// 动画
// ============================================

.fade-in {
  animation: fadeIn $duration-slow $ease-apple;
}

.fade-in-up {
  animation: fadeInUp $duration-slow $ease-apple;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(60rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
