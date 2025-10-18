<template>
  <view class="login-container">
    <view class="content">
      <view class="logo">
        <image src="/static/logo.png" mode="aspectFit" />
      </view>
      <view class="title">大师AI命理</view>
      <view class="subtitle">专业命理分析·智能对话</view>
    </view>

    <view class="footer">
      <button
        class="login-btn"
        open-type="getUserInfo"
        @getuserinfo="handleGetUserInfo"
        :loading="loading"
      >
        <text>微信一键登录</text>
      </button>
      <view class="tips">
        <text>登录即表示同意</text>
        <text class="link" @click="handlePrivacy">《隐私政策》</text>
        <text>和</text>
        <text class="link" @click="handleTerms">《用户协议》</text>
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
    const loginRes = await uni.login({
      provider: 'weixin'
    })

    if (!loginRes[1].code) {
      throw new Error('获取登录凭证失败')
    }

    // 调用后端登录接口
    const result = await wxLogin(loginRes[1].code)

    // 保存登录状态
    userStore.login(result.token, result.user)

    // 显示欢迎提示
    if (result.is_new_user) {
      uni.showModal({
        title: '欢迎',
        content: `恭喜您获得${result.user.token_balance}个Token！`,
        showCancel: false,
        success: () => {
          navigateToHome()
        }
      })
    } else {
      navigateToHome()
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    uni.showToast({
      title: error.message || '登录失败，请重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

function navigateToHome() {
  uni.reLaunch({
    url: '/pages/chat/index'
  })
}

function handlePrivacy() {
  uni.navigateTo({
    url: '/pages/webview/index?url=privacy'
  })
}

function handleTerms() {
  uni.navigateTo({
    url: '/pages/webview/index?url=terms'
  })
}
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 100rpx 60rpx 60rpx;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logo {
  width: 200rpx;
  height: 200rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60rpx;

  image {
    width: 160rpx;
    height: 160rpx;
  }
}

.title {
  font-size: 64rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 20rpx;
}

.subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.footer {
  width: 100%;
}

.login-btn {
  width: 100%;
  height: 96rpx;
  background: #fff;
  border-radius: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: bold;
  color: #667eea;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);

  &::after {
    border: none;
  }
}

.tips {
  margin-top: 40rpx;
  text-align: center;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);

  .link {
    color: #fff;
    text-decoration: underline;
  }
}
</style>

