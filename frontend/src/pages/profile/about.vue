<template>
  <view class="about-page">
    <view class="content">
      <!-- Logo 和品牌 -->
      <view class="brand-section">
        <view class="logo-wrapper">
          <image src="/static/logo.svg" mode="aspectFit" class="logo" />
        </view>
        <text class="app-name">国学大师</text>
        <text class="version">版本 1.0.0</text>
      </view>

      <!-- 应用简介 -->
      <view class="intro-section">
        <text class="intro-text">
          国学大师是一款结合中国传统命理学与现代人工智能技术的应用。我们致力于将博大精深的八字命理学以科学、易懂的方式呈现，帮助您更好地认识自己，把握人生。
        </text>
        <text class="intro-text">
          本应用提供的命理分析仅供娱乐和参考，不构成任何人生决策建议。命运掌握在自己手中，积极进取、努力奋斗才是通往成功的关键。
        </text>
      </view>

      <!-- 联系方式 -->
      <view class="contact-section">
        <text class="section-title">联系我们</text>
        <view class="contact-list">
          <view class="contact-item">
            <text class="contact-label">官方邮箱</text>
            <text class="contact-value">support@guoxuedashi.com</text>
          </view>
          <view class="contact-item">
            <text class="contact-label">用户反馈</text>
            <text class="contact-value">通过应用内反馈功能</text>
          </view>
          <view class="contact-item">
            <text class="contact-label">商务合作</text>
            <text class="contact-value">business@guoxuedashi.com</text>
          </view>
        </view>
      </view>

      <!-- 法律链接 -->
      <view class="legal-links">
        <text class="link" @click="handlePrivacy">隐私政策</text>
        <text class="separator">|</text>
        <text class="link" @click="handleTerms">用户协议</text>
      </view>

      <!-- 版权信息 -->
      <view class="copyright">
        <text class="copyright-text">© 2025 国学大师 All Rights Reserved</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'

onLoad(() => {
  uni.setNavigationBarTitle({
    title: '关于我们'
  })
})

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

.about-page {
  min-height: 100vh;
  background: $bg-page;
}

.content {
  padding: $space-lg;
  padding-bottom: $space-xl;
}

// 品牌区域
.brand-section {
  @include flex-center;
  flex-direction: column;
  padding: $space-xl 0;
  margin-bottom: $space-lg;
}

.logo-wrapper {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: $space-base;
}

.logo {
  width: 100%;
  height: 100%;
}

.app-name {
  font-size: $font-xl;
  font-weight: 600;
  color: $primary;
  margin-bottom: $space-xs;
}

.version {
  font-size: $font-sm;
  color: $text-tertiary;
}

// 简介区域
.intro-section {
  margin-bottom: $space-xl;
  padding: $space-lg;
}

.intro-text {
  display: block;
  font-size: $font-base;
  color: $text-secondary;
  line-height: 2;
  margin-bottom: $space-lg;
  text-align: justify;
  
  &:last-child {
    margin-bottom: 0;
  }
}

// 通用标题
.section-title {
  display: block;
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $space-base;
  padding-left: $space-xs;
  border-left: 4rpx solid $accent;
}

// 联系方式
.contact-section {
  margin-bottom: $space-lg;
}

.contact-list {
  @include card-bordered;
  padding: $space-lg;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: $space-sm 0;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
}

.contact-label {
  width: 140rpx;
  font-size: $font-base;
  font-weight: 600;
  color: $text-primary;
  margin-right: $space-base;
}

.contact-value {
  flex: 1;
  font-size: $font-sm;
  color: $text-secondary;
}

// 法律链接
.legal-links {
  @include flex-center;
  margin-bottom: $space-base;
}

.link {
  font-size: $font-sm;
  color: $accent;
  
  &:active {
    opacity: 0.7;
  }
}

.separator {
  margin: 0 $space-base;
  font-size: $font-sm;
  color: $text-tertiary;
}

// 版权信息
.copyright {
  text-align: center;
  padding-top: $space-base;
  border-top: 1rpx solid $border-color;
}

.copyright-text {
  font-size: $font-xs;
  color: $text-tertiary;
}
</style>

