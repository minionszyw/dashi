<template>
  <view class="bazi-calculate-page">
    <view class="form-container">
      <view class="form-item">
        <text class="label">姓名</text>
        <input v-model="formData.name" class="input" placeholder="请输入姓名" />
      </view>

      <view class="form-item">
        <text class="label">性别</text>
        <view class="radio-group">
          <label v-for="item in genderOptions" :key="item.value" class="radio-item">
            <radio :value="item.value" :checked="formData.gender === item.value" @click="formData.gender = item.value" />
            <text>{{ item.label }}</text>
          </label>
        </view>
      </view>

      <view class="form-item">
        <text class="label">日历</text>
        <view class="radio-group">
          <label v-for="item in calendarOptions" :key="item.value" class="radio-item">
            <radio :value="item.value" :checked="formData.calendar === item.value" @click="formData.calendar = item.value" />
            <text>{{ item.label }}</text>
          </label>
        </view>
      </view>

      <view class="form-item">
        <text class="label">出生日期</text>
        <picker mode="date" :value="dateValue" @change="handleDateChange">
          <view class="picker-value">{{ dateValue || '请选择日期' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">出生时间</text>
        <picker mode="time" :value="timeValue" @change="handleTimeChange">
          <view class="picker-value">{{ timeValue || '请选择时间' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">出生城市</text>
        <input v-model="formData.birth_city" class="input" placeholder="请输入出生城市" />
      </view>

      <view class="form-item">
        <text class="label">现居城市</text>
        <input v-model="formData.current_city" class="input" placeholder="请输入现居城市（选填）" />
      </view>

      <button class="submit-btn" :loading="loading" @click="handleSubmit">开始排盘</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useBaziStore } from '@/stores'

const baziStore = useBaziStore()

const formData = ref({
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

const loading = ref(false)

const genderOptions = [
  { label: '男', value: '男' },
  { label: '女', value: '女' }
]

const calendarOptions = [
  { label: '公历', value: '公历' },
  { label: '农历', value: '农历' }
]

const dateValue = computed(() => {
  if (!formData.value.year) return ''
  return `${formData.value.year}-${String(formData.value.month).padStart(2, '0')}-${String(formData.value.day).padStart(2, '0')}`
})

const timeValue = computed(() => {
  if (!formData.value.hour && !formData.value.minute) return ''
  return `${String(formData.value.hour).padStart(2, '0')}:${String(formData.value.minute).padStart(2, '0')}`
})

function handleDateChange(e: any) {
  const date = new Date(e.detail.value)
  formData.value.year = date.getFullYear()
  formData.value.month = date.getMonth() + 1
  formData.value.day = date.getDate()
}

function handleTimeChange(e: any) {
  const [hour, minute] = e.detail.value.split(':')
  formData.value.hour = parseInt(hour)
  formData.value.minute = parseInt(minute)
}

async function handleSubmit() {
  // 验证表单
  if (!formData.value.name) {
    uni.showToast({ title: '请输入姓名', icon: 'none' })
    return
  }
  if (!formData.value.year) {
    uni.showToast({ title: '请选择出生日期', icon: 'none' })
    return
  }
  if (!formData.value.birth_city) {
    uni.showToast({ title: '请输入出生城市', icon: 'none' })
    return
  }

  try {
    loading.value = true
    const profile = await baziStore.calculate(formData.value)
    
    uni.showToast({
      title: '排盘成功',
      icon: 'success',
      duration: 1500
    })

    // 跳转到结果页
    setTimeout(() => {
      uni.redirectTo({
        url: `/pages/bazi/result?id=${profile.id}`
      })
    }, 1500)
  } catch (error: any) {
    console.error('排盘失败:', error)
    uni.showToast({
      title: error.message || '排盘失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.bazi-calculate-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 24rpx;
}

.form-container {
  background: #fff;
  border-radius: 16rpx;
  padding: 40rpx;
}

.form-item {
  margin-bottom: 40rpx;

  &:last-child {
    margin-bottom: 0;
  }
}

.label {
  display: block;
  font-size: 28rpx;
  font-weight: 500;
  margin-bottom: 20rpx;
}

.input {
  width: 100%;
  height: 80rpx;
  padding: 0 24rpx;
  background: #f5f5f5;
  border-radius: 10rpx;
  font-size: 28rpx;
}

.radio-group {
  display: flex;
  gap: 40rpx;
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
  font-size: 28rpx;
}

.picker-value {
  height: 80rpx;
  line-height: 80rpx;
  padding: 0 24rpx;
  background: #f5f5f5;
  border-radius: 10rpx;
  font-size: 28rpx;
  color: #333;
}

.submit-btn {
  width: 100%;
  height: 96rpx;
  margin-top: 60rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 48rpx;
  font-size: 32rpx;
  font-weight: bold;

  &::after {
    border: none;
  }
}
</style>

