<template>
  <view class="bazi-list">
    <view class="list-container">
      <text class="title">八字档案</text>
      <text class="hint">八字档案列表页面开发中...</text>
    </view>
  </view>
</template>

<script setup lang="ts">
// 八字档案列表页面
</script>

<style scoped lang="scss">
.bazi-list {
  padding: 20rpx;
  
  .list-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    
    .title {
      font-size: 36rpx;
      font-weight: bold;
      margin-bottom: 20rpx;
    }
    
    .hint {
      font-size: 28rpx;
      color: #999;
    }
  }
}
</style>

