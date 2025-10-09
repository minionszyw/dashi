<template>
  <view class="profile-container">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <image class="user-avatar" :src="userInfo?.avatar_url || '/static/avatar.png'" mode="aspectFill"></image>
      <view class="user-info">
        <text class="user-name">{{ userInfo?.nickname || '未设置昵称' }}</text>
        <text class="user-id">ID: {{ userInfo?.id }}</text>
      </view>
    </view>
    
    <!-- 余额卡片 -->
    <view class="balance-card">
      <view class="balance-info">
        <text class="balance-label">账户余额</text>
        <text class="balance-value">{{ balance }}</text>
        <text class="balance-unit">Token</text>
      </view>
      <button class="recharge-btn" @tap="handleRecharge">充值</button>
    </view>
    
    <!-- 交易记录 -->
    <view class="transactions">
      <view class="section-title">交易记录</view>
      
      <view v-if="transactions.length === 0" class="empty-transactions">
        <text class="empty-text">暂无交易记录</text>
      </view>
      
      <view v-else class="transaction-list">
        <view v-for="trans in transactions" :key="trans.id" class="transaction-item">
          <view class="transaction-info">
            <text class="transaction-desc">{{ trans.description }}</text>
            <text class="transaction-time">{{ formatTime(trans.created_at) }}</text>
          </view>
          <view class="transaction-amount" :class="trans.type === 'recharge' ? 'income' : 'expense'">
            {{ trans.type === 'recharge' ? '+' : '-' }}{{ Math.abs(Number(trans.amount)) }}
          </view>
        </view>
      </view>
    </view>
    
    <!-- 设置项 -->
    <view class="settings">
      <view class="setting-item" @tap="handleAbout">
        <text class="setting-label">关于我们</text>
        <text class="setting-arrow">›</text>
      </view>
      <view class="setting-item" @tap="handleLogout">
        <text class="setting-label logout">退出登录</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserInfo } from '@/api/auth'
import { getBalance, getTransactions, createRecharge } from '@/api/billing'
import type { UserInfo } from '@/api/auth'
import type { Transaction } from '@/api/billing'

const userInfo = ref<UserInfo | null>(null)
const balance = ref(0)
const transactions = ref<Transaction[]>([])

onMounted(async () => {
  await loadUserInfo()
  await loadBalance()
  await loadTransactions()
})

const loadUserInfo = async () => {
  try {
    userInfo.value = uni.getStorageSync('userInfo')
    const { data } = await getUserInfo()
    userInfo.value = data
    uni.setStorageSync('userInfo', data)
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const loadBalance = async () => {
  try {
    const { data } = await getBalance()
    balance.value = data.balance
  } catch (error) {
    console.error('获取余额失败:', error)
  }
}

const loadTransactions = async () => {
  try {
    const { data } = await getTransactions(10)
    transactions.value = data
  } catch (error) {
    console.error('获取交易记录失败:', error)
  }
}

const handleRecharge = () => {
  uni.showModal({
    title: '充值',
    content: '充值功能开发中，敬请期待',
    showCancel: false
  })
}

const handleAbout = () => {
  uni.showModal({
    title: '关于我们',
    content: '国学大师 v0.1.0\n基于AI的命理分析服务',
    showCancel: false
  })
}

const handleLogout = () => {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        uni.removeStorageSync('token')
        uni.removeStorageSync('userInfo')
        uni.reLaunch({
          url: '/pages/login/login'
        })
      }
    }
  })
}

const formatTime = (time: string) => {
  const date = new Date(time)
  return date.toLocaleString()
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20rpx;
}

.user-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  padding: 40rpx;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  margin-right: 32rpx;
}

.user-info {
  flex: 1;
}

.user-name {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 8rpx;
}

.user-id {
  display: block;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.balance-card {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.balance-info {
  display: flex;
  align-items: baseline;
}

.balance-label {
  font-size: 28rpx;
  color: #666;
  margin-right: 16rpx;
}

.balance-value {
  font-size: 48rpx;
  font-weight: bold;
  color: #6366F1;
  margin-right: 8rpx;
}

.balance-unit {
  font-size: 24rpx;
  color: #999;
}

.recharge-btn {
  background: #6366F1;
  color: #ffffff;
  border-radius: 40rpx;
  height: 64rpx;
  line-height: 64rpx;
  padding: 0 40rpx;
  font-size: 28rpx;
}

.transactions {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 32rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.empty-transactions {
  padding: 80rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.transaction-list {
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.transaction-item:last-child {
  border-bottom: none;
}

.transaction-info {
  flex: 1;
}

.transaction-desc {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 8rpx;
}

.transaction-time {
  display: block;
  font-size: 24rpx;
  color: #999;
}

.transaction-amount {
  font-size: 32rpx;
  font-weight: bold;
}

.transaction-amount.income {
  color: #52c41a;
}

.transaction-amount.expense {
  color: #ff4d4f;
}

.settings {
  background: #ffffff;
  border-radius: 20rpx;
  overflow: hidden;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  font-size: 28rpx;
  color: #333;
}

.setting-label.logout {
  color: #ff4d4f;
}

.setting-arrow {
  font-size: 40rpx;
  color: #ccc;
}
</style>

