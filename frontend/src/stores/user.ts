/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { storage } from '@/utils/storage'
import { getUserProfile, updateUserProfile } from '@/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string>('')
  const isLogin = computed(() => !!token.value && !!user.value)

  /**
   * 设置Token
   */
  function setToken(newToken: string) {
    token.value = newToken
    storage.setToken(newToken)
  }

  /**
   * 设置用户信息
   */
  function setUser(newUser: User) {
    user.value = newUser
    storage.setUser(newUser)
  }

  /**
   * 初始化（从缓存加载）
   */
  function init() {
    token.value = storage.getToken()
    const cachedUser = storage.getUser()
    if (cachedUser) {
      user.value = cachedUser
    }
  }

  /**
   * 登录
   */
  function login(newToken: string, newUser: User) {
    setToken(newToken)
    setUser(newUser)
  }

  /**
   * 登出
   */
  function logout() {
    user.value = null
    token.value = ''
    storage.clear()
  }

  /**
   * 刷新用户信息
   */
  async function refreshUser() {
    try {
      const userData = await getUserProfile()
      setUser(userData)
      return userData
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      throw error
    }
  }

  /**
   * 更新用户信息
   */
  async function updateUser(data: Partial<User>) {
    try {
      const userData = await updateUserProfile(data)
      setUser(userData)
      return userData
    } catch (error) {
      console.error('更新用户信息失败:', error)
      throw error
    }
  }

  /**
   * 扣减Token余额
   */
  function deductTokenBalance(amount: number) {
    if (user.value) {
      user.value.token_balance -= amount
      storage.setUser(user.value)
    }
  }

  return {
    user,
    token,
    isLogin,
    setToken,
    setUser,
    init,
    login,
    logout,
    refreshUser,
    updateUser,
    deductTokenBalance
  }
})

