/**
 * 认证相关API
 */
import { post, get, put } from '@/utils/request'

export interface UserInfo {
  id: number
  openid: string
  nickname?: string
  avatar_url?: string
  token_balance: number
  created_at: string
  last_login_at?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

/**
 * 微信登录
 */
export function wechatLogin(code: string) {
  return post<LoginResponse>('/api/v1/auth/wechat/login', { code })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return get<UserInfo>('/api/v1/auth/user/info')
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data: { nickname?: string; avatar_url?: string }) {
  return put<UserInfo>('/api/v1/auth/user/info', data)
}

