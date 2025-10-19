/**
 * 认证相关API
 */
import { post, put } from './request'

/**
 * 微信登录
 */
export function wxLogin(code: string) {
  return post<{
    token: string
    user: any
    is_new_user: boolean
  }>('/api/v1/auth/wx-login', { code })
}

/**
 * 更新用户信息
 */
export function updateUser(data: { nickname?: string; avatar_url?: string }) {
  return put<any>('/api/v1/auth/user', data)
}

