<template>
  <view class="login-page">
    <!-- 主要内容区 -->
    <view class="content">
      <!-- Logo 和品牌区 -->
      <view class="brand-section fade-in">
        <view class="logo-wrapper">
          <image src="/static/logo.svg" mode="aspectFit" class="logo" />
        </view>
        <text class="app-name">国学大师</text>
        <text class="app-slogan">专业八字排盘 · AI智能解析</text>
      </view>
      
      <!-- 装饰性元素 -->
      <view class="decoration">
        <view class="decoration-line"></view>
        <text class="decoration-text">传承千年智慧</text>
        <view class="decoration-line"></view>
      </view>
    </view>
    
    <!-- 底部登录区 -->
    <view class="footer safe-area-bottom">
      <button 
        class="login-button"
        open-type="getUserInfo"
        @getuserinfo="handleGetUserInfo"
        :loading="loading"
        hover-class="login-button-hover"
      >
        <text class="button-text">{{ loading ? '登录中...' : '微信登录' }}</text>
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
  uni.switchTab({
    url: '/pages/session/index'
  })
}

function handlePrivacy() {
  uni.navigateTo({
    url: '/pages/login/privacy'
  })
}

function handleTerms() {
  uni.navigateTo({
    url: '/pages/login/terms'
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.login-page {
  min-height: 100vh;
  background: $bg-page;
  @include flex-column;
  justify-content: space-between;
}

// ============================================
// 主要内容
// ============================================

.content {
  flex: 1;
  @include flex-center;
  flex-direction: column;
  padding: $space-xxxl $space-xl;
}

// ============================================
// 品牌区
// ============================================

.brand-section {
  text-align: center;
  margin-bottom: $space-xxxl;
}

.logo-wrapper {
  width: 180rpx;
  height: 180rpx;
  margin: 0 auto $space-xl;
  @include flex-center;
}

.logo {
  width: 100%;
  height: 100%;
}

.app-name {
  display: block;
  font-size: $font-xxxl;
  font-weight: $weight-bold;
  color: $primary;
  margin-bottom: $space-sm;
  letter-spacing: 8rpx;
}

.app-slogan {
  display: block;
  font-size: $font-base;
  color: $text-secondary;
  letter-spacing: 2rpx;
}

// ============================================
// 装饰性元素
// ============================================

.decoration {
  @include flex-center-y;
  gap: $space-base;
  margin-top: $space-xxl;
  opacity: 0.6;
}

.decoration-line {
  width: 60rpx;
  height: 2rpx;
  background: linear-gradient(to right, transparent, $accent, transparent);
}

.decoration-text {
  font-size: $font-sm;
  color: $text-tertiary;
  letter-spacing: 2rpx;
}

// ============================================
// 底部登录区
// ============================================

.footer {
  padding: $space-xl;
}

.login-button {
  @include btn-primary;
  width: 100%;
  height: 96rpx;
  font-size: $font-md;
  border-radius: $radius-base;
  
  &:active:not([loading]) {
    transform: scale(0.98);
  }
}

.login-button-hover {
  opacity: 0.9;
}

.button-text {
  font-weight: $weight-medium;
  color: $text-inverse;
  letter-spacing: 2rpx;
}

// ============================================
// 协议提示
// ============================================

.agreement {
  margin-top: $space-lg;
  text-align: center;
  line-height: 1.8;
}

.agreement-text {
  font-size: $font-xs;
  color: $text-tertiary;
}

.agreement-link {
  font-size: $font-xs;
  color: $accent;
  margin: 0 4rpx;
  
  &:active {
    opacity: 0.7;
  }
}

// ============================================
// 动画
// ============================================

.fade-in {
  animation: fadeIn 0.8s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(40rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
