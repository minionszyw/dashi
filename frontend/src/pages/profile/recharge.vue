<template>
  <view class="recharge-page">
    <!-- 充值套餐 -->
    <view class="package-section">
      <text class="section-title">选择充值套餐</text>
      <view class="packages">
        <view 
          v-for="pkg in packages" 
          :key="pkg.id"
          class="package-card"
          :class="{ active: selectedPackage === pkg.id }"
          @click="selectPackage(pkg.id)"
        >
          <view v-if="pkg.hot" class="hot-tag">热门</view>
          <text class="package-amount">{{ pkg.tokens }}</text>
          <text class="package-unit">Token</text>
          <text class="package-price">¥{{ pkg.price }}</text>
          <text class="package-desc">{{ pkg.desc }}</text>
        </view>
      </view>
    </view>

    <!-- 充值按钮 -->
    <view class="action-section safe-area-bottom">
      <button 
        class="recharge-button"
        :disabled="!selectedPackage"
        @click="handleRecharge"
      >
        <text>立即充值</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedPackage = ref<string>('')

const packages = [
  { id: '1', tokens: 100, price: 9.9, desc: '新手推荐', hot: false },
  { id: '2', tokens: 500, price: 39.9, desc: '超值优惠', hot: true },
  { id: '3', tokens: 1000, price: 69.9, desc: '畅聊无忧', hot: false },
  { id: '4', tokens: 2000, price: 119.9, desc: '尊享套餐', hot: false },
]

function selectPackage(id: string) {
  selectedPackage.value = id
}

function handleRecharge() {
  if (!selectedPackage.value) return
  
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.recharge-page {
  min-height: 100vh;
  background: $bg-page;
  padding: $space-base;
}

.package-section {
  margin-bottom: $space-xl;
}

.section-title {
  display: block;
  font-size: $font-lg;
  font-weight: $weight-semibold;
  color: $text-primary;
  margin-bottom: $space-lg;
}

.packages {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $space-base;
}

.package-card {
  @include card-bordered;
  padding: $space-xl $space-base;
  text-align: center;
  position: relative;
  transition: all $duration-base ease;
  
  &.active {
    border-color: $accent;
    box-shadow: $shadow-lg;
    background: rgba($accent, 0.02);
  }
  
  &:active {
    transform: scale(0.98);
  }
}

.hot-tag {
  position: absolute;
  top: -4rpx;
  right: -4rpx;
  background: $accent;
  color: $text-primary;
  font-size: $font-xs;
  padding: 4rpx 16rpx;
  border-radius: 0 $radius-lg 0 $radius-lg;
  font-weight: $weight-medium;
}

.package-amount {
  display: block;
  font-size: 56rpx;
  font-weight: $weight-bold;
  color: $accent;
  margin-bottom: 8rpx;
}

.package-unit {
  display: block;
  font-size: $font-sm;
  color: $text-tertiary;
  margin-bottom: $space-base;
}

.package-price {
  display: block;
  font-size: $font-xl;
  color: $error;
  font-weight: $weight-semibold;
  margin-bottom: $space-sm;
}

.package-desc {
  display: block;
  font-size: $font-xs;
  color: $text-secondary;
}

.action-section {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  padding: $space-base;
  background: $bg-card;
  border-top: 1rpx solid $border-color;
  @include safe-area-bottom;
}

.recharge-button {
  @include btn-primary;
  height: 88rpx;
  
  &[disabled] {
    opacity: 0.5;
  }
}
</style>
