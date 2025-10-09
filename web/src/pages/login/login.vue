<template>
  <view class="login-container">
    <view class="login-content">
      <view class="logo">
        <image src="/static/logo.png" mode="aspectFit" class="logo-img"></image>
      </view>
      
      <view class="title">国学大师</view>
      <view class="subtitle">AI驱动的命理分析服务</view>
      
      <view class="features">
        <view class="feature-item">
          <text class="feature-icon">🤖</text>
          <text class="feature-text">智能AI对话</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">💬</text>
          <text class="feature-text">多轮会话</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">⚡</text>
          <text class="feature-text">流式响应</text>
        </view>
      </view>
      
      <button class="login-btn" @tap="handleLogin" :loading="loading">
        <text>微信授权登录</text>
      </button>
      
      <view class="tips">
        登录即表示同意《用户协议》和《隐私政策》
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { wechatLogin } from '@/api/auth'

const loading = ref(false)

const handleLogin = () => {
  loading.value = true
  
  // 微信登录
  uni.login({
    provider: 'weixin',
    success: async (loginRes) => {
      try {
        const { data } = await wechatLogin(loginRes.code)
        
        // 保存token和用户信息
        uni.setStorageSync('token', data.access_token)
        uni.setStorageSync('userInfo', data.user)
        
        // 跳转到首页
        uni.switchTab({
          url: '/pages/index/index'
        })
      } catch (error) {
        console.error('登录失败:', error)
        uni.showToast({
          title: '登录失败，请重试',
          icon: 'none'
        })
      } finally {
        loading.value = false
      }
    },
    fail: (err) => {
      console.error('微信登录失败:', err)
      uni.showToast({
        title: '微信登录失败',
        icon: 'none'
      })
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
}

.login-content {
  width: 100%;
  text-align: center;
}

.logo {
  margin-bottom: 40rpx;
}

.logo-img {
  width: 200rpx;
  height: 200rpx;
  border-radius: 40rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 20rpx;
}

.subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 80rpx;
}

.features {
  display: flex;
  justify-content: space-around;
  margin-bottom: 100rpx;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature-icon {
  font-size: 48rpx;
  margin-bottom: 16rpx;
}

.feature-text {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.9);
}

.login-btn {
  background: #ffffff;
  color: #667eea;
  border-radius: 50rpx;
  height: 88rpx;
  line-height: 88rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin: 0 40rpx;
}

.tips {
  margin-top: 40rpx;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.6);
}
</style>

