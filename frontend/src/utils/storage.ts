/**
 * 本地存储工具
 */

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'user_info'

export const storage = {
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
   * 清空所有存储
   */
  clear() {
    uni.clearStorageSync()
  }
}

