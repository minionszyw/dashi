/**
 * 认证相关API
 */
import { post } from './request'

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

