/**
 * 本地存储工具
 */

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'user_info'

export const storage = {
  /**
   * 通用存储方法
   */
  set(key: string, value: any) {
    uni.setStorageSync(key, JSON.stringify(value))
  },

  /**
   * 通用获取方法
   */
  get<T>(key: string): T | null {
    const value = uni.getStorageSync(key)
    if (!value) return null
    try {
      return JSON.parse(value) as T
    } catch {
      return value as T
    }
  },

  /**
   * 通用移除方法
   */
  remove(key: string) {
    uni.removeStorageSync(key)
  },

  /**
   * 保存Token
   */
  setToken(token: string) {
    uni.setStorageSync(TOKEN_KEY, token)
  },

  /**
   * 获取Token
   */
  getToken(): string {
    return uni.getStorageSync(TOKEN_KEY) || ''
  },

  /**
   * 移除Token
   */
  removeToken() {
    uni.removeStorageSync(TOKEN_KEY)
  },

  /**
   * 保存用户信息
   */
  setUser(user: any) {
    uni.setStorageSync(USER_KEY, JSON.stringify(user))
  },

  /**
   * 获取用户信息
   */
  getUser(): any {
    const userStr = uni.getStorageSync(USER_KEY)
    return userStr ? JSON.parse(userStr) : null
  },

  /**
   * 移除用户信息
   */
  removeUser() {
    uni.removeStorageSync(USER_KEY)
  },

  /**
   * 清空用户数据（保留用户设置）
   */
  clear() {
    // 保存需要保留的用户偏好设置（不依赖于特定账号）
    const aiSettings = this.get('ai_settings')
    
    // 清空所有存储
    uni.clearStorageSync()
    
    // 恢复设置
    if (aiSettings) {
      this.set('ai_settings', aiSettings)
    }
  }
}

