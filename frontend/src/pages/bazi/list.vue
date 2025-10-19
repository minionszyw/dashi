<template>
  <view class="bazi-list-page">
    <view v-if="loading" class="loading">
      <text>加载中...</text>
    </view>
    
    <view v-else-if="profiles.length === 0" class="empty">
      <text class="empty-text">还没有八字档案</text>
      <button class="btn-create" @click="handleCreate">
        <text>立即排盘</text>
      </button>
    </view>
    
    <view v-else class="list-container">
      <view 
        v-for="profile in profiles" 
        :key="profile.id" 
        class="profile-item"
        @click="handleViewDetail(profile.id)"
      >
        <view class="profile-header">
          <text class="profile-name">{{ profile.name }}</text>
          <text class="profile-gender">{{ profile.gender }}</text>
        </view>
        <view class="profile-info">
          <text class="info-text">{{ formatBirthDate(profile) }}</text>
        </view>
        <view class="profile-bazi">
          <text class="bazi-text">{{ profile.bazi_result.bazi }}</text>
        </view>
      </view>
      
      <view class="action-section">
        <button class="btn-add" @click="handleCreate">
          <text>+ 新增排盘</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBaziStore } from '@/stores'
import type { BaziProfile } from '@/types'

const baziStore = useBaziStore()
const loading = ref(true)
const profiles = ref<BaziProfile[]>([])

onMounted(async () => {
  try {
    await baziStore.loadProfiles()
    profiles.value = baziStore.profiles
  } catch (error) {
    console.error('加载八字档案列表失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
})

function formatBirthDate(profile: BaziProfile): string {
  const { year, month, day, hour, minute, calendar } = profile.birth_info
  return `${calendar} ${year}年${month}月${day}日 ${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`
}

function handleViewDetail(id: string) {
  uni.navigateTo({
    url: `/pages/bazi/result?id=${id}`
  })
}

function handleCreate() {
  uni.navigateTo({
    url: '/pages/bazi/calculate'
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.bazi-list-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: $spacing-xxl;
}

.loading, .empty {
  @include flex-center;
  flex-direction: column;
  min-height: 80vh;
}

.loading {
  font-size: $font-size-lg;
  color: $text-secondary;
}

.empty {
  gap: $spacing-xl;
}

.empty-text {
  font-size: $font-size-lg;
  color: $text-tertiary;
}

.btn-create {
  @include btn-primary;
  width: 320rpx;
  height: 88rpx;
  font-size: $font-size-lg;
}

.list-container {
  padding: $spacing-base;
}

.profile-item {
  @include card;
  margin-bottom: $spacing-base;
  padding: $spacing-lg;
  
  &:active {
    background: $bg-hover;
  }
}

.profile-header {
  @include flex-between;
  margin-bottom: $spacing-md;
}

.profile-name {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-primary;
}

.profile-gender {
  font-size: $font-size-md;
  color: $text-tertiary;
  padding: 4rpx 16rpx;
  background: $bg-page;
  border-radius: $radius-sm;
}

.profile-info {
  margin-bottom: $spacing-md;
}

.info-text {
  font-size: $font-size-sm;
  color: $text-secondary;
}

.profile-bazi {
  padding-top: $spacing-md;
  border-top: 1rpx solid $border-color;
}

.bazi-text {
  font-size: $font-size-lg;
  font-weight: $font-weight-medium;
  color: $primary;
  letter-spacing: 4rpx;
}

.action-section {
  margin-top: $spacing-xl;
  padding: 0 $spacing-base;
}

.btn-add {
  @include btn-secondary;
  width: 100%;
  height: 88rpx;
  font-size: $font-size-lg;
}
</style>

