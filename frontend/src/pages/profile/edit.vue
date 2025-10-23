<template>
  <view class="edit-page">
    <!-- 个人信息 -->
    <view class="edit-section">
      <view class="section-title">个人信息</view>
      <view class="edit-item" @click="handleChooseAvatar">
        <text class="item-label">头像</text>
        <view class="item-value">
          <image :src="form.avatar_url || '/static/user-avatar.svg'" class="avatar-preview" mode="aspectFill" />
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
    <view class="edit-section">
      <view class="section-title">八字信息</view>
      
      <!-- 八字表单 -->
      <view class="bazi-form">
        <view class="edit-item">
          <text class="item-label">姓名</text>
          <input 
            v-model="baziForm.name" 
            class="item-input" 
            placeholder="请输入姓名"
            maxlength="10"
          />
        </view>
        
        <view class="edit-item">
          <text class="item-label">性别</text>
          <radio-group class="radio-group" @change="handleGenderChange">
            <label class="radio-item">
              <radio :checked="baziForm.gender === '男'" value="男" />
              <text>男</text>
            </label>
            <label class="radio-item">
              <radio :checked="baziForm.gender === '女'" value="女" />
              <text>女</text>
            </label>
          </radio-group>
        </view>
        
        <view class="edit-item">
          <text class="item-label">历法</text>
          <radio-group class="radio-group" @change="handleCalendarChange">
            <label class="radio-item">
              <radio :checked="baziForm.calendar === '公历'" value="公历" />
              <text>公历</text>
            </label>
            <label class="radio-item">
              <radio :checked="baziForm.calendar === '农历'" value="农历" />
              <text>农历</text>
            </label>
          </radio-group>
        </view>
        
        <view class="edit-item" @click="handleDatePicker">
          <text class="item-label">出生日期</text>
          <text :class="['picker-value', { placeholder: !baziForm.year }]">
            {{ datePickerText }}
          </text>
        </view>
        
        <view class="edit-item" @click="handleTimePicker">
          <text class="item-label">出生时间</text>
          <text :class="['picker-value', { placeholder: !hasSelectedTime }]">
            {{ timePickerText }}
          </text>
        </view>
        
        <view class="edit-item">
          <text class="item-label">出生城市</text>
          <input 
            v-model="baziForm.birth_city" 
            class="item-input" 
            placeholder="如:北京"
            maxlength="20"
          />
        </view>
        
        <view class="edit-item">
          <text class="item-label">现居城市</text>
          <input 
            v-model="baziForm.current_city" 
            class="item-input" 
            placeholder="选填，如:上海"
            maxlength="20"
          />
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
import { uploadAvatar } from '@/api/upload'
import type { BaziProfile } from '@/types'

const userStore = useUserStore()
const baziStore = useBaziStore()

const form = ref({
  nickname: '',
  avatar_url: ''
})

const baziForm = ref({
  name: '',
  gender: '男',
  calendar: '公历',
  year: 0,
  month: 0,
  day: 0,
  hour: 0,
  minute: 0,
  birth_city: '',
  current_city: ''
})

const hasBazi = computed(() => baziStore.profiles.length > 0)
const currentBaziProfile = computed(() => baziStore.profiles[0] || null)

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

const datePickerText = computed(() => {
  if (!baziForm.value.year) return '请选择出生日期'
  return `${baziForm.value.year}年${baziForm.value.month}月${baziForm.value.day}日`
})

const hasSelectedTime = computed(() => {
  return baziForm.value.hour !== 0 || baziForm.value.minute !== 0
})

const timePickerText = computed(() => {
  if (!hasSelectedTime.value) return '请选择出生时间'
  return `${String(baziForm.value.hour).padStart(2, '0')}:${String(baziForm.value.minute).padStart(2, '0')}`
})

onMounted(async () => {
  form.value.nickname = userStore.user?.nickname || ''
  form.value.avatar_url = userStore.user?.avatar_url || ''
  
  // 加载八字档案
  await baziStore.loadProfiles()
  
  // 如果有八字档案，自动填充到表单
  if (currentBaziProfile.value) {
    const profile = currentBaziProfile.value
    baziForm.value = {
      name: profile.name,
      gender: profile.gender,
      calendar: profile.birth_info.calendar,
      year: profile.birth_info.year,
      month: profile.birth_info.month,
      day: profile.birth_info.day,
      hour: profile.birth_info.hour,
      minute: profile.birth_info.minute,
      birth_city: profile.birth_info.birth_city,
      current_city: profile.birth_info.current_city || ''
    }
  }
})

function handleChooseAvatar() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: async (res) => {
      const tempFilePath = res.tempFilePaths[0]
      
      // 显示上传中
      uni.showLoading({ title: '上传中...' })
      
      try {
        // 上传头像
        const result = await uploadAvatar(tempFilePath)
        
        // 更新表单中的头像URL
        form.value.avatar_url = result.avatar_url
        
        // 同时更新用户store
        await userStore.refreshUser()
        
        uni.hideLoading()
        uni.showToast({
          title: '头像上传成功',
          icon: 'success'
        })
      } catch (error: any) {
        uni.hideLoading()
        console.error('头像上传失败:', error)
        uni.showToast({
          title: error.message || '头像上传失败',
          icon: 'none'
        })
      }
    }
  })
}

function handleGenderChange(e: any) {
  baziForm.value.gender = e.detail.value
}

function handleCalendarChange(e: any) {
  baziForm.value.calendar = e.detail.value
}

function handleDatePicker() {
  uni.showModal({
    title: '选择出生日期',
    editable: true,
    placeholderText: 'YYYY-MM-DD',
    success: (res) => {
      if (res.confirm && res.content) {
        const parts = res.content.split('-')
        if (parts.length === 3) {
          baziForm.value.year = parseInt(parts[0])
          baziForm.value.month = parseInt(parts[1])
          baziForm.value.day = parseInt(parts[2])
        }
      }
    }
  })
}

function handleTimePicker() {
  uni.showModal({
    title: '选择出生时间',
    editable: true,
    placeholderText: 'HH:MM',
    success: (res) => {
      if (res.confirm && res.content) {
        const parts = res.content.split(':')
        if (parts.length === 2) {
          baziForm.value.hour = parseInt(parts[0])
          baziForm.value.minute = parseInt(parts[1])
        }
      }
    }
  })
}

async function handleSave() {
  // 验证昵称
  if (!form.value.nickname?.trim()) {
    uni.showToast({
      title: '请输入昵称',
      icon: 'none'
    })
    return
  }

  // 验证八字信息（如果已填写）
  const hasBaziData = baziForm.value.name || baziForm.value.year || baziForm.value.birth_city
  if (hasBaziData) {
    if (!baziForm.value.name) {
      uni.showToast({ title: '请输入姓名', icon: 'none' })
      return
    }
    if (!baziForm.value.year || !baziForm.value.month || !baziForm.value.day) {
      uni.showToast({ title: '请选择出生日期', icon: 'none' })
      return
    }
    if (!hasSelectedTime.value) {
      uni.showToast({ title: '请选择出生时间', icon: 'none' })
      return
    }
    if (!baziForm.value.birth_city) {
      uni.showToast({ title: '请输入出生城市', icon: 'none' })
      return
    }
  }

  try {
    uni.showLoading({ title: '保存中...' })
    
    // 1. 更新昵称（头像已经在上传时更新了）
    await userStore.updateUser({
      nickname: form.value.nickname
    })
    
    // 2. 如果填写了八字信息，则保存或更新八字
    if (hasBaziData) {
      // 如果已有八字档案，先删除旧的
      if (currentBaziProfile.value) {
        await baziStore.removeProfile(currentBaziProfile.value.id)
      }
      
      // 计算新的八字
      await baziStore.calculate(baziForm.value)
    }
    
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
    console.error('保存失败:', error)
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
  padding-bottom: $space-xxxl;
}

.edit-section {
  margin-top: $space-base;
  background: $bg-card;
}

.section-title {
  padding: $space-lg $space-base $space-sm;
  font-size: $font-sm;
  color: $text-tertiary;
  font-weight: $weight-medium;
}

.edit-item {
  @include flex-between;
  padding: $space-lg $space-base;
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
  font-size: $font-md;
  color: $text-primary;
  font-weight: $weight-medium;
  min-width: 140rpx;
}

.item-input {
  flex: 1;
  text-align: right;
  font-size: $font-md;
  color: $text-primary;
  margin-left: $space-base;
  
  &::placeholder {
    color: $text-tertiary;
  }
}

.item-value {
  @include flex-center-y;
  gap: $space-md;
}

.item-value-text {
  font-size: $font-md;
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
  font-weight: $weight-light;
}

.radio-group {
  @include flex-center-y;
  gap: $space-xl;
}

.radio-item {
  @include flex-center-y;
  gap: $space-sm;
  font-size: $font-md;
  color: $text-primary;
}

.picker-value {
  flex: 1;
  text-align: right;
  font-size: $font-md;
  color: $text-primary;
  
  &.placeholder {
    color: $text-tertiary;
  }
}

.save-section {
  padding: $space-xxl $space-base;
}

.save-button {
  @include btn-primary;
  height: 88rpx;
  font-size: $font-lg;
}
</style>

