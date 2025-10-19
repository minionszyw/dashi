<template>
  <view class="edit-page">
    <!-- 头像 -->
    <view class="edit-section">
      <view class="section-title">个人信息</view>
      <view class="edit-item" @click="handleChooseAvatar">
        <text class="item-label">头像</text>
        <view class="item-value">
          <image :src="form.avatar_url || '/static/default-avatar.svg'" class="avatar-preview" mode="aspectFill" />
          <text class="arrow">›</text>
        </view>
      </view>
      
      <view class="edit-item">
        <text class="item-label">昵称</text>
        <input 
          v-model="form.nickname" 
          class="item-input" 
          placeholder="请输入昵称"
          maxlength="20"
        />
      </view>
      
      <view class="edit-item disabled">
        <text class="item-label">用户ID</text>
        <text class="item-value-text disabled">{{ userId }}</text>
      </view>
    </view>

    <!-- 八字信息 -->
    <view class="edit-section" v-if="hasBazi">
      <view class="section-title">八字信息</view>
      <view class="edit-item" @click="handleGotoBazi">
        <text class="item-label">八字排盘</text>
        <view class="item-value">
          <text class="item-value-text">已设置</text>
          <text class="arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 保存按钮 -->
    <view class="save-section">
      <button class="save-button" @click="handleSave">
        <text>保存</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore, useBaziStore } from '@/stores'

const userStore = useUserStore()
const baziStore = useBaziStore()

const form = ref({
  nickname: '',
  avatar_url: ''
})

const hasBazi = computed(() => baziStore.profiles.length > 0)

const userId = computed(() => {
  const openid = userStore.user?.openid
  if (!openid) return '--------'
  
  let hash = 0
  for (let i = 0; i < openid.length; i++) {
    hash = ((hash << 5) - hash) + openid.charCodeAt(i)
    hash = hash & hash
  }
  
  const num = Math.abs(hash) % 90000000 + 10000000
  return String(num)
})

onMounted(async () => {
  form.value.nickname = userStore.user?.nickname || ''
  form.value.avatar_url = userStore.user?.avatar_url || ''
  await baziStore.loadProfiles()
})

function handleChooseAvatar() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      form.value.avatar_url = res.tempFilePaths[0]
    }
  })
}

function handleGotoBazi() {
  uni.navigateTo({
    url: '/pages/bazi/list'
  })
}

async function handleSave() {
  if (!form.value.nickname?.trim()) {
    uni.showToast({
      title: '请输入昵称',
      icon: 'none'
    })
    return
  }

  try {
    uni.showLoading({ title: '保存中...' })
    
    await userStore.updateUser({
      nickname: form.value.nickname,
      avatar_url: form.value.avatar_url
    })
    
    uni.hideLoading()
    uni.showToast({
      title: '保存成功',
      icon: 'success'
    })
    
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error: any) {
    uni.hideLoading()
    uni.showToast({
      title: error.message || '保存失败',
      icon: 'none'
    })
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.edit-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: $spacing-xxxl;
}

.edit-section {
  margin-top: $spacing-base;
  background: $bg-card;
}

.section-title {
  padding: $spacing-lg $spacing-base $spacing-sm;
  font-size: $font-size-sm;
  color: $text-tertiary;
  font-weight: $font-weight-medium;
}

.edit-item {
  @include flex-between;
  padding: $spacing-lg $spacing-base;
  border-bottom: 1rpx solid $border-color;
  
  &:last-child {
    border-bottom: none;
  }
  
  &.disabled {
    opacity: 0.6;
  }
  
  &:not(.disabled):active {
    background: $bg-hover;
  }
}

.item-label {
  font-size: $font-size-md;
  color: $text-primary;
  font-weight: $font-weight-medium;
}

.item-input {
  flex: 1;
  text-align: right;
  font-size: $font-size-md;
  color: $text-primary;
  margin-left: $spacing-base;
  
  &::placeholder {
    color: $text-tertiary;
  }
}

.item-value {
  @include flex-center-y;
  gap: $spacing-md;
}

.item-value-text {
  font-size: $font-size-md;
  color: $text-secondary;
  
  &.disabled {
    color: $text-tertiary;
  }
}

.avatar-preview {
  width: 100rpx;
  height: 100rpx;
  border-radius: $radius-base;
  background: $bg-page;
}

.arrow {
  font-size: 48rpx;
  color: $text-disabled;
  font-weight: $font-weight-light;
}

.save-section {
  padding: $spacing-xxl $spacing-base;
}

.save-button {
  @include btn-primary;
  height: 88rpx;
  font-size: $font-size-lg;
}
</style>

