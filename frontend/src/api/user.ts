/**
 * 用户相关API
 */
import { get, put } from './request'
import type { User } from '@/types'

/**
 * 获取用户信息
 */
export function getUserProfile() {
  return get<User>('/api/v1/user/profile')
}

/**
 * 更新用户信息
 */
export function updateUserProfile(data: Partial<User>) {
  return put<User>('/api/v1/user/profile', data)
}

/**
 * 获取用户设置
 */
export function getUserSettings() {
  return get<{
    context_size: number
    ai_style: string
    stream_output: boolean
  }>('/api/v1/user/settings')
}

/**
 * 更新用户设置
 */
export function updateUserSettings(data: any) {
  return put('/api/v1/user/settings', data)
}

